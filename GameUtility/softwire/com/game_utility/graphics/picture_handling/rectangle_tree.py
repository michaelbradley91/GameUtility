'''
Created on 5 Jul 2014

@author: michael
'''

class RectangleTree(object):
    '''
    The rectangle tree is designed to store rectangles, and check for intersections between the stored
    rectangle and another rectangle as efficiently as possible. It is specifically designed for fixed
    width/height screens.
    
    By rectangle, we actually mean a tuple of the form:
    (x_min, y_min, x_max, y_max, key)
    
    where the key is arbitrary and for the user only.
    '''

    def __init__(self, size):
        '''
        Construct a new rectangle tree, designed to cover coordinates ranging from (0,0) to (x,y) for
        (x,y) = size.
        @param size: the size of the space spanned by the rectangle tree
        '''
        self.__size = size
        
    def insert_rectangle(self, rect):
        '''
        This adds a rectangle to the tree. Note that if the rectangle falls outside
        the size of the grid, it will effectively be clipped. The call will then have no effect
        if the whole of the rectangle lies outside the grid
        @param rect: the rectangle to add to the rectangle tree
        '''
        
    def remove_rectangle(self, rect):
        '''
        Remove a rectangle from the tree. This has no effect if the exact rectangle given does not exist in the
        tree.
        @param rect: the rectangle to remove from the tree.
        '''
    
    def collide_rectangle(self, rect, remove=False):
        '''
        @param rect: the rectangle to check for collisions against.
        @param remove: whether or not the returned rectangles should also be removed from the structure.
        @return: all of the rectangles strictly colliding (overlapping by at least one pixel) with the given rect.
        '''
        