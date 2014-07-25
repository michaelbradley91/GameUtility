'''
Created on 25 Jul 2014

@author: michael
'''

import mjb.dev.game_utility.graphics.collisions.rectangle_collider as collider

class SimpleRectangleCollider(collider.RectangleCollider):
    '''
    This class is the simplest version of the rectangle collider, for the smallest
    screens and the lowest overheads.
    '''

    def __init__(self, size):
        '''
        Construct a new rectangle collider with the given size
        @param size: the size of the screen to collide in as (width,height)
        '''
        (width,height) = size
        self.__width = width
        self.__height = height
        #The rectangle list
        self.__list = []
        
    def insert_rectangle(self, rect):
        '''
        Insert a rectangle into the collider.
        @param rect: the rectangle to insert, which should have the form (x_min,y_min,x_max,y_max,key)
        where key is any custom value
        '''
        if not self.__is_inside_screen(rect):
            return
        #Add to the list
        self.__list.append(rect)
    
    def remove_rectangle(self, rect):
        '''
        Remove a rectangle from the collider. Note that the key must also be equal
        to the key of the rectangle you wish to remove.
        @param rect: the rectangle to insert, which should have the form (x_min,y_min,x_max,y_max,key)
        where key is any custom value
        @return: true iff the rectangle was removed, since it was in the tree
        
        '''
        if not self.__is_inside_screen(rect):
            return
        #Remove from the list
        if rect in self.__list:
            self.__list.remove(rect)
            return True
        else:
            return False
    
    def collide_rectangle(self, rect):
        '''
        Collide a rectangle tree with the collider
        @param rect: the rectangle to collide against in the form of (x_min,y_min,x_max,y_max)
        @return: a list of all rectangles that collided with the given rectangle.
        '''
        (x_min,y_min,x_max,y_max) = rect
        if not self.__is_inside_screen((x_min,y_min,x_max,y_max,None)):
            return []
        #Find all the colliding rectangles...
        res = []
        for (rect_x_min, rect_y_min, rect_x_max, rect_y_max, key) in self.__list:
            if rect_x_min<x_max and rect_x_max>x_min and rect_y_min<y_max and rect_y_max>y_min:
                res.append((rect_x_min, rect_y_min, rect_x_max, rect_y_max, key))
        return res
    
    def is_colliding(self,rect):
        '''
        Check if a rectangle is colliding with any rectangle inserted into the collider.
        (This is more efficient than using collide_rectangle(..)==[])
        @param rect: the rectangle to check for collisions with in the form of (x_min,y_min,x_max,y_max)
        @return: true iff some rectangle exists in the collider that is colliding
        '''
        (x_min,y_min,x_max,y_max) = rect
        if not self.__is_inside_screen((x_min,y_min,x_max,y_max,None)):
            return False
        #Find the first colliding rectangle
        for (rect_x_min, rect_y_min, rect_x_max, rect_y_max, _) in self.__list:
            if rect_x_min<x_max and rect_x_max>x_min and rect_y_min<y_max and rect_y_max>y_min:
                return True
        return False
        
    def clear(self):
        '''
        Remove all rectangles from the collider
        '''
        self.__list = []
    
    def __is_inside_screen(self, rect):
        '''
        @param rect: the rectangle to check
        @return: true iff the rectangle is actually inside the screen (at least in part)
        Also catches zero width or zero height
        '''
        (x_min, y_min, x_max, y_max, _) = rect
        return x_max>0 and y_max>0 and x_min<self.__width and y_min<self.__height and x_max!=x_min and y_max!=y_min
        
    
    