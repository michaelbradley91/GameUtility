'''
Created on 1 Aug 2014

@author: michael
'''

from mjb.dev.game_utility.collisions.rectangle_collider_picker import RectangleColliderPicker

class ShapeCalculator(object):
    '''
    A shape calculator must be able to calculate a representation of its shape as a list
    of rectangles according to various levels of precision.
    
    Any shape calculator holds a bounding rectangle, covering the whole shape. This bounding rectangle's
    top left coordinate should be sensitive to where it is positioned on screen.
    
    The shape calculator's other method (calculate shape), returns rectangles more closely
    representing this shape - how closely depends on the precision. These rectangles assume
    the shape is rooted at (0,0) and should fit entirely within the bounding rectangle.
    '''

    def __init__(self):
        '''
        Construct a new shape calculator (use whatever constructor you want)
        '''
        pass
    
    def is_immutable(self):
        '''
        @return: true iff this shape calculator is immutable. Immutability provides a few technical
        advantages.
        '''
    
    def get_bounding_rectangle(self):
        '''
        @return: a single rectangle covering the whole shape in the form of (x_min,y_min,x_max,y_max)
        '''
    
    def calculate_shape(self,precision,include_collider=True):
        '''
        @param precision: the precision to which the shape should be calculated. Treat None as the lowest
        possible precision, and so should usually return the bounding rectangle. A value
        of 1 should be pixel perfect, and higher values are less precise.
        @param include_collider: will be true iff a collider for the shape should also be returned
        @return: a tuple pair as (rectangle_list,collider). Note that if include_collider=False, collider
        will be None. The rectangle list will be a list of rectangles covering at least the entire
        shape rooted at (0,0) unlike the bounding rectangle. All of the rectangles in this list
        should fit within the bounding rectangle (if it were rooted at (0,0)), and each rectangle will have the form
        (x_min,y_min,x_max,y_max). If the collider is included, it will include exactly those rectangles (with None keys)
        '''
        pass
    
    @staticmethod
    def calculate_default_collider(bounding_rectangle_size,rectangle_list):
        '''
        @param bounding_rectangle_size: the (width,height) of the bounding rectangle
        @param rectangle_list: the list of rectangles generated by calculate shape
        @return: a collider optimised to contain the given rectangles.
        '''
        #This method is here for convenience and to remove some duplication...
        collider = RectangleColliderPicker.get_recommended_collider(bounding_rectangle_size, len(rectangle_list))
        #Insert the rectangles...
        for (x_min,y_min,x_max,y_max) in rectangle_list:
            collider.insert_rectangle((x_min,y_min,x_max,y_max,None))
        return collider