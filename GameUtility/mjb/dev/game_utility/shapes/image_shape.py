'''
Created on 7 Aug 2014

@author: michael
'''

from mjb.dev.game_utility.shapes.shape import Shape
from mjb.dev.game_utility.utility.rectangle_filler import RectangleFiller
from mjb.dev.game_utility.collisions.rectangle_collider_picker import RectangleColliderPicker

class ImageShape(Shape):
    '''
    This class will accept an image (which you should never modify) and construct
    a shape from that image. The image here is intended to be an image as defined in the graphics
    package.
    '''

    def __init__(self, image, cache_depth=2):
        '''
        Construct a new shape from the given image. The image should never be modified
        directly (i.e.: it should be immutable). This is why operations on images always
        create new images.
        @param image: the image to create a shape from.
        @param cache_depth: how many calculations to save for this image. The calculation
        for an image at high precision is quite expensive, so it is recommended that you make
        use of the cache. Default 2
        '''
        Shape.__init__(self, cache_depth)
        #Save the pygame surface (do not need the rest)
        self.__image = image
        self.__surface = image.get_surface()
        self.__size = self.__surface.get_size()
    
    def _calculate_shape_to_override(self,precision,include_collider):
        '''
        This method's intended behaviour is identical to calculate shape's except this
        is meant to be overridden.
        '''
        (width,height) = self.__size
        colour_key = self.__image.get_colour_key()
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
        rects = RectangleFiller.fill_grid(occupied_coords)
        #Convert the rectangles back...
        converted_coords = []
        for (x_min,y_min,x_max,y_max) in rects:
            converted_coords.append((x_min * precision,
                                     y_min * precision,
                                     min((x_max+1) * precision,width),
                                     min((y_max+1) * precision,height)))
        #Now create a collider if appropriate...
        if include_collider:
            collider = RectangleColliderPicker.get_recommended_collider(self.__size, len(converted_coords))
            for (x_min,y_min,x_max,y_max) in converted_coords:
                collider.insert_rectangle((x_min,y_min,x_max,y_max,None))
        else:
            collider = None
        #Return the result!
        print("Used this many rectangles: " + str(len(converted_coords)))
        return (converted_coords,collider)
    
    def get_size(self):
        '''
        (You should override this)
        @return: the size of this shape as (width,height) as needed by shape handlers to form
        the bounding rectangle
        '''
        return self.__size
    
    def get_image(self):
        '''
        @return: the image held in this image shape
        '''
        return self.__image