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
'''

import softwire.com.game_utility.graphics.screen as screen
import pygame
import threading
import collections
import softwire.com.game_utility.graphics.picture_handling.rectangle_tree as rectangle_tree
import softwire.com.game_utility.graphics.picture_handling.rectangle_filler as rectangle_filler

class Drawer(object):
    '''
    This class is an interface for an object which wishes to draw itself into the picture
    '''
    
    def __init__(self):
        '''
        A constructor which does nothing
        '''
        pass
    
    def redraw(self, top_left, surface):
        '''
        Called by the picture handler when this object needs to redraw itself
        on the surface provided.
        @param top_left: the top left coordinate of the surface as it will be blitted to the screen
        @param surface: the surface to drawn on. Other than drawing itself, the surface should
        not be tampered with. Get the clip area to see the rectangle in which the drawing is
        actually occurring if you can exploit that for efficiency.
        '''
        pass

class _DummyPictureHandler(screen._PictureHandler):
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
    
    #This is a unique identifier associated to each drawer, it ensures that items
    #will be drawn in a consistent order.
    __unique_id = 0L
    
    #The number of width divisions along the screen
    __WIDTH_DIVISION = 32;
    #The number of height divisions along the screen
    __HEIGHT_DIVISION = 16;
    
    #The list of rectangles to fill the screen rectangle tree
    __SCREEN_RECTANGLES = []
    
    #Storing the conversion back to the screen coordinates
    __MIN_X_COORD_SCREEN_CONVERSION = collections.defaultdict(lambda:0)
    __MAX_X_COORD_SCREEN_CONVERSION = collections.defaultdict(lambda:0)
    __MIN_Y_COORD_SCREEN_CONVERSION = collections.defaultdict(lambda:0)
    __MAX_Y_COORD_SCREEN_CONVERSION = collections.defaultdict(lambda:0)
    
    #The screen rectangle tree
    __screen_rectangle_tree = None
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
        PictureHandler.__background_colour = screen.Screen.get_background_colour()
        PictureHandler.__size = screen.Screen.get_screen_size()
        #Initialise the picture
        PictureHandler.__picture = pygame.Surface(PictureHandler.__size)
        PictureHandler.__picture = PictureHandler.__picture.convert()
        PictureHandler.__picture.fill(PictureHandler.__background_colour)
        #Assign self as the picture handler
        screen.Screen.set_picture_handler(PictureHandler.__handler)
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
        width_dividers = collections.defaultdict(lambda:0)
        width_division = screen_width / width_div
        for i in range(0,width_div):
            width_dividers[i] = i * width_division
        for i in range(0,screen_width % width_div): #the remainder
            width_dividers[width_div-(1+i)] = width_dividers[width_div-(1+i)] + (screen_width % width_div) - i
        #Repeat for the height
        height_dividers = collections.defaultdict(lambda:0)
        height_division = screen_height / height_div
        for i in range(0,height_div):
            height_dividers[i] = i * height_division
        for i in range(0,screen_height % height_div): #the remainder
            height_dividers[height_div-(i+1)] = height_dividers[height_div-(i+1)] + (screen_height % height_div) - i
        #For convenience:
        width_dividers[width_div] = screen_width #plus one because we consider being >= to be in the sector
        height_dividers[height_div] = screen_height
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
            PictureHandler.__MIN_X_COORD_SCREEN_CONVERSION[x] = width_dividers[x]
            PictureHandler.__MAX_X_COORD_SCREEN_CONVERSION[x] = width_dividers[x+1]
        for y in range(0,height_div):
            PictureHandler.__MIN_Y_COORD_SCREEN_CONVERSION[y] = height_dividers[y]
            PictureHandler.__MAX_Y_COORD_SCREEN_CONVERSION[y] = height_dividers[y+1]
        #Fill the tree
        PictureHandler.__screen_rectangles_to_add = PictureHandler.__SCREEN_RECTANGLES
        PictureHandler.__screen_rectangle_tree = rectangle_tree.RectangleTree(PictureHandler.__size)
        #Fill it
        PictureHandler.__fill_screen_tree()
        
    @staticmethod
    def __fill_screen_tree():
        '''
        Fill the rectangle tree for the screen (not the images)
        '''
        for rect in PictureHandler.__screen_rectangles_to_add:
            PictureHandler.__screen_rectangle_tree.insert_rectangle(rect)
        #Really simple
    
    @staticmethod
    def __add_to_screen(rect):
        '''
        Add a given rectangle to the screen
        @param rect: the rectangle to add in the form of (x_min, y_min, x_max, y_max)
        '''
        (x_min,y_min,x_max,y_max) = rect
        #Add a dummy key
        rect = (x_min,y_min,x_max,y_max,None)
        #Add the rectangle to the screen rectangle tree by colliding it first
        collided_rects = PictureHandler.__screen_rectangle_tree.collide_rectangle(rect)
        #Now remove the collided rectangles
        for rect in collided_rects:
            was_removed = PictureHandler.__screen_rectangle_tree.remove_rectangle(rect)
            if was_removed:
                PictureHandler.__screen_rectangles_to_add.append(rect)
        #Done!
        
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
        #Firstly, gather the coordinates and update the screen rectangle tree...
        coords = []
        for rect in PictureHandler.__screen_rectangles_to_add:
            (_,_,_,_,(x,y)) = rect
            coords.append((x,y))
            #Now fill the rectangle tree again
            PictureHandler.__screen_rectangle_tree.insert_rectangle(rect)
        #Empty the update list
        PictureHandler.__screen_rectangles_to_add = []
        #Calculate the covering rectangles...
        covering_rects = rectangle_filler.RectangleFiller.fill_grid(coords)
        #Recalculate from these rectangles the screen rectangles to update against...
        screen_rects = []
        for (x_coord_min, y_coord_min, x_coord_max, y_coord_max) in covering_rects:
            screen_rects.append(PictureHandler.__MIN_X_COORD_SCREEN_CONVERSION[x_coord_min],
                                PictureHandler.__MAX_X_COORD_SCREEN_CONVERSION[x_coord_max],
                                PictureHandler.__MIN_Y_COORD_SCREEN_CONVERSION[y_coord_min],
                                PictureHandler.__MAX_Y_COORD_SCREEN_CONVERSION[y_coord_max],
                                None)
        #Got them all!
        return screen_rects
                       
    @staticmethod
    def _get_picture():
        '''
        Called by the screen when the picture needs to be drawn
        '''
        PictureHandler.__picture_lock.acquire()
        return PictureHandler.__picture
    
    @staticmethod
    def _picture_drawn():
        '''
        Called by the screen after the picture has been drawn successfully
        '''
        PictureHandler.__picture_lock.release()
        
        return
    
    @staticmethod
    def register_rectangles(drawer, rectangles, depth):
        '''
        Register a drawer object as wishing to draw on the screen. The rectangles
        should always cover the entire area that you might wish to draw on.
        You can use multiple rectangles to approximate shapes, although using too many
        is discouraged as it will slow down the processing speed (especially if they are regularly
        being re-registered and moved...)
        @param drawer: the drawer to register with the rectangles.
        @param rectangles: a list of rectangles covering the area the drawer might draw in.
        @param depth: the depth of this object in the picture. Objects with a greater
        depth value will appear behind objects with a smaller depth value. Negative values
        are allowed, and the background colour will always be drawn behind all objects.
        '''
        pass
    
    @staticmethod
    def deregister_rectangles(drawer):
        '''
        Deregister this drawer from the picture, meaning it will be erased in the next frame
        from the picture. Note that if this is called concurrently, you may be forced to draw
        again before deregistration completes as a lock may be held on the picture.
        @param drawer: the drawer to erase from the picture.
        '''
        pass
    