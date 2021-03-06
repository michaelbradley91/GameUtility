'''
Created on 5 Jul 2014

@author: michael
'''

'''
Here's how it is going to work:

We will divide the screen into 32 * 16 pieces (where the 32 divides the width, and the 16 divides the height).
We will have one rectangle tree to be initialised with all of these rectangles. Call this rectangle tree
the "Screen Tree"

(Note that the exact number of ways we divide the screen may be adjusted according to stress tests...)

When a rectangle for updating is registered, we find all the rectangles colliding with it in the Screen Tree.
As these rectangles are found, we also remove them from the tree, and remember them in a grid
which is a 32 * 16 boolean array.

Once all of the updates are registered (with the above process repeated), we will compute the largest rectangles
filling the grid formed effectively by the 32 * 16 boolean array (the items being true must be filled).
We then reconstruct the corresponding rectangle coordinates.

In the meantime we have another rectangle tree which we will call the "Item Tree". The Item Tree holds rectangles
bounding areas that the various drawers are interested in. With the rectangles constructed from the grid,
we now compute how each one collides with the rectangles in the item tree.

We collect these items up, sort them in order, and instruct them to redraw over the rectangle.
(Technically, large rectangles increase the number of items which must be sorted, so it may be beneficial
to have smaller rectangles. However, I seriously doubt it would be worth it due to the amount of extra
redraws that might be necessary with smaller rectangles).

When items want to register their interest in parts of the screen, they are added to the Item Tree
(and subsequently removed if necessary in a similar manner).

Efficiency note:

The use of lots of rectangles dividing the screen in the Screen Tree is an easier way to compute the largest
rectangles. However, it would be better if we could directly merge the rectangles somehow so that we don't create
lots of small rectangles inside a large rectangle. Unfortunately, this seems to be hard in practice...

TODO: create drawing panes to ensure that certain objects can always be drawn, so
that the panes themselves will always be drawn in the right order...

TODO: currently ignoring alphas and so only permitting colour keys... not sure how much
I care...
'''

from mjb.dev.game_utility.graphics.screen import _PictureHandler, Screen
import pygame
import threading
from mjb.dev.game_utility.collisions.large_rectangle_tree import LargeRectangleTree
from mjb.dev.game_utility.collisions.small_rectangle_tree import SmallRectangleTree
from mjb.dev.game_utility.utility.rectangle_filler import RectangleFiller
from mjb.dev.game_utility.collisions.screen_collider import ScreenCollider

class Drawer(object):
    '''
    This class is an interface for an object which wishes to draw itself into the picture.
    Note that it is best to stick to the same drawer if you are "moving" the drawn image.
    The drawer itself determines whether or not it appears on top of another drawer
    on the screen in the event of a tie in the depth. Thus, if you want the image to be drawn
    in a consistent order with other images, stick to the same drawer!
    (Or be more explicit about the depth...)
    '''
    
    def redraw(self, top_left, surface):
        '''
        Called by the picture handler when this object needs to redraw itself
        on the surface provided. No interaction with the picture handler is allowed
        if you are drawing - this will cause deadlock (no registrations or deregistrations)
        @param top_left: the top left coordinate of the surface as it will be blitted to the screen
        (Surface begins at 0,0)
        @param surface: the surface to drawn on. Other than drawing itself, the surface should
        not be tampered with. Get the clip area to see the rectangle in which the drawing is
        actually occurring if you can exploit that for efficiency.
        '''
        pass
    
    def get_bounding_rectangle(self):
        '''
        @return: a rectangle in the form of (x_min,y_min,x_max,y_max) covering the whole
        area that the drawer might draw in. This should not change.
        '''
        pass
    
    def get_inner_shape(self):
        '''
        @return: the inner rectangles more accurately representing the space occupied by
        the drawer. This should be a pair of (rectangle_list,collider). If no inner representation
        exists, this should be ([],None)
        '''
        pass
    
    def get_depth(self):
        '''
        @return: the depth this drawer wishes to draw at. This should not change, and should
        be unique to each object to be drawn.
        '''
        pass
        
class _DummyPictureHandler(_PictureHandler):
    '''
    This handler just passes the calls to the static class
    '''
    def __init__(self):
        pass

    def get_picture(self):
        return PictureHandler._get_picture()
    
    def picture_drawn(self):
        PictureHandler._picture_drawn()

