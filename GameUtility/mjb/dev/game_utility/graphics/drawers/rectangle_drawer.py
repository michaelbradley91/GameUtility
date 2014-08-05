'''
Created on 21 Jul 2014

@author: michael
'''

from mjb.dev.game_utility.capabilities.shape import Shape
from mjb.dev.game_utility.capabilities.drawable_shape_handler import DrawableShapeHandler
from mjb.dev.game_utility.capabilities.drawable import Drawable

class RectangleDrawer(Shape):
    '''
    Construct a new rectangle drawer to draw a rectangle on the screen!
    
    TODO: refactor this! Done for testing at the moment.
    '''

    def __init__(self,rect,colour,depth=0,visible=True):
        '''
        Construct a new rectangle drawer to draw the specific rectangle. Note that this
        rectangle will automatically redraw for you - so no worries!
        @param rect: the rectangle to draw (x_min,y_min,width,height)
        @param colour: the colour to solid fill the rectangle with
        @param depth: the depth on screen this rectangle should be drawn at. Default 0,
        higher values push the object further back
        @param visible: True by default - whether or not you want this rectangle to appear
        on screen.
        '''
        #Use no cache
        Shape.__init__(self, cache_depth=0)
        #Remember everything...
        (x_min,y_min,width,height) = rect
        self.__colour = colour
        #Attach to a drawable handler...
        self.__handler = DrawableShapeHandler(self, depth, (x_min,y_min,x_min+width,y_min+height))
        self.__drawable_capability = Drawable(self.__handler,None,self.redraw,enabled=False)
        #TODO: ACTUALLY LISTEN TO PARAMS
        if visible:
            #Register with the picture handler so that I will appear!
            self.__drawable_capability.enable()
    
    #Override
    def redraw(self, top_left, surface):
        #TODO REMOVE print("Asked to redraw")
        (x_offset,y_offset) = top_left
        (x_min,y_min,x_max,y_max) = self.get_bounding_rectangle()
        #Redraw onto the surface...
        target_rect = (x_min-x_offset,y_min-y_offset,x_max-x_min,y_max-y_min)
        #TODO REMOVE print("Drawing to " + str(target_rect))
        surface.fill(self.__colour,target_rect)
        #Done!
        
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
    
    def set_rectangle(self,rect):
        '''
        @param rect: set the new rectangular area to be covered by this rectangle (separately from the colour) 
        '''
        self.__handler.set_bounding_rectangle(rect)
                
    def set_colour(self,colour):
        '''
        @param colour: the colour the rectangle should be filled with
        '''
        if self.__colour!=colour:
            #Change the appearance
            self.__handler.change_appearance(self.__set_colour, colour)
    
    def __set_colour(self, colour):
        #Actually set the colour
        self.__colour = colour
    
    def move_rectangle(self,x_move=0,y_move=0):
        '''
        @param x_move: the amount to move in the x coordinate along the screen
        @param y_move: the amount to move in the y coordinate along the screen
        '''
        (x_min,y_min,x_max,y_max) = self.get_bounding_rectangle()
        self.__handler.set_bounding_rectangle((x_min+x_move,y_min+y_move,x_max+x_move,y_max+y_move))
        
    def set_depth(self,depth):
        '''
        @param depth: the depth you wish this to now draw at
        '''
        if self.__handler.get_depth()!=depth:
            self.__handler.set_depth(depth)
        
    #Get the various properties...
    def get_rectangle(self):
        '''
        @return: the rectangle as (x_min,y_min,width,height) being drawn by this drawer
        '''
        return self.__handler.get_bounding_rectangle()
    
    def get_colour(self):
        '''
        @return: the colour of the rectangle being drawn by this drawer
        '''
        return self.__colour
    
    def get_visible(self):
        '''
        @return: True iff this drawer is visible on screen (in the sense that it is actually drawing)
        '''
        return self.__drawable_capability.is_enabled()
        
    def get_bounding_rectangle(self):
        '''
        @return: a rectangle in the form of (x_min,y_min,x_max,y_max) covering the whole
        area that the drawer might draw in. This should not change.
        '''
        return self.__handler.get_bounding_rectangle()
    
    def _calculate_shape_to_override(self,precision,include_collider):
        '''
        This method's intended behaviour is identical to calculate shape's except this
        is meant to be overridden.
        '''
        return ([],None)
    
    def get_depth(self):
        '''
        @return: the depth this drawer wishes to draw at. This should not change.
        '''
        return self.__handler.get_depth()