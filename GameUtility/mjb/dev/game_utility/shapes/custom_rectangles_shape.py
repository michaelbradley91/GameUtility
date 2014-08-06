'''
Created on 6 Aug 2014

@author: michael
'''

from mjb.dev.game_utility.shapes.shape import Shape

class CustomRectanglesShape(Shape):
    '''
    This class allows you to construct a shape from a "user supplied" list of rectangles.
    This is intended to enable users to override the default calculated shapes from images
    (although the calculated shape is often quite good...)
    '''

    def __init__(self, rect_list):
        '''
        Construct a new shape from the given list of rectangles. The shape will calculate the
        size for you, and will return just the bounding rectangle for "None" precision.
        For any other precision, it will return exactly your rectangle list.
        @param rect_list: a list of rectangles of the form (x_min,y_min,width,height)
        @note: the rectangles should treat the top left of the shape as (0,0)
        '''
        #Do not need a cache for this...
        Shape.__init__(self, cache_depth=0)
        #Conver the rectangle list
        converted_rect_list = []
        for (x_min,y_min,width,height) in rect_list:
            converted_rect_list.append((x_min,y_min,x_min+width,y_min+height))
        #Figure out our size...
        largest_x_max = converted_rect_list[0][2]
        largest_y_max = converted_rect_list[0][3]
        for (_,_,x_max,y_max) in converted_rect_list:
            if x_max>largest_x_max:
                largest_x_max = x_max
            if y_max>largest_y_max:
                largest_y_max = y_max
        #The bounding rectangle has been decided!!
        self.__size = (largest_x_max,largest_y_max)
        #Make the collider
        self.__collider = Shape.calculate_default_collider(self.__size, converted_rect_list)
        self.__rect_list = converted_rect_list
    
    def _calculate_shape_to_override(self,precision,include_collider):
        '''
        This method's intended behaviour is identical to calculate shape's except this
        is meant to be overridden.
        '''
        return (self.__rect_list,self.__collider)
    
    def get_size(self):
        '''
        (You should override this)
        @return: the size of this shape as (width,height) as needed by shape handlers to form
        the bounding rectangle
        '''
        return self.__size
        