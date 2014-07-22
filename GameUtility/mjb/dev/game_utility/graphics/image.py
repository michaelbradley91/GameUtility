'''
Created on 12 May 2014

@author: michael
'''

import os
import pygame.transform

class Image(object):
    '''
    An image for this application. An image should be considered immutable.
    An image supports rotation and scaling transformations. However, you should
    use an image drawer's methods for basic transformations to preserve the quality of the
    image*.
    
    *It is better to apply the full series of transformations all at once to
    the original image (loaded from your machine) than to apply many little transformations,
    because each one reduces the image quality. An image drawer will handle this for you!
    
    TODO: I suppose if you want to be really fancy, it would be cool
    if we could make child and parent images, so that the transformations are applied
    across all images in a group. Might confuse the drawer pretty badly though...
    Will leave that until much later...
    
    TODO: note to self - should be possible to flip colliding rectangles etc
    as well to avoid a recalculation. (Not feasible for rotations or scaling
    due to likely implementation disagreements in rounding or bugs...).
    '''
    def __init__(self, surface):
        '''
        Construct a new image
        @param surface: the surface containing the image to be blitted to the screen.
        '''
        self.__surface = surface
    
    def scale(self, new_width, new_height):
        '''
        Scale the image to the given size
        @param new_width: the width of the new scaled image
        @param new_height: the height of the new scaled image
        @return: a new transformed image
        '''
        return Image(pygame.transform.scale(self.__surface,(new_width,new_height)))
    
    def rotate(self, degrees, is_clockwise=True):
        '''
        Rotate the image by the given number of degrees (sorry rads - believe this is more
        intuitive). Clockwise is the default direction of rotation.
        @param degrees: the number of degrees to turn this image by. (Negatives allowed)
        @param is_clockwise: True by default, and should true iff you wish to rotate the image
        clockwise.
        @return: a new transformed image
        '''
        if is_clockwise:
            return Image(pygame.transform.rotate(self.__surface,-1 * degrees))
        else:
            return Image(pygame.transform.rotate(self.__surface,degrees))
    
    def flip(self,is_vertical=False):
        '''
        Flip this image either horizontally or vertically. (Flipping vertically means M becomes W)
        Horizontal flip by default
        @param is_vertical: should be false iff you wish to flip vertically. (False by default)
        @return: a new image flipped along the right axis.
        '''
        return Image(pygame.transform.flip(self.__surface,not is_vertical,is_vertical))
    
    def get_size(self):
        '''
        @return: the size of the image (in terms of the surface it has been attached to)
        as (width,height)
        '''
        return self.__surface.get_size()
    
    def get_colour_key(self):
        '''
        @return: the colour key of this surface. (You should not change this!
        Not sure what you need it for..?)
        '''
        return self.__surface.get_colorkey()
        
    def _get_surface(self):
        '''
        This returns the actual surface of the image being drawn, allowing you to
        perform fancier transformations. This is discouraged - the actions provided
        to you in this class were chosen carefully.
        If you do use this, you must not modify this surface instance itself. Once
        you have the new surface, you can create a new image object like this to use elsewhere
        in the application.
        @return: the surface containing the image to be drawn
        '''
        return self.__surface
    
    def _calculate_rectangle_approximation(self, precision=None):
        '''
        Seems like an obscure method, but it is really useful! This will calculate
        a list of rectangles fully covering the image, with a particular precision.
        This respects the colour key of the image only. Pixel alphas are not supported at
        the moment.
        TODO: support pixel alphas? Probably surface alphas at least. Imagine we could enforce
        that.
        @param precision: will treat the sprite as a grid of precision*precision squares
        and then cover the (partially) occupied squares with rectangles.
        Default None will return a single rectangle (fast). Precision of one is pixel perfect.
        '''
        pass

class ImageLoader(object):
    '''
    The image loader manages the loading of images into pygame.
    Note that you should not load an image into the game more than once,
    unless you have so many that some must be forgotten for memory reasons...
    '''
    
    def __init__(self,directory):
        '''
        Construct a new image loader using the given directory. (This can be set freely afterwards)
        @param directory: a directory where images should be loaded from by this loader. Default ""
        '''
        self.__directory = directory
    
    def load_image(self,name, colourkey=None):
        '''
        Load an image with the given name into pygame.
        @param name: the name of the file after the image directory
        @param colourKey: the colour that should appear transparent in the image
        None by default meaning no colour will appear transparent
        @return: the image (as in this file!)
        '''
        fullname = os.path.join(self.directory, name)
        try:
            surface = pygame.image.load(fullname)
        except pygame.error, message:
            print("Does this image exist (otherwise permissions or memory)? Cannot load image at: " + fullname)
            raise SystemExit, message
        surface = surface.convert()
        if colourkey is not None:
            surface.set_colorkey(colourkey, pygame.locals.RLEACCEL)
        return Image(surface)
    
    def get_directory(self):
        '''
        @return: the directory that this loader is loading images from.
        '''
        return self.__directory
    
    def set_directory(self,directory):
        '''
        @param directory: the directory this loader should now load from (convenience method)
        '''
        self.__directory = directory