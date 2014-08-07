'''
Created on 7 Aug 2014

@author: michael
'''

from mjb.dev.game_utility.shapes.handlers.drawable_shape_handler import DrawableShapeHandler
from mjb.dev.game_utility.capabilities.drawable import Drawable

class ImageShapeHandler(DrawableShapeHandler):
    '''
    This class is a simple wrapper to provide useful friendlier methods to manipulate an
    image in the game
    '''

    def __init__(self,image_shape,top_left,depth=0,visible=True,precision=None):
        '''
        @param image: the image to hold and manipulate
        @param top_left: the top left coordinate of the image as it should appear on screen
        @param depth: the depth on screen that the image should sit at. Higher depth
        pushes the image further back away from you facing the screen. Default 0
        @param visibile: whether or not this shape should be visible. Default True
        @param precision: the precision at whcih to control redraws. Typically, this should be None (default)
        '''
        DrawableShapeHandler.__init__(self, image_shape, depth, top_left)
        self.__drawable_capability = Drawable(self,precision,self.redraw,enabled=False)
        if visible:
            #Register with the picture handler so that I will appear!
            self.__drawable_capability.enable()
    
    def get_visible(self):
        '''
        @return: True iff this drawer is visible on screen (in the sense that it is actually drawing)
        '''
        return self.__drawable_capability.is_enabled()
    
    def set_visible(self, visible=True):
        '''
        @param visible: Default True, whether or not the rectangle should appear on the screen
        '''
        if self.__drawable_capability.is_enabled()!=visible:
            if visible:
                #Appear!
                self.__drawable_capability.enable()
            else:
                #Disappear!
                self.__drawable_capability.disable()
                
    def redraw(self, top_left, surface):
        '''
        Draw the image onto the surface...
        (overridden)
        '''
        #Figure out the top left coordinate to draw on...
        (x,y) = top_left
        (x2,y2) = self.get_top_left()
        surface.blit(self.get_shape().get_image().get_surface(),(x2-x,y2-y))
        #Done, hopefully!
        