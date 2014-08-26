'''
Created on 26 Aug 2014

@author: michael
'''

import collections

class DynamicCollider(object):
    '''
    This class is designed to act as a rectangle collider. It will use the new angled and scaled
    rectangles in its construction, and will grow dynamically.
    
    The growth is not entirely memory free. A new index will be added every 120 pixels any object shifts
    in the outer 4 indices.
    A set will exist for each level of recursion in these outer 4, specifying the indices that are occupied.
    Then, during a range search, you will only search among these indices.
    
    The "infinite" (as much as memory permits) range will be implemented using a defaultdict (shared between
    levels). The set will make range traversal feasible, and this ensures the memory consumed
    is linear in the number of items added.
    
    Note: if the default dict is not fast enough, a list will probably work quickly enough
    in practice.
    '''

    def __init__(self):
        '''
        Construct a new dynamic collider! Note that there are no parameters!
        '''
        #The base default dict. It is really just one for better performance
        #NOTE: is this really better? Might slow down individual look ups... It's a dynamic hash table...
        #shouldn't gget too much worse...
        self.root = collections.defaultdict(lambda:[])
    
    def insert_rectangle(self, angled_rect):
        '''
        Insert an angled rectangle into the collider.
        @param rect: the rectangle to insert, which should have the form (x_min,y_min,x_max,y_max,key)
        where key is any custom value
        '''
        pass
    
    def remove_rectangle(self, angled_rect):
        '''
        Remove an angled rectangle from the collider. Note that the key must also be equal
        to the key of the rectangle you wish to remove.
        @param rect: the rectangle to insert, which should have the form (x_min,y_min,x_max,y_max,key)
        where key is any custom value
        @return: true iff the rectangle was removed, since it was in the tree
        '''
        pass
    
    def collide_rectangle(self, angled_rect, touching=False):
        '''
        Collide an angled rectangle with all rectangles in the collider
        @param rect: the rectangle to collide against in the form of (x_min,y_min,x_max,y_max)
        @param touching: False by default. If True, returns rectangles which are only touching as well.
        @return: a list of all rectangles that collided with the given rectangle.
        '''
        pass
    
    def is_colliding(self, angled_rect, touching=False):
        '''
        Check if an angled rectangle is colliding with any rectangle inserted into the collider.
        (This is more efficient than using collide_rectangle(..)==[])
        @param rect: the rectangle to check for collisions with in the form of (x_min,y_min,x_max,y_max)
        @param touching: False by default. If True, returns true if a rectangle is only touching as well.
        @return: true iff some rectangle exists in the collider that is colliding
        '''
        pass
    
    def clear(self):
        '''
        Remove all rectangles from the collider
        '''
        pass
