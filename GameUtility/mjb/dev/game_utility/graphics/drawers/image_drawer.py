'''
Created on 22 Jul 2014

@author: michael
'''

class ImageDrawer(object):
    '''
    This class allows you to draw images onto the screen!
    
    TODO: worry about transformations!
    
    Note that creating an image is like loading the image. You should do this as infrequently
    as possible. Some things to avoid are:
    
    1. LOADING THE SAME IMAGE TWICE: seriously - you never need to do that...
    2. Enabling collision detection on an image which stretches and/or rotates.
    
    Collision detection - especially fine collision detection against the image
    if you are using an automated form, is exceedingly expensive. The automated
    collision detector must map the image to a list of rectangle approximations
    each time it is transformed. Doing this once when the image is initialised is ok,
    and typically you'd do this before the game begins to avoid hurting the FPS.
    However, doing it every time an image is transformed is expensive.
    
    Screen drawing - if high precision is given when the image is drawn, it is also strongly
    discouraged to transform. See the initialisation method for details. The default
    will usually be best.
    
    TODO: REMOVE this
    It is possible to rotate, stretch, rotate etc and get a different result
    compared to any form of rotation followed by stretch (or vice versa).
    As in, the order of transformations is important...
    
    This could be too complex. I could restrict the user to full scale or rotations,
    and never more than these.
    
    TODO: THOUGHT:
    
    we could use inheritance to manage the collision settings. It is a lot for one class
    to consider transformations, rotations, screen drawing precision etc as well as collisions.
    Probably a good idea... 
    '''
    
    '''
    Use this value if precision in redrawing could be useful. This is only helpful for large
    images. See the init method of this class for details...
    '''
    SCREEN_DRAW_PRECISE = 8
    '''
    Use this value if the image is small (matches the default value atm)
    or otherwise has few hollow regions.
    '''
    SCREEN_DRAW_NO_PRECISION = None
    
    def __init__(self, image, top_left, visible=True, screen_draw_precision=None):
        '''
        @param image: the image to be drawn by this object. Note that the image
        should be the surface returned by the image loader.
        @param top_left: the top left coordinate where this image should appear on screen, as (x,y)
        @param visible: default True, determines whether or not the image should appear
        on screen.
        @param screen_draw_precision: default None, determines when the image is redrawn*
        
        *This is a technical setting but not tooooo... hard to understand. As images pass over
        each other, they have to be redrawn to ensure that images appear in the correct order
        on screen. The screen precision determines when this should happen.
        
        All images are approximated by rectangles internally (not in appearance),
        and if these rectangles are touched by another image, it will trigger this image to
        redraw.
        
        Approximating an image by a single rectangle is fine for small images,
        as the redraw method will only be called unnecessarily very rarely. This is faster
        than using many rectangles for more precise detection.
        
        However, for large objects like a lamp post, very little of the lamp post will actually
        cover its rectangle, due to the overhanging light. Hence, it would be better
        to approximate this by two rectangles. This is faster since it will be redrawn
        less often (even though the additional rectangle incurs a larger overhead).
        
        screen_draw_precision determines how the approximating rectangles are generated.
        A value of None is cheapand usually fast - using one big rectangle.
        A value of 1 will cover the image with pixel perfect precision, which I'd never
        recommend as it is often very slow for "rough" edges etc (or evil circles)
        A value of "x" will treat the image as a grid of x*x squares, with a square
        considered occupied if any pixel in the image occupies it. These squares
        will then be covered by rectangles kept as "large as possible" (heuristically
        for speed) and will form the approximation for an image. Thus, large x will ignore
        small imperfections in "straight" edges more or less, and use far less rectangles.
        
        Use the class constants for recommended values. Typically, x=8 is ok for special
        cases which care about the precision, but x=None is the default since it is faster.
        '''
        pass
    
    def set_current_root_image(self, image):
        '''
        Set the current image this object should use. Note that
        it is advised you use a root image, since if you pass a transformed image and
        transform again, you'll start to lose quality.
        @param image: the image to store.
        '''
        pass
        
    def get_current_image(self):
        '''
        @return: the image as it is being drawn now. It is generally
        no advised to try modifying this!
        '''
        pass
    
    def get_current_root_image(self):
        '''
        @return: the image for this object. The root image
        is the image as it was loaded from your machine - in other words before transformations
        have been applied. To avoid losing quality, it is best to apply all transformations
        to the root image, so it is best to pass this around if sharing...
        '''
        pass
    
    def save_current_image_data(self):
        '''
        Save the current image data in memory. This is useful for storing transformations
        of the image on the fly. This is in RAM, so don't do it too often
        (this does not write to a file or anything).
        If a transformation of an image is stored in RAM, and that transformation
        is needed again, it will be loaded much more quickly! (Along with
        collision stuff probably...not implemented yet).
        It is not worth doing if the image is never transformed.
        
        @return: a key representing what was saved. It is saved statically
        so all drawers can access this saved image.
        '''
        pass
    
    @staticmethod
    def forget_image_data(key):
        '''
        Forget a saved image. This is important for freeing up memory.
        @param key: the key that was received when the image was saved. (Keep it!)
        '''
        pass
    
    @staticmethod
    def forget_all_image_data():
        '''
        Forget all of the saved image data. This is quite brutal, but useful
        if you lost your keys!
        (It is a lot faster than iterating over all the keys though).
        If you don't know what I mean by keys, hopefully you didn't save any images,
        in which case there is nothing to forget. Images are not saved like
        this by default.
        '''
        pass
        