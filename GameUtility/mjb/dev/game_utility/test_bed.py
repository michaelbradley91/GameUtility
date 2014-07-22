'''
Created on 21 Jul 2014

@author: michael
'''

import mjb.dev.game_utility.graphics.screen as screen
import mjb.dev.game_utility.input_listeners.keyboard_listener as key_listeners
import mjb.dev.game_utility.input_listeners.mouse_button_listener as mouse_button_listeners
import mjb.dev.game_utility.input_listeners.mouse_motion_listener as mouse_motion_listeners
import mjb.dev.game_utility.input_listeners.frame_listener as frame_listeners
import mjb.dev.game_utility.graphics.drawers.rectangle_drawer as rectangle_drawer
import pygame.locals

class QuitKeyboardListener(key_listeners.KeyboardListener):
    
    def __init__(self, keys):
        #Initialise both keys...
        key_listeners.KeyboardListener.__init__(self,keys)
        
    def key_down(self,key,key_modifiers):
        if key==pygame.locals.K_ESCAPE:
            print("Exiting!")
            screen.Screen.quit_game()

class Dadskeys(key_listeners.KeyboardListener, frame_listeners.FrameListener,mouse_button_listeners.MouseButtonListener):
    
    def __init__(self, my_rectangle, keys):
        #Initialise both keys...
        key_listeners.KeyboardListener.__init__(self,keys)
        frame_listeners.FrameListener.__init__(self)
        mouse_button_listeners.MouseButtonListener.__init__(self)
        #Remember if kp8 is down
        self.kp8_is_down = False
        self.kp2_is_down = False
        self.my_rectangle = my_rectangle
        
        
    def key_down(self,key,key_modifiers):
        if key==pygame.locals.K_KP8:
            self.kp8_is_down = True
        if key==pygame.locals.K_KP2:
            self.kp2_is_down = True
            
    
    def key_up(self,key,key_modifiers):
        if key==pygame.locals.K_KP8:
            self.kp8_is_down = False
        if key==pygame.locals.K_KP2:
            self.kp2_is_down = False
    
    def frame_passed(self):
        if self.kp8_is_down:
            self.my_rectangle.move_rectangle(x_move=2,y_move=2)
        if self.kp2_is_down:
            self.my_rectangle.move_rectangle(x_move=2,y_move=-2)
            
    def button_down(self,button):
        if mouse_button_listeners.LEFT_BUTTON==button:
            self.my_rectangle.set_visible(False)
        if mouse_button_listeners.RIGHT_BUTTON==button:
            self.my_rectangle.set_visible(True)
            (r,g,b) = self.my_rectangle.get_colour()
            self.my_rectangle.set_colour((r-20,g,b))

def run():
    QuitKeyboardListener([pygame.locals.K_ESCAPE])
    'Your code goes here!'
    #rectangle_drawer.RectangleDrawer((x_min,y_min,width,height),(r,g,b),depth)
    my_rectangle = rectangle_drawer.RectangleDrawer((500,400,100,100),(250,50,150),50)
    Dadskeys(my_rectangle,[pygame.locals.K_KP8,pygame.locals.K_KP2])
    'End code'
    screen.Screen.start_game_loop()