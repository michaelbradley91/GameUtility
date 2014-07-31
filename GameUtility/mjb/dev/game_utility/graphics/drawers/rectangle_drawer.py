'''
Created on 21 Jul 2014

@author: michael
'''

import mjb.dev.game_utility.graphics.picture_handler as picture_handler

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
        if self.__visible:
            #Register with the picture handler so that I will appear!
            picture_handler.PictureHandler.register_drawer(self)
    
    #Override
    def redraw(self, top_left, surface):
        #TODO REMOVE print("Asked to redraw")
        (x_offset,y_offset) = top_left
        (x_min,y_min,width,height) = self.__rect
        #Redraw onto the surface...
        target_rect = (x_min-x_offset,y_min-y_offset,width,height)
        #TODO REMOVE print("Drawing to " + str(target_rect))
        surface.fill(self.__colour,target_rect)
        #Done!
        
    def set_visible(self, visible=True):
        '''
        @param visible: Default True, whether or not the rectangle should appear on the screen
        '''
        if self.__visible!=visible:
            self.__visible = visible
            if self.__visible:
                #Appear!
                self.__register()
            else:
                #Disappear!
                self.__deregister()
    
    def __register(self):
        '''
        To remove code duplication, register myself with the picture handler
        '''
        picture_handler.PictureHandler.register_drawer(self)
    
    def __deregister(self):
        '''
        To remove code duplication, deregister myself with the picture handler
        '''
        picture_handler.PictureHandler.deregister_drawer(self)
    
    def set_rectangle(self,rect):
        '''
        @param rect: set the new rectangular area to be covered by this rectangle (separately from the colour) 
        '''
        if self.__rect!=rect:
            if self.__visible:
                #Redraw!
                self.__deregister()
                #Change after deregistration
                self.__rect = rect
                self.__register()
            else:
                self.__rect = rect
                
    def set_colour(self,colour):
        '''
        @param colour: the colour the rectangle should be filled with
        '''
        if self.__colour!=colour:
            self.__colour = colour
            if self.__visible:
                #Redraw!
                self.__deregister()
                self.__register()
                
    def move_rectangle(self,x_move=0,y_move=0):
        '''
        @param x_move: the amount to move in the x coordinate along the screen
        @param y_move: the amount to move in the y coordinate along the screen
        '''
        (x_min,y_min,width,height) = self.__rect
        self.set_rectangle((x_min+x_move,y_min+y_move,width,height))
        
    def set_depth(self,depth):
        '''
        @param depth: the depth you wish this to now draw at
        '''
        if self.__depth!=depth:
            self.__depth = depth
            if self.__visible:
                #Redraw!
                self.__deregister()
                self.__register()
        
    #Get the various properties...
    def get_rectangle(self):
        '''
        @return: the rectangle as (x_min,y_min,width,height) being drawn by this drawer
        '''
        return self.__rect
    
    def get_colour(self):
        '''
        @return: the colour of the rectangle being drawn by this drawer
        '''
        return self.__colour
    
    def get_visible(self):
        '''
        @return: True iff this drawer is visible on screen (in the sense that it is actually drawing)
        '''
        return self.__visible
        
    def get_bounding_rectangle(self):
        '''
        @return: a rectangle in the form of (x_min,y_min,x_max,y_max) covering the whole
        area that the drawer might draw in. This should not change.
        '''
        return (self.__rect[0],self.__rect[1],
                self.__rect[0]+self.__rect[2],
                self.__rect[1]+self.__rect[3])
    
    def get_inner_rectangles(self):
        '''
        @return: the inner rectangles more accurately representing the space occupied by
        the drawer. This is intended to remain static (change the drawer if the image
        changes). The rectangles should be of the form (x_min,y_min,x_max,y_max).
        Use an empty list if the bounding rectangle is accurate enough.
        This should not change.
        '''
        return []
    
    def get_inner_collider(self):
        '''
        @return: a rectangle collider containing all of the inner rectangles.
        Leave this as None if no such rectangle is required. This should not change.
        '''
        return None
    
    def get_depth(self):
        '''
        @return: the depth this drawer wishes to draw at. This should not change.
        '''
        return self.__depth