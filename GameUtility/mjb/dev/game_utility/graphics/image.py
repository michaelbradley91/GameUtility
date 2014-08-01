'''
Created on 12 May 2014

@author: michael
'''

import os
import pygame.transform
import mjb.dev.game_utility.utility.rectangle_filler as rectangle_filler

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
        @return: the colour key of this surface as (r,g,b). (You should not change this!
        Not sure what you need it for..?)
        '''
        (r,g,b,_) = self.__surface.get_colorkey()
        return (r,g,b)
        
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
        
        Note: if the entity is entirely transparent, there is a "feature". Any non-trivial
        precision will return no rectangles at all, but the default simple one
        will return the entire object... I don't know why you would have an image that is
        genuinely invisible (especially since drawers have visibility settings) but that's
        what would happen. Accounting for this case is expensive so I've ignored it.
        
        TODO: support pixel alphas? Probably surface alphas at least. Imagine we could enforce
        that.
        @param precision: will treat the sprite as a grid of precision*precision squares
        and then cover the (partially) occupied squares with rectangles.
        Default None will return a single rectangle (fast). Precision of one is pixel perfect.
        
        @return: the list of covering rectangles in the form of (x_min,y_min,x_max,y_max)
        '''
        if precision!=None and precision<1:
            raise ValueError("The precision for an image cannot be negative. Received value " + str(precision))
        (width,height) = self.__surface.get_size()
        #OK! First take care of the special case..
        if precision==None:
            return (0,0,width,height)
        colour_key = self.get_colour_key()
        #For the non-trivial precision, calculate which rectangles
        #are occupied and which are not...
        occupied_coords = []
        for x in range(0,((width-1)/precision)+1):
            for y in range(0,((height-1)/precision)+1):
                #Note that the screen pixels are from 0 to width-1 and 0 to height-1
                #Decide if this is an occupied square...
                is_empty = True
                x_mod = 0
                y_mod = 0
                while is_empty and y_mod<precision:
                    #Figure out the pixel coordinates...
                    x_pixel = (x * precision) + x_mod
                    y_pixel = (y * precision) + y_mod
                    if (x_pixel>=width):
                        #Skip...
                        x_mod = 0
                        y_mod+=1
                        continue
                    if (y_pixel>=height):
                        break #quit the loop
                    #The pixel fits in the surface
                    (r,g,b,_) = self.__surface.get_at((x_pixel,y_pixel))
                    if (r,g,b)!=colour_key:
                        #It is not empty!
                        is_empty = False
                    #Update the coordinates
                    if x_mod==precision-1:
                        y_mod+=1
                        x_mod=0
                    else:
                        x_mod+=1
                #See if it is empty
                if not is_empty:
                    #Add to the coordinates...
                    occupied_coords.append((x,y))
        #Now fill the rectangle...
        rects = rectangle_filler.RectangleFiller.fill_grid(occupied_coords)
        print("Got occupied coords " + str(occupied_coords))
        print("Got fill " + str(rects))
        #Convert the rectangles back...
        converted_coords = []
        for (x_min,y_min,x_max,y_max) in rects:
            converted_coords.append((x_min * precision,
                                     y_min * precision,
                                     min((x_max+1) * precision,width),
                                     min((y_max+1) * precision,height)))
        return converted_coords

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