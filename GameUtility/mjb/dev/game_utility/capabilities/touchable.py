'''
Created on 3 Aug 2014

@author: michael
'''

from mjb.dev.game_utility.capabilities.capability import Capability
from mjb.dev.game_utility.graphics.screen import Screen
from mjb.dev.game_utility.collisions.screen_collider import ScreenCollider
from mjb.dev.game_utility.collisions.large_rectangle_tree import LargeRectangleTree
from mjb.dev.game_utility.capabilities.shape_handler import ShapeHandler
from mjb.dev.game_utility.input_listeners.mouse_motion_listener import MouseMotionListener

class TouchScreen(object):
    '''
    The touch screen (unfortunately named...) is where mouse enter and mouse leave events are
    calculated based on the mouse's motion.
    TODO: the methods are implemented simply at the moment - their efficiency can be improved
    (at least a little)
    
    TODO: the mouse enter event is not called immediately even if the mouse begins on top of the shape.
    That may be faithful to the name anyway...
    '''
    @staticmethod
    def initialise():
        '''
        Initialise the collision screen. This should be called after the screen has been constructed,
        but before any user input has been processed (so immediately after more or less).
        '''
        if not TouchScreen.__is_initialised:
            TouchScreen.__screen = ScreenCollider(LargeRectangleTree(Screen.get_screen_size()),
                                                      lambda (a,b,c,d,collideable): collideable._get_inner_shape())
            TouchScreen.__is_initialised = True
        
    #The screen that the collisions are checked on...
    __screen = None
    __is_initialised = False
    
    #Remember the touchables who believe the mouse is inside them...
    _touchables_entered = set()
    
    #The mouse motion listener
    class _ClickScreenMouseButtonListener(MouseMotionListener):
        def mouse_moved(self,location):
            #Forward to the touch screen
            TouchScreen._mouse_moved(location)
    
    @staticmethod
    def _insert_touchable(touchable):
        '''
        Insert a collideable object into the screen (should not already exist)
        @param collideable: the collideable object to add to the screen handler
        '''
        (x_min,y_min,x_max,y_max) = touchable._get_bounding_rectangle()
        TouchScreen.__screen.insert_rectangle((x_min,y_min,x_max,y_max,touchable))
    
    @staticmethod
    def _remove_touchable(touchable):
        '''
        Remove a collideable object from the screen (must exist)
        @param collideable: the collideable object to remove from the screen handler
        '''
        (x_min,y_min,x_max,y_max) = touchable._get_bounding_rectangle()
        TouchScreen.__screen.remove_rectangle((x_min,y_min,x_max,y_max,touchable))
        
    @staticmethod
    def _mouse_moved(location):
        #Collide the mouse at this position with the screen...
        #Collide the mouse with all objects on the screen...
        (x_min,y_min) = location
        touchables = TouchScreen.__screen.collide_rectangle((x_min,y_min,x_min+1,y_min+1), [], None)
        touchable_set = set()
        #Update the objects which it (just) entered
        for touchable in touchables:
            touchable_set.add(touchable)
            if not touchable in TouchScreen._touchables_entered:
                (touchable._get_mouse_enter_handler())()
        #Update the objects which it left
        for touchable in TouchScreen._touchables_entered:
            if not touchable in touchable_set:
                (touchable._get_mouse_leave_handler())()
        TouchScreen._touchables_entered = touchable_set

def get_entered_shape_handlers():
    '''
    @return: a set of all shape handlers which the mouse is currently considered to have entered.
    You should not modify this set.
    '''
    return TouchScreen._touchables_entered

class Touchable(Capability):
    '''
    The collideable capability enables an object to be checked for collisions.
    If an object is not made collideable, you cannot detect collisions with it!
    
    TODO: a lot of the code for the capabilities is the same. Try to factor it out.
    '''
    
    def __init__(self, shape_handler, precision, mouse_enter_handler, mouse_leave_handler, enabled=True):
        '''
        @param shape_handler: the shape handler this is concerned with
        @param precision: the precision that collisions with this shape should be calculated at.
        @param mouse_enter_handler: a function to be called whenever the mouse enters this object.
        Accepts no arguments.
        @param mouse_leave_handler: a function to be called whenever the mouse leaves this object.
        Accepts no arguments
        @param top_only: false by default, set to true iff you only want the events to be handled when
        it affects the top most element that is touchable.*
        @param enabled: true by default, whether or not the object should be collideable immediately
        
        *If an element is not touchable, it will never be considered on top. Hence, to block a mouse enter
        or leave event, you would need to cover it with a touchable shape and swallow the events.
        '''
        self.__precision = precision
        self.__shape_handler = shape_handler
        self.__enabled = enabled
        self.__mouse_enter_handler = mouse_enter_handler
        self.__mouse_leave_handler = mouse_leave_handler
        #Attach myself to the collision screen if I'm enabled.
        if self.__enabled:
            TouchScreen._insert_collideable(self)
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
    
    def _get_mouse_enter_handler(self):
        '''
        @return: the function designed to handle the mouse entering
        '''
        return self.__mouse_enter_handler
    
    def _get_mouse_leave_handler(self):
        '''
        @return: the function designed to handle the mouse leaving
        '''
        return self.__mouse_leave_handler
    
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
    
    def _get_depth(self):
        '''
        A method to return the depth
        @return: the depth of the bounding rectangle
        '''
        return self.__shape_handler.get_depth()
    
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
                TouchScreen._remove_collideable(self)
    
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
                TouchScreen._insert_collideable(self)
    
    def enable(self):
        '''
        Enable this capability
        '''
        if not self.__enabled:
            #Attach myself
            TouchScreen._insert_collideable(self)
            self.__enabled = True
            self.__shape_handler._enable_capability(self)
        
    def disable(self):
        '''
        Disable this capability
        '''
        if self.__enabled:
            #Detach myself
            TouchScreen._remove_collideable(self)
            self.__enabled = False
            self.__shape_handler._disable_capability(self)