'''
Created on 25 Jul 2014

@author: michael
'''

class RectangleCollider(object):
    '''
    This class is the interface for any rectangle collider.
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
    
    