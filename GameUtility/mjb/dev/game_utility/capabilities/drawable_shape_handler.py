'''
Created on 5 Aug 2014

@author: michael
'''

from mjb.dev.game_utility.capabilities.shape_handler import ShapeHandler
from mjb.dev.game_utility.capabilities.drawable import Drawable

class DrawableShapeHandler(ShapeHandler):
    '''
    This class is designed to enable the drawing of objects
    on the screen. If you wish to use a drawable capability, you should always
    use a drawable shape handler. (You may want to use this by default regardless...)
    '''
    
    __drawable_capability = None
    
    def change_appearance(self, change_function, param):
        '''
        This method should be called whenever you intend to change the appearance of an object on
        screen.
        @param change_function: the function to implement the change in appearance
        @param param: the parameter to be passed to the change function (for convenience)
        '''
        if self.__drawable_capability!=None:
            #TODO: Do something!!
            self.__drawable_capability.prior_appearance_update()
            change_function(param)
            self.__drawable_capability.post_appearance_update()
        #Done!
    
    def _enable_capability(self, capability):
        '''
        This method is called by the capability itself when it is enabled.
        @param capability: the capability being added
        '''
        if capability is Drawable:
            #Hold this separately
            self.__drawable_capability = capability
        else:
            ShapeHandler._enable_capability(self, capability)
        
    def _disable_capability(self, capability):
        '''
        This method is called by the capability itself when it is disabled.
        @param capability: the capability being removed
        '''
        if capability is Drawable:
            #Remove this specially
            self.__drawable_capability = None
        else:
            ShapeHandler._disable_capability(self, capability)
    
        