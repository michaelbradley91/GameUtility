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
    
    @staticmethod
    def initialise():
        '''
        Initialise the picture handler. This should be done strictly after the screen has been
        initialised, and strictly before any requests are made to the picture handler.
        This should only be called once
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
        #Remember we did this!
        PictureHandler.__initialised = True
        
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
    