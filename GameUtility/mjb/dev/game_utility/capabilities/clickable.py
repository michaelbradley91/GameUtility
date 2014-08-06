'''
Created on 3 Aug 2014

@author: michael
'''

from mjb.dev.game_utility.capabilities.capability import Capability
from mjb.dev.game_utility.graphics.screen import Screen
from mjb.dev.game_utility.collisions.screen_collider import ScreenCollider
from mjb.dev.game_utility.collisions.large_rectangle_tree import LargeRectangleTree
from mjb.dev.game_utility.shapes.handlers.shape_handler import ShapeHandler
from mjb.dev.game_utility.input_listeners.mouse_button_listener import MouseButtonListener
import mjb.dev.game_utility.input_listeners.mouse_motion_listener as mouse_motion_listener

class ClickScreen(object):
    '''
    The click screen is where rectangles for click detection are actually kept.
    TODO: the methods are implemented simply at the moment - their efficiency can be improved
    (at least a little)
    '''
    @staticmethod
    def initialise():
        '''
        Initialise the collision screen. This should be called after the screen has been constructed,
        but before any user input has been processed (so immediately after more or less).
        '''
        if not ClickScreen.__is_initialised:
            ClickScreen.__screen = ScreenCollider(LargeRectangleTree(Screen.get_screen_size()),
                                                      lambda (a,b,c,d,clickable): clickable._get_inner_shape())
            ClickScreen.__is_initialised = True
        #Start listening...
        ClickScreen._ClickScreenMouseButtonListener()
        
    #The screen that the collisions are checked on...
    __screen = None
    __is_initialised = False
    
    #The mouse button listener
    class _ClickScreenMouseButtonListener(MouseButtonListener):
        def button_down(self,button):
            #Forward to the click screen
            ClickScreen._mouse_button_down(button, mouse_motion_listener.get_mouse_position())
        def button_up(self,button):
            #Forward to the click screen
            ClickScreen._mouse_button_up(button, mouse_motion_listener.get_mouse_position())
    
    @staticmethod
    def _insert_clickable(clickable):
        '''
        Insert a collideable object into the screen (should not already exist)
        @param collideable: the collideable object to add to the screen handler
        '''
        (x_min,y_min,x_max,y_max) = clickable._get_bounding_rectangle()
        ClickScreen.__screen.insert_rectangle((x_min,y_min,x_max,y_max,clickable))
    
    @staticmethod
    def _remove_clickable(clickable):
        '''
        Remove a collideable object from the screen (must exist)
        @param collideable: the collideable object to remove from the screen handler
        '''
        (x_min,y_min,x_max,y_max) = clickable._get_bounding_rectangle()
        ClickScreen.__screen.remove_rectangle((x_min,y_min,x_max,y_max,clickable))
    
    @staticmethod
    def _mouse_button_down(button, location):
        '''
        @param button: the button pushed down
        @param location: the location of the mouse when the button was pushed down
        '''
        ClickScreen.__process_click(button, location, True)
    
    @staticmethod
    def __process_click(button, location, is_down):
        '''
        To remove code duplication, this updates all of the click objects.
        @param button: the button in the event
        @param location: the location of the mouse when the event was raised
        @param is_down: true iff the button was released (otherwise pressed)
        '''
        #Collide the mouse with all objects on the screen...
        (x_min,y_min) = location
        clickables = ClickScreen.__screen.collide_rectangle((x_min,y_min,x_min+1,y_min+1), [], None)
        #Convert the list...
        temp_list = []
        for (_,_,_,_,clickable) in clickables:
            temp_list.append(clickable)
        clickables = temp_list
        #Find out which is the minimum...
        if clickables!=[]:
            #Some minimum to find
            min_depth = clickables[0]._get_depth()
            min_index = 0
            for index in range(1,len(clickables)):
                depth = clickables[index]._get_depth()
                if depth<min_depth:
                    min_depth = depth
                    min_index = index
            min_clickable = clickables[min_index]
            #Got the minimum! Now update the clickable objects...
            if is_down:
                for clickable in clickables:
                    (clickable._get_button_down_handler())(button, clickable==min_clickable)
            else:
                for clickable in clickables:
                    (clickable._get_button_up_handler())(button, clickable==min_clickable)
    
    @staticmethod
    def _mouse_button_up(button, location):
        '''
        @param button: the button released
        @param location: the location of the mouse when the button was released
        '''
        ClickScreen.__process_click(button, location, False)

class Clickable(Capability):
    '''
    The clickable capability enables an object to identify if it has been clicked.
    
    TODO: a lot of the code for the capabilities is the same. Try to factor it out.
    '''
    
    def __init__(self, shape_handler, precision, button_down_handler, button_up_handler, enabled=True):
        '''
        @param shape_handler: the shape handler this is concerned with
        @param precision: the precision that collisions with this shape should be calculated at.
        @param button_down_handler: a function prepared to accept a button and a flag which will be true iff
        you were the top element clicked on*.
        @param button_up_handler: a hander with the same parameters as the button_down_handler
        (but called when a mouse button is released)
        @param enabled: true by default, whether or not the object should be clickable immediately
        
        *Awkwardly, if you wanted other elements to block a click event by being on top, you'll need
        to make them clickable too to swallow the event.
        '''
        self.__precision = precision
        self.__shape_handler = shape_handler
        self.__enabled = enabled
        self.__button_down_handler = button_down_handler
        self.__button_up_handler = button_up_handler
        #Attach myself to the click screen if I'm enabled.
        if self.__enabled:
            ClickScreen._insert_clickable(self)
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
    
    def _get_depth(self):
        '''
        A method to return the depth
        @return: the depth of the bounding rectangle
        '''
        return self.__shape_handler.get_depth()
    
    def _get_button_up_handler(self):
        '''
        @return: the button up handler held by this clickable object
        '''
        return self.__button_up_handler
    
    def _get_button_down_handler(self):
        '''
        @return: the button down handler held by this clickable object
        '''
        return self.__button_down_handler
    
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
                ClickScreen._remove_clickable(self)
    
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
                ClickScreen._insert_clickable(self)
    
    def enable(self):
        '''
        Enable this capability
        '''
        if not self.__enabled:
            #Attach myself
            ClickScreen._insert_clickable(self)
            self.__enabled = True
            self.__shape_handler._enable_capability(self)
        
    def disable(self):
        '''
        Disable this capability
        '''
        if self.__enabled:
            #Detach myself
            ClickScreen._remove_clickable(self)
            self.__enabled = False
            self.__shape_handler._disable_capability(self)
    
    def is_enabled(self):
        '''
        @return: true iff this capability is enabled
        '''
        return self.__enabled
    
    def dispose(self):
        '''
        Dispose of this capability (freeing memory)
        Once called, the capability should not be used again
        '''
        self.disable()