'''
Created on 6 Aug 2014

@author: michael
'''

from mjb.dev.game_utility.shapes.shape import Shape
from mjb.dev.game_utility.shapes.handlers.drawable_shape_handler import DrawableShapeHandler
from mjb.dev.game_utility.capabilities.drawable import Drawable

class DrawableRectangleHandler(DrawableShapeHandler):
    '''
    Construct a new rectangle drawer to draw a rectangle on the screen!
    
    TODO: complication in the immutability of the shape and its size when setting the rectangle.
    We have to change the shape used internally independently
    '''
    
    class _Rectangle_Shape(Shape):
        '''
        The shape used by the rectangle handler
        '''
        
        def __init__(self,rect):
            '''
            Construct a new rectangle shape
            @param rect: the rectangle as (x_min,y_min,width,height)
            '''
            #Make the shape...
            Shape.__init__(self, cache_depth=0)
            (_,_,width,height) = rect
            self.__size = (width,height)
        
        #Override
        def get_size(self):
            return self.__size
        
        #Override
        def _calculate_shape_to_override(self,precision,include_collider):
            return ([],None)
            
    def __init__(self,rect,colour,depth=0,visible=True):
        '''
        Construct a new rectangle to draw on the screen. You should hold onto this object
        to change its position etc, so that it maintains properties like its depth and colour
        (+implementation stuff...) for you.
        @param rect: the rectangle to draw (x_min,y_min,width,height)
        @param colour: the colour to solid fill the rectangle with
        @param depth: the depth on screen this rectangle should be drawn at. Default 0,
        higher values push the object further back
        @param visible: True by default - whether or not you want this rectangle to appear
        on screen.
        @note: the rectangle drawer automatically attaches a drawable capability to itself.
        '''
        #Make myself as a shape handler...
        (x_min,y_min,_,_) = rect
        DrawableShapeHandler.__init__(self, DrawableRectangleHandler._Rectangle_Shape(rect), depth, (x_min,y_min))
        #Remember everything...
        self.__colour = colour
        #Attach to a drawable handler...
        self.__drawable_capability = Drawable(self,None,self.redraw,enabled=False)
        if visible:
            #Register with the picture handler so that I will appear!
            self.__drawable_capability.enable()
    
    def redraw(self, top_left, surface):
        '''
        Redraw this rectangle!
        @param top_left: the top left coordinate of the surface the rectangle is being drawn on
        @param surface: the surface to draw on
        '''
        (x_offset,y_offset) = top_left
        (x_min,y_min,x_max,y_max) = self.get_bounding_rectangle()
        #Redraw onto the surface...
        target_rect = (x_min-x_offset,y_min-y_offset,x_max-x_min,y_max-y_min)
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
        The rect should be in the form of (x_min,y_min,width,height) 
        '''
        (x_min,y_min,width,height) = rect
        if (self.get_shape().get_size()==(width,height)):
            #Keep the old shape...
            if (x_min,y_min)==self.get_top_left():
                return #nothing to do
            self.set_top_left((x_min,y_min))
        else:
            self.set_shape(DrawableRectangleHandler._Rectangle_Shape(rect), top_left=(x_min,y_min))
                
    def set_colour(self,colour):
        '''
        @param colour: the colour the rectangle should be filled with
        '''
        if self.__colour!=colour:
            #Change the appearance
            self.change_appearance(self.__set_colour, colour)
    
    def __set_colour(self, colour):
        '''
        The deferred set colour method
        @param colour: the colour the rectangle should be turned into
        '''
        self.__colour = colour
    
    def move_rectangle(self,x_move=0,y_move=0):
        '''
        @param x_move: the amount to move in the x coordinate along the screen
        @param y_move: the amount to move in the y coordinate along the screen
        '''
        (x_min,y_min) = self.get_top_left()
        self.set_top_left((x_min+x_move,y_min+y_move))
        
    #Get the various properties...
    def get_rectangle(self):
        '''
        @return: the rectangle as (x_min,y_min,width,height) being drawn by this drawer
        '''
        (width,height) = self.get_shape().get_size()
        (x_min,y_min) = self.get_top_left()
        return (x_min,y_min,width,height)
    
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
    
    