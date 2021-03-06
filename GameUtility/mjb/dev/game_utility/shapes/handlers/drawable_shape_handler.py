'''
Created on 5 Aug 2014

@author: michael
'''

from mjb.dev.game_utility.shapes.handlers.shape_handler import ShapeHandler
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
        if type(capability) is Drawable:
            #Hold this separately
            self.__drawable_capability = capability
        ShapeHandler._enable_capability(self, capability)
        
    def _disable_capability(self, capability):
        '''
        This method is called by the capability itself when it is disabled.
        @param capability: the capability being removed
        '''
        if type(capability) is Drawable:
            #Remove this specially
            self.__drawable_capability = None
        ShapeHandler._disable_capability(self, capability)
    
    def dispose(self):
        '''
        Dispose of this shape handler. You should not use this shape handler
        again once it has been disposed...
        '''
        #For each enabled capability, dispose it!
        if self.__drawable_capability!=None:
            self.__drawable_capability.dispose()
            self.__drawable_capability = None
        #Call the base class too..
        ShapeHandler.dispose(self)
        
    def redraw(self, top_left, surface):
        '''
        To be overridden - redraw the shape in this shape handler.
        You should blit or otherwise draw onto the surface, clipping yourself as required.
        @param top_left: the top left coordinate of the surface passed in as it will
        be drawn on screen
        @param surface: the surface to draw on
        '''
        pass