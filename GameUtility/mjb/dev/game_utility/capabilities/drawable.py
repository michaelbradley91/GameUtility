'''
Created on 3 Aug 2014

@author: michael
'''

from mjb.dev.game_utility.capabilities.capability import Capability
from mjb.dev.game_utility.graphics.picture_handler import PictureHandler

class Drawable(Capability):
    '''
    The drawable capability enables an object to be drawn!
    
    This class interacts heavily with the picture handler class to ensure objects can be drawn,
    and is an unusual capability as it supports updates to the appearance of a shape as well
    as changes to the shape itself.
    
    It manages some of the plumbing to older code
    
    TODO: a lot of the code for the capabilities is the same. Try to factor it out.
    '''
    
    class _Inner_Drawer(object):
        '''
        Class which actually registers with the picture handler...
        '''
        def __init__(self, drawable):
            '''
            Construct a drawer to draw on the picture handler with the given drawable object
            @param drawable: the drawable capability being added
            '''
            self.__drawable = drawable
    
        def redraw(self, top_left, surface):
            #Redraw yourself!
            self.__drawable._get_redraw_handler(top_left,surface)
        
        def get_bounding_rectangle(self):
            self.__drawable._get_bounding_rectangle()
        
        def get_inner_shape(self):
            self.__drawable._get_inner_shape()
        
        def get_depth(self):
            self.__drawable._get_depth()
    
    def __init__(self, shape_handler, precision, redraw_handler, enabled=True):
        '''
        @param shape_handler: the shape handler this is concerned with
        @param precision: the precision at which to calculate the redrawing of this object
        (see the picture handler for details).
        @param redraw_handler: a function to redraw the shape. Should accept a top left coordinate
        and a pygame surface to draw on.
        @param enabled: true by default, whether or not the object should be drawable immediately
        '''
        self.__precision = precision
        self.__shape_handler = shape_handler
        self.__enabled = enabled
        self.__redraw_handler = redraw_handler
        self.__inner_drawer = Drawable._Inner_Drawer(self)
        #Attach myself to the picture handler if I'm enabled.
        if self.__enabled:
            PictureHandler.register_drawer(self.__inner_drawer)
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
    
    def _get_redraw_handler(self):
        '''
        @return: the redraw handler used to draw the shape (in the shape handler...)
        '''
        return self.__redraw_handler
    
    def prior_appearance_update(self):
        '''
        To be called strictly before the appearance of a drawable shape handler is changed.
        '''
        #Flag is irrelevant
        self.prior_update(0)
        
    def post_appearance_update(self):
        '''
        To be called strictly after the appearance of the drawable shape handler has been changed.
        '''
        #Flag is irrelevant
        self.post_update(0)
    
    def prior_update(self, flag):
        '''
        Called strictly before the relevant shape handler updates its state.
        This is a chance for the capability to deregister the handler where appropriate.
        @param flag: a flag stating what is updating (constants held in the shape handler)
        '''
        #Only care about this if enabled
        if self.__enabled:
            #We need to reset...
            PictureHandler.deregister_drawer(self.__inner_drawer)
    
    def post_update(self, flag):
        '''
        Called strictly after the relevant shape handler updates its state.
        This is a chance for the capability to register (again) the handler where appropriate.
        @param flag: a flag stating what is updating (constants held in the shape handler)
        '''
        #Only care about this if enabled
        if self.__enabled:
            PictureHandler.register_drawer(self.__inner_drawer)
    
    def enable(self):
        '''
        Enable this capability
        '''
        if not self.__enabled:
            #Attach myself
            PictureHandler.register_drawer(self.__inner_drawer)
            self.__enabled = True
            self.__shape_handler._enable_capability(self)
        
    def disable(self):
        '''
        Disable this capability
        '''
        if self.__enabled:
            #Detach myself
            PictureHandler.deregister_drawer(self.__inner_drawer)
            self.__enabled = False
            self.__shape_handler._disable_capability(self)