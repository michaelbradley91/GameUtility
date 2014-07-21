'''
Created on 21 Jul 2014

@author: michael
'''

import softwire.com.game_utility.graphics.picture_handling.picture_handler as picture_handler

class RectangleDrawer(picture_handler.Drawer):
    '''
    Construct a new rectangle drawer to draw a rectangle on the screen!
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
        #Remember everything...
        self.__rect = rect
        self.__colour = colour
        self.__depth = depth
        self.__visible = visible
        
        #TODO: ACTUALLY LISTEN TO PARAMS
        #Register with the picture handler so that I will appear!
        picture_handler.PictureHandler.register_rectangles(self, [self.__rect], self.__depth)
        
    def redraw(self, top_left, surface):
        #TODO REMOVE print("Asked to redraw")
        (x_offset,y_offset) = top_left
        (x_min,y_min,width,height) = self.__rect
        #Redraw onto the surface...
        target_rect = (x_min-x_offset,y_min-y_offset,width,height)
        #TODO REMOVE print("Drawing to " + str(target_rect))
        surface.fill(self.__colour,target_rect)
        #Done!
        