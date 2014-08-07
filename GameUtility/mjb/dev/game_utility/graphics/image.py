'''
Created on 12 May 2014

@author: michael
'''

import os
import pygame.transform

class Image(object):
    '''
    An image for this application. An image should be considered immutable. An image
    is really just a pygame surface.
    
    An image supports various transformations. Note that you should always aim to
    transform the original image rather than transforming a transformed image.
    
    For example, rotating an image 45 degrees by applying 45 one degree rotations
    would cause a huge loss in quality, where as a single 45 degree rotation would lose
    far less quality.
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
        @return: the colour key of this surface as (r,g,b).
        '''
        (r,g,b,_) = self.__surface.get_colorkey()
        return (r,g,b)
        
    def get_surface(self):
        '''
        This returns the actual surface of the image being drawn, allowing you to
        perform fancier transformations.
        You must not modify this surface. Most transformations return a new surface leaving
        the original surface untouched, so you can use those.
        @return: the surface containing the image to be drawn
        '''
        return self.__surface

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
        fullname = os.path.join(self.__directory, name)
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