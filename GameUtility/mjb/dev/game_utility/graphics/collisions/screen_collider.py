'''
Created on 27 Jul 2014

@author: michael
'''

class ScreenCollider(object):
    '''
    The screen collider is designed to provide "screen" sized (it is still a parameter)
    collision detection automatically. It expects recursive collisions to be applied,
    which means that a single rectangle is attached to the screen collider first,
    and then inside this rectangle is a list of further rectangles. This enables faster
    addition and deletion.
    '''
    
    '''
    The minimum width of the screen that this tree supports
    '''
    MIN_WIDTH = 16
    '''
    The minimum height of the screen that this tree supports
    '''
    MIN_HEIGHT = 16
    
    def __init__(self,rectangle_collider,get_inner_rectangles, get_inner_collider):
        '''
        Create a new screen collider!
        @param rectangle_collider: the rectangle collider to be used for the outer rectangles
        @param get_inner_rectangles: return a list of all the inner rectangles as a list of (x_min,y_min,x_max,y_max). Should return [] if there are none, and accept a rectangle with the key as a parameter
        @param get_inner_collider: return the collider containing the inner rectangles. Should accept an outer rectangle with the key.
        @raise ValueError: if the width and height are not at least 16 pixels
        '''
        #Remember the values
        self.__get_inner_rectangles = get_inner_rectangles
        self.__get_inner_collider = get_inner_collider
        self.__rectangle_collider = rectangle_collider
        
    def insert_outer_rectangle(self, rect):
        '''
        Insert a rectangle into the collider.
        @param rect: the rectangle to insert, which should have the form (x_min,y_min,x_max,y_max,key)
        where key is any custom value
        '''
        self.__rectangle_collider.insert_rectangle(rect)
    
    def remove_outer_rectangle(self, rect):
        '''
        Remove a rectangle from the collider. Note that the key must also be equal
        to the key of the rectangle you wish to remove.
        @param rect: the rectangle to insert, which should have the form (x_min,y_min,x_max,y_max,key)
        where key is any custom value
        @return: true iff the rectangle was removed, since it was in the tree
        '''
        return self.__rectangle_collider.remove_rectangle(rect)
    
    def collide_outer_rectangle(self, outer_rectangle, inner_rectangles=[], inner_collider=None):
        '''
        Collide a rectangle tree with the collider
        @param outer_rectangle: the rectangle to collide against in the form of (x_min,y_min,x_max,y_max)
        @param inner_rectangles: the inner rectangles associated to the outer rectangle as a list of (x_min,y_min,x_max,y_max)
        @param inner_collider: the inner collider associated to the inner rectangle
        @return: a list of all rectangles that collided with the given rectangle.
        '''
        outer_rectangles = self.__rectangle_collider.collide_rectangle(outer_rectangle)
        first_x_offset = outer_rectangle[0]
        first_y_offset = outer_rectangle[1]
        #We now check whether or not each outer rectangle collided against really was colliding.
        first_has_inner_rects = inner_rectangles!=[]
        res = []
        for second_outer_rectangle in outer_rectangles:
            second_inner_rects = self.__get_inner_rectangles(second_outer_rectangle)
            second_has_inner_rects = second_inner_rects!=[]
            second_inner_collider = self.__get_inner_collider(second_outer_rectangle)
            second_x_offset = second_outer_rectangle[0]
            second_y_offset = second_outer_rectangle[1]
            if not (first_has_inner_rects or second_has_inner_rects):
                res.append(second_outer_rectangle)
                continue
            #Loop over the small list
            if len(inner_rectangles)>len(second_inner_rects):
                if not second_has_inner_rects:
                    (x_min,y_min,x_max,y_max,_) = second_outer_rectangle
                    if inner_collider.is_colliding((x_min-first_x_offset,
                                                    y_min-first_y_offset,
                                                    x_max-first_x_offset,
                                                    y_max-first_y_offset)):
                        res.append(second_outer_rectangle)
                    continue
                for (x_min,y_min,x_max,y_max) in second_inner_rects:
                    if inner_collider.is_colliding((x_min+second_x_offset-first_x_offset,
                                                    y_min+second_y_offset-first_y_offset,
                                                    x_max+second_x_offset-first_x_offset,
                                                    y_max+second_y_offset-first_y_offset)):
                        res.append(second_outer_rectangle)
                        break
                continue
            else:
                if not first_has_inner_rects:
                    (x_min,y_min,x_max,y_max) = outer_rectangle
                    if second_inner_collider.is_colliding((x_min-second_x_offset,
                                                           y_min-second_y_offset,
                                                           x_max-second_x_offset,
                                                           y_max-second_y_offset)):
                        res.append(second_outer_rectangle)
                    continue
                for (x_min,y_min,x_max,y_max) in inner_rectangles:
                    if second_inner_collider.is_colliding((x_min+first_x_offset-second_x_offset,
                                                           y_min+first_y_offset-second_y_offset,
                                                           x_max+first_x_offset-second_x_offset,
                                                           y_max+first_y_offset-second_y_offset)):
                        res.append(second_outer_rectangle)
                        break
                continue
        #Done! Res has all of the rectangles that are definitely colliding
        return res
    
    def is_colliding(self, outer_rectangle, inner_rectangles=[], inner_collider=None):
        '''
        Collide a rectangle tree with the collider
        @param outer_rectangle: the rectangle to collide against in the form of (x_min,y_min,x_max,y_max)
        @param inner_rectangles: the inner rectangles associated to the outer rectangle as a list of (x_min,y_min,x_max,y_max)
        @param inner_collider: the inner collider associated to the inner rectangle
        @return: true iff the outer rectangle is colliding with something in the collider
        '''
        outer_rectangles = self.__rectangle_collider.collide_rectangle(outer_rectangle)
        first_x_offset = outer_rectangle[0]
        first_y_offset = outer_rectangle[1]
        #We now check whether or not each outer rectangle collided against really was colliding.
        first_has_inner_rects = inner_rectangles!=[]
        for second_outer_rectangle in outer_rectangles:
            second_inner_rects = self.__get_inner_rectangles(second_outer_rectangle)
            second_has_inner_rects = second_inner_rects!=[]
            second_inner_collider = self.__get_inner_collider(second_outer_rectangle)
            second_x_offset = second_outer_rectangle[0]
            second_y_offset = second_outer_rectangle[1]
            if not (first_has_inner_rects or second_has_inner_rects):
                return True
            #Loop over the small list
            if len(inner_rectangles)>len(second_inner_rects):
                if not second_has_inner_rects:
                    (x_min,y_min,x_max,y_max,_) = second_outer_rectangle
                    if inner_collider.is_colliding((x_min-first_x_offset,
                                                    y_min-first_y_offset,
                                                    x_max-first_x_offset,
                                                    y_max-first_y_offset)):
                        return True
                    continue
                for (x_min,y_min,x_max,y_max) in second_inner_rects:
                    if inner_collider.is_colliding((x_min+second_x_offset-first_x_offset,
                                                    y_min+second_y_offset-first_y_offset,
                                                    x_max+second_x_offset-first_x_offset,
                                                    y_max+second_y_offset-first_y_offset)):
                        return True
                continue
            else:
                if not first_has_inner_rects:
                    (x_min,y_min,x_max,y_max) = outer_rectangle
                    if second_inner_collider.is_colliding((x_min-second_x_offset,
                                                           y_min-second_y_offset,
                                                           x_max-second_x_offset,
                                                           y_max-second_y_offset)):
                        return True
                    continue
                for (x_min,y_min,x_max,y_max) in inner_rectangles:
                    if second_inner_collider.is_colliding((x_min+first_x_offset-second_x_offset,
                                                           y_min+first_y_offset-second_y_offset,
                                                           x_max+first_x_offset-second_x_offset,
                                                           y_max+first_y_offset-second_y_offset)):
                        return True
                continue
        #Done! Res has all of the rectangles that are definitely colliding
        return False
            
    def clear(self):
        '''
        Remove all rectangles from the collider
        '''
        self.__rectangle_collider.clear()