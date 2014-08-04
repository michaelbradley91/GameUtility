'''
Created on 3 Aug 2014

@author: michael
'''

from mjb.dev.game_utility.capabilities.capability import Capability
from mjb.dev.game_utility.graphics.screen import Screen
from mjb.dev.game_utility.collisions.screen_collider import ScreenCollider
from mjb.dev.game_utility.collisions.large_rectangle_tree import LargeRectangleTree
from mjb.dev.game_utility.capabilities.shape_handler import ShapeHandler

class CollisionScreen(object):
    '''
    The colliding screen is where checks for collisions are actually kept.
    TODO: the methods are implemented simply at the moment - their efficiency can be improved
    (at least a little)
    '''
    @staticmethod
    def initialise():
        '''
        Initialise the collision screen. This should be called after the screen has been constructed,
        but before any user input has been processed (so immediately after more or less).
        '''
        if not CollisionScreen.__is_initialised:
            CollisionScreen.__screen = ScreenCollider(LargeRectangleTree(Screen.get_screen_size()),
                                                      lambda (a,b,c,d,collideable): collideable._get_inner_shape())
            CollisionScreen.__is_initialised = True
        
    #The screen that the collisions are checked on...
    __screen = None
    __is_initialised = False
    
    @staticmethod
    def _insert_collideable(collideable):
        '''
        Insert a collideable object into the screen (should not already exist)
        @param collideable: the collideable object to add to the screen handler
        '''
        (x_min,y_min,x_max,y_max) = collideable._get_bounding_rectangle()
        CollisionScreen.__screen.insert_rectangle((x_min,y_min,x_max,y_max,collideable))
    
    @staticmethod
    def _remove_collideable(collideable):
        '''
        Remove a collideable object from the screen (must exist)
        @param collideable: the collideable object to remove from the screen handler
        '''
        (x_min,y_min,x_max,y_max) = collideable._get_bounding_rectangle()
        CollisionScreen.__screen.remove_rectangle((x_min,y_min,x_max,y_max,collideable))
        
    @staticmethod
    def get_collisions(shape_handler, precision=None):
        '''
        @param shape_handler: the shape handler to check for collisions with
        @param precision: the precision with which to calculate the shape_handler's shape that you are
        passing in. (The precision works in the same was as in the shape's calculation method)
        @return: all of the shape handlers (as a list) whose shape you are colliding with.
        @note: returning all of the rectangles available is roughly as easy as checking for any particular
        one, so that's what this does.
        
        TODO: could write a method to look for a specific rectangle to collide with - probably wouldn't
        help a lot...
        '''
        #Get the inner rectangles...
        (rect_list,rect_collider) = shape_handler.get_shape().calculate_shape(precision)
        res = CollisionScreen.__screen.collide_rectangle(shape_handler.get_bounding_rectangle(), rect_list, rect_collider)
        shape_handlers = []
        for (_,_,_,_,collideable) in res:
            shape_handlers.append(collideable.get_shape_handler())
        return shape_handlers

class Collideable(Capability):
    '''
    The collideable capability enables an object to be checked for collisions.
    If an object is not made collideable, you cannot detect collisions with it!
    
    TODO: a lot of the code for the capabilities is the same. Try to factor it out.
    '''
    
    def __init__(self, shape_handler, precision, enabled=True):
        '''
        @param shape_handler: the shape handler this is concerned with
        @param precision: the precision that collisions with this shape should be calculated at.
        @param enabled: true by default, whether or not the object should be collideable immediately
        '''
        self.__precision = precision
        self.__shape_handler = shape_handler
        self.__enabled = enabled
        #Attach myself to the collision screen if I'm enabled.
        if self.__enabled:
            CollisionScreen._insert_collideable(self)
            self.__shape_handler._enable_capability(self)
        
    def get_shape_handler(self):
        '''
        @return: the shape handler held by this collideable object
        '''
        return self.__shape_handler
    
    def get_precision(self):
        '''
        @return: the precision used by this capability
        '''
        return self.__precision
    
    def set_precision(self, precision):
        '''
        @param precision: the new precision this capability should use.
        '''
        self.__precision = precision
        #Resetting ourselves in the collision screen is unnecessary because it will recalculate at the
        #precision used at any time.
    
    def _get_bounding_rectangle(self):
        '''
        A method to return the bounding rectangle
        @return: the bounding rectangle as (x_min,y_min,x_max,y_max)
        '''
        return self.__shape_handler.get_bounding_rectangle()
    
    def _get_inner_shape(self):
        '''
        A method to calculate the shape for the screen collider
        @return: (inner_rect_list,inner_collider)
        '''
        return self.__shape_handler.get_shape().calculate_shape(self.__precision)
    
    def prior_update(self, flag):
        '''
        Called strictly before the relevant shape handler updates its state.
        This is a chance for the capability to deregister the handler where appropriate.
        @param flag: a flag stating what is updating (constants held in the shape handler)
        '''
        #Only care about this if enabled
        if self.__enabled:
            if flag!=ShapeHandler._DEPTH_UPDATE:
                #We need to reset...
                CollisionScreen._remove_collideable(self)
    
    def post_update(self, flag):
        '''
        Called strictly after the relevant shape handler updates its state.
        This is a chance for the capability to register (again) the handler where appropriate.
        @param flag: a flag stating what is updating (constants held in the shape handler)
        '''
        #Only care about this if enabled
        if self.__enabled:
            #The depth is not important for us
            if flag!=ShapeHandler._DEPTH_UPDATE:
                #We need to reset...
                CollisionScreen._insert_collideable(self)
    
    def enable(self):
        '''
        Enable this capability
        '''
        if not self.__enabled:
            #Attach myself
            CollisionScreen._insert_collideable(self)
            self.__enabled = True
            self.__shape_handler._enable_capability(self)
        
    def disable(self):
        '''
        Disable this capability
        '''
        if self.__enabled:
            #Detach myself
            CollisionScreen._remove_collideable(self)
            self.__enabled = False
            self.__shape_handler._disable_capability(self)