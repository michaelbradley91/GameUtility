'''
Created on 25 Jul 2014

@author: michael
'''

from mjb.dev.game_utility.graphics.collisions.large_rectangle_tree import LargeRectangleTree
from mjb.dev.game_utility.graphics.collisions.small_rectangle_tree import SmallRectangleTree
from mjb.dev.game_utility.graphics.collisions.simple_rectangle_collider import SimpleRectangleCollider

class RectangleCollider(object):
    '''
    This class contains the static methods for determining the type of collider
    most suitable for a situation.
    This class is also the interface for any rectangle collider.
    '''
    
    #
    # Note to self: ideally the collide_rectangle method would be lazy, so that you could
    # get the first k rectangles collided against efficiently. However, this functionality
    # simply isn't needed at the moment anyway...
    #
    
    def insert_rectangle(self, rect):
        '''
        Insert a rectangle into the collider.
        @param rect: the rectangle to insert, which should have the form (x_min,y_min,x_max,y_max,key)
        where key is any custom value
        '''
        pass
    
    def remove_rectangle(self, rect):
        '''
        Remove a rectangle from the collider. Note that the key must also be equal
        to the key of the rectangle you wish to remove.
        @param rect: the rectangle to insert, which should have the form (x_min,y_min,x_max,y_max,key)
        where key is any custom value
        @return: true iff the rectangle was removed, since it was in the tree
        '''
        pass
    
    def collide_rectangle(self, rect):
        '''
        Collide a rectangle tree with the collider
        @param rect: the rectangle to collide against in the form of (x_min,y_min,x_max,y_max)
        @return: a list of all rectangles that collided with the given rectangle.
        '''
        pass
    
    def is_colliding(self,rect):
        '''
        Check if a rectangle is colliding with any rectangle inserted into the collider.
        (This is more efficient than using collide_rectangle(..)==[])
        @param rect: the rectangle to check for collisions with in the form of (x_min,y_min,x_max,y_max)
        @return: true iff some rectangle exists in the collider that is colliding
        '''
        pass
    
    def clear(self):
        '''
        Remove all rectangles from the collider
        '''
        pass

    def __init__(self, size):
        '''
        Construct a new rectangle collider with the specified screen size. For implementation
        reasons, certain types of collider have minimum size restrictions. See each class's
        static fields.
        @param size: the size of the screen as (width,height)
        '''
        pass
    
    #The boundaries for deciding which collider is best...
    SMALL = 10
    '''
    If the expected number of rectangles is <=SMALL, the simple rectangle collider will be used
    '''
    MEDIUM = 100
    '''
    If the expected number of rectangles is >SMALL and <=MEDIUM, the small rectangle tree will be used
    (Otherwise the large tree will be used)
    '''
    
    @staticmethod
    def get_recommended_collider(self,size,number_of_rectangles):
        '''
        Return the collider most suitable to handle the given size of screen
        and the (estimated) number of rectangles to be added
        @param size: the size of the screen for the collider to work with
        @param number_of_rectangles: the estimated number of rectangles to be added to this screen
        '''
        #Check the size...
        (width,height) = size
        if (number_of_rectangles<=RectangleCollider.SMALL):
            #The small collider will do
            return SimpleRectangleCollider(size)
        if (number_of_rectangles>RectangleCollider.SMALL
            and number_of_rectangles<=RectangleCollider.MEDIUM):
            #The small tree is appropriate
            if (SmallRectangleTree.MIN_WIDTH<=width or SmallRectangleTree.MIN_HEIGHT<=height):
                return SmallRectangleTree(size)
            return SimpleRectangleCollider(size)
        #The large tree is needed!
        if (LargeRectangleTree.MIN_WIDTH<=width or LargeRectangleTree.MIN_HEIGHT<=height):
            return LargeRectangleTree(size)
        if (SmallRectangleTree.MIN_WIDTH<=width or SmallRectangleTree.MIN_HEIGHT<=height):
            return SmallRectangleTree(size)
        return SimpleRectangleCollider(size)