class PictureHandler(object):
    '''
    This class handles how things are drawn to the screen.
    The class ensures that images can be moved around on screen, and expect overlapping to be managed
    correctly.
    '''
        
    #The dummy picture handler to link with the screen
    __handler = _DummyPictureHandler()
    #Stats about the screen, held here for convenience
    __background_colour = None
    __size = None
    #Whether or not the PictureHandler has been initialised
    __initialised = False
    #The picture being blitted
    __picture = None
    #A lock for the picture while it is being modified.
    __picture_lock = threading.Semaphore()
    
    #The number of width divisions along the screen
    __WIDTH_DIVISION = 32;
    #The number of height divisions along the screen
    __HEIGHT_DIVISION = 16;
    
    #The list of rectangles to fill the screen rectangle tree
    __SCREEN_RECTANGLES = []
    
    #Storing the conversion back to the screen coordinates
    __MIN_X_COORD_SCREEN_CONVERSION = []
    __MAX_X_COORD_SCREEN_CONVERSION = []
    __MIN_Y_COORD_SCREEN_CONVERSION = []
    __MAX_Y_COORD_SCREEN_CONVERSION = []
    
    #The screen rectangle tree (divides the screen up into a grid)
    __screen_rectangle_tree = None
    #The picture rectangle tree
    __picture_rectangle_tree = None
    #The rectangles that need to be added to the tree...
    __screen_rectangles_to_add = []
    
    @staticmethod
    def initialise():
        '''
        Initialise the picture handler. This should be done strictly after the screen has been
        initialised, and strictly before any requests are made to the picture handler.
        This should only be called once.
        Note that the screen should be at least 32 * 32 pixels.
        '''
        if PictureHandler.__initialised:
            raise ValueError("Cannot initialise the picture handler more than once")
        #Remember some stats about the screen
        PictureHandler.__background_colour = Screen.get_background_colour()
        PictureHandler.__size = Screen.get_screen_size()
        #Initialise the picture
        PictureHandler.__picture = pygame.Surface(PictureHandler.__size)
        PictureHandler.__picture = PictureHandler.__picture.convert()
        PictureHandler.__picture.fill(PictureHandler.__background_colour)
        #Assign self as the picture handler
        Screen.set_picture_handler(PictureHandler.__handler)
        #Initialise the grid mechanism
        PictureHandler.__initialise_grid()
        #Remember we did this!
        PictureHandler.__initialised = True
        
    @staticmethod
    def __initialise_grid():
        '''
        Populates the grid rectangle tree and sets the "arrays" (default dictionaries)
        '''
        #Firstly, figure out the width and height dividers again...
        (screen_width,screen_height) = PictureHandler.__size
        #For convenience
        width_div = PictureHandler.__WIDTH_DIVISION
        height_div = PictureHandler.__HEIGHT_DIVISION
        #Now fill the arrays...
        #Divide by the width
        width_dividers = []
        width_division = screen_width / width_div
        for i in range(0,width_div):
            width_dividers.append(i * width_division)
        for i in range(0,screen_width % width_div): #the remainder
            width_dividers[width_div-(1+i)] = width_dividers[width_div-(1+i)] + (screen_width % width_div) - i
        #Repeat for the height
        height_dividers = []
        height_division = screen_height / height_div
        for i in range(0,height_div):
            height_dividers.append(i * height_division)
        for i in range(0,screen_height % height_div): #the remainder
            height_dividers[height_div-(i+1)] = height_dividers[height_div-(i+1)] + (screen_height % height_div) - i
        #For convenience:
        width_dividers.append(screen_width) #plus one because we consider being >= to be in the sector
        height_dividers.append(screen_height)
        #Now calculate the rectangles...
        for x in range(0,width_div):
            for y in range(0,height_div):
                #Figure out the rectangle in its (x_min,y_min,x_max,y_max) form
                x_min = width_dividers[x]
                x_max = width_dividers[x+1]
                y_min = height_dividers[y]
                y_max = height_dividers[y+1]
                #Use the key to remember the coordinates
                rect = (x_min,y_min,x_max,y_max,(x,y))
                PictureHandler.__SCREEN_RECTANGLES.append(rect)
        
        #We will receive the rectangle coordinates, and would like to know where they fit
        #in the grid. We store this for speed
        for x in range(0,width_div):
            PictureHandler.__MIN_X_COORD_SCREEN_CONVERSION.append(width_dividers[x])
            PictureHandler.__MAX_X_COORD_SCREEN_CONVERSION.append(width_dividers[x+1])
        for y in range(0,height_div):
            PictureHandler.__MIN_Y_COORD_SCREEN_CONVERSION.append(height_dividers[y])
            PictureHandler.__MAX_Y_COORD_SCREEN_CONVERSION.append(height_dividers[y+1])
        #Fill the tree
        PictureHandler.__screen_rectangles_to_add = PictureHandler.__SCREEN_RECTANGLES
        PictureHandler.__screen_rectangle_tree = ScreenCollider(
            #Use a small rectangle tree for the screen itself
            SmallRectangleTree(PictureHandler.__size),
            #These rectangles are plain old big rectangles.
            lambda _: ([],None)
            )
        #Fill it
        PictureHandler.__fill_screen_tree()
        PictureHandler.__screen_rectangles_to_add = [] #don't update on this...
        #Finally set up the picture rectangle tree...
        PictureHandler.__picture_rectangle_tree = ScreenCollider(
            #Use a large rectangle tree to hold the picture
            LargeRectangleTree(PictureHandler.__size),
            #Extract the inner rectangles from the drawer
            lambda (a,b,c,d,drawer): drawer.get_inner_shape()
            )
        
    @staticmethod
    def __fill_screen_tree():
        '''
        Fill the rectangle tree for the screen (not the images)
        '''
        for rect in PictureHandler.__screen_rectangles_to_add:
            PictureHandler.__screen_rectangle_tree.insert_rectangle(rect)
        #Really simple
    
    @staticmethod
    def __add_to_screen(drawer):
        '''
        Add a given drawer to the screen
        @param drawer: the drawer to add
        '''
        rect = drawer.get_bounding_rectangle()
        #Add the rectangle to the screen rectangle tree by colliding it first
        #TODO REMOVE print("Adding rectangle " + str(rect))
        (rect_list,collider) = drawer.get_inner_shape()
        collided_rects = PictureHandler.__screen_rectangle_tree.collide_rectangle(
            rect,rect_list,collider)
        #TODO REMOVE print("Got collided rectangles " + str(collided_rects))
        #Now remove the collided rectangles
        for rect in collided_rects:
            was_removed = PictureHandler.__screen_rectangle_tree.remove_rectangle(rect)
            if was_removed:
                PictureHandler.__screen_rectangles_to_add.append(rect)
        #Done!
        #TODO REMOVE print("Got update list as " + str(PictureHandler.__screen_rectangles_to_add))
        
    @staticmethod
    def __calculate_screen_update_list():
        '''
        Given the rectangles which have been added to the screen,
        this calculates a list of rectangles specifying the areas which need
        to be updated.
        This should only be called once per frame, since it resets itself.
        @return: a list of rectangles to use to update the screen, in the form
        of (x_min, y_min, x_max, y_max, None) (key for the next tree)
        '''
        #TODO REMOVE print("Calculating update list")
        #Firstly, gather the coordinates and update the screen rectangle tree...
        coords = []
        for rect in PictureHandler.__screen_rectangles_to_add:
            (_,_,_,_,(x,y)) = rect
            coords.append((x,y))
            #Now fill the rectangle tree again
            PictureHandler.__screen_rectangle_tree.insert_rectangle(rect)
        #Empty the update list
        #TODO REMOVE print("Filling coords " + str(coords))
        PictureHandler.__screen_rectangles_to_add = []
        #Calculate the covering rectangles...
        covering_rects = RectangleFiller.fill_grid(coords)
        #TODO REMOVE print("Got covering rectangles " + str(covering_rects))
        #Recalculate from these rectangles the screen rectangles to update against...
        screen_rects = []
        for (x_coord_min, y_coord_min, x_coord_max, y_coord_max) in covering_rects:
            screen_rects.append((PictureHandler.__MIN_X_COORD_SCREEN_CONVERSION[x_coord_min],
                                 PictureHandler.__MIN_Y_COORD_SCREEN_CONVERSION[y_coord_min],
                                 PictureHandler.__MAX_X_COORD_SCREEN_CONVERSION[x_coord_max],
                                 PictureHandler.__MAX_Y_COORD_SCREEN_CONVERSION[y_coord_max]))
        #TODO REMOVE print("Got screen update rectangles as " + str(screen_rects))
        #Got them all!
        return screen_rects
    
    @staticmethod
    def __update_surface_slab(surface,rect):
        '''
        Update a slab of the surface according to whatever needs to be drawn!
        @param surface: the surface everything should be drawn on
        @param rect: the rectangle on the original screen that the surface will be blitted to.
        Should be of the form (x_min,y_min,x_max,y_max)
        '''
        (x_min,y_min,x_max,y_max) = rect
        #Now work out everyone who needs to redraw...
        collided_rectangles = PictureHandler.__picture_rectangle_tree.collide_rectangle((x_min,y_min,x_max,y_max))
        #Gather them up, and order them by depth
        collided_list = []
        #TODO REMOVE print("Got collided rectangles " + str(collided_rectangles))
        for (_,_,_,_,drawer) in collided_rectangles:
            collided_list.append((drawer.get_depth(),drawer))
        #Sort by the first element only
        collided_list.sort(key=lambda tup: tup[0], reverse=True)
        #Now we call the redraw methods appropriately...
        for (_,drawer) in collided_list:
            #Redraw!
            drawer.redraw((x_min,y_min),surface)
        #That should be everything...
                       
    @staticmethod
    def _get_picture():
        '''
        Called by the screen when the picture needs to be drawn
        '''
        PictureHandler.__picture_lock.acquire()
        #Now we calculate the updates... (refills tree automatically atm)
        update_rects = PictureHandler.__calculate_screen_update_list()
        converted_update_list = [] #other form of rectangle...
        #Now collide the update rects to get the redrawing stuff...
        for (x_min,y_min,x_max,y_max) in update_rects:
            #Calculate the size of the surface we need
            (width,height) = (x_max-x_min,y_max-y_min)
            #Draw the background first...
            picture_slab = pygame.Surface((width,height))
            picture_slab = picture_slab.convert()
            picture_slab.fill(PictureHandler.__background_colour)
            #TODO REMOVE print("Made update slab with size " + str((width,height)))
            #Ready to perform the updates!!
            PictureHandler.__update_surface_slab(picture_slab,(x_min,y_min,x_max,y_max))
            #Finally, blit it to the picture and register the update...
            PictureHandler.__picture.blit(picture_slab,(x_min,y_min))
            #Should have worked I think...
            converted_update_list.append((x_min,y_min,width,height))
        #Return the relevant stuff...
        #TODO REMOVE print("Requesting screen updates on " + str(converted_update_list))
        return (PictureHandler.__picture,converted_update_list)
    
    @staticmethod
    def _picture_drawn():
        '''
        Called by the screen after the picture has been drawn successfully
        '''
        PictureHandler.__picture_lock.release()
        return
    
    @staticmethod
    def __deregister_drawer(drawer):
        '''
        Exactly the same as deregister_drawer - but does not acquire the synchronising lock
        You should not deregister twice.
        @param drawer: the drawer to deregister. Note that undoing any updates triggered
        is too complex to be worth the trouble...
        '''
        #Remove from the tree
        (x_min,y_min,x_max,y_max) = drawer.get_bounding_rectangle()
        PictureHandler.__picture_rectangle_tree.remove_rectangle((x_min,y_min,x_max,y_max,drawer))
        #Update the screen...
        PictureHandler.__add_to_screen(drawer)
    
    @staticmethod
    def register_drawer(drawer):
        '''
        Register a drawer object as wishing to draw on the screen. The rectangles
        should always cover the entire area that you might wish to draw on.
        You can use multiple rectangles to approximate shapes, although using too many
        is discouraged as it will slow down the processing speed (especially if they are regularly
        being re-registered and moved...)
        Rectangles should be of the form (x_min,y_min,width,height)
        You must not register twice!
        @param drawer: the drawer to register with the rectangles.
        '''
        #Now synchronise...
        PictureHandler.__picture_lock.acquire()
        #Add the key (the depth + drawer) to the rectangles...
        (x_min,y_min,x_max,y_max) = drawer.get_bounding_rectangle()
        #Add to the screen for the updates
        '''
        Note: this method doesn't need the key since it is
        calculating the screen update rectangles. These are separate rectangles.
        The rectangle passed in is not stored.
        '''
        PictureHandler.__add_to_screen(drawer)
        #Add to the picture handler's screen
        PictureHandler.__picture_rectangle_tree.insert_rectangle((x_min,y_min,x_max,y_max,drawer))
        #That should be everything..?
        PictureHandler.__picture_lock.release()
    
    @staticmethod
    def deregister_drawer(drawer):
        '''
        Deregister this drawer from the picture, meaning it will be erased in the next frame
        from the picture. Note that if this is called concurrently, you may be forced to draw
        again before deregistration completes as a lock may be held on the picture.
        @param drawer: the drawer to erase from the picture.
        @warning: you must have the same bounding rectangle, and the same inner collider
        and inner rectangles when you deregister, as you had when you previously registered.
        '''
        PictureHandler.__picture_lock.acquire()
        #We should call the auxiliary...
        PictureHandler.__deregister_drawer(drawer)
        PictureHandler.__picture_lock.release()
    