'''
Created on 4 Jul 2014

@author: michael
'''
import softwire.com.game_utility.graphics.screen as screen
import softwire.com.game_utility.input_listeners.keyboard_listener as key_listeners
import softwire.com.game_utility.input_listeners.mouse_button_listener as mouse_button_listeners
import softwire.com.game_utility.input_listeners.mouse_motion_listener as mouse_motion_listeners
import softwire.com.game_utility.graphics.picture_handling.picture_handler as picture_handler
import pygame.locals
import softwire.com.game_utility.graphics.picture_handling.rectangle_tree as rect_tree
import time

class DummyKeyListener(key_listeners.KeyboardListener):
    
    def key_down(self,key,key_modifiers):
        print("Key went down: " + str(key) + " with modifier/s " + str(key_modifiers))
        if key==pygame.locals.K_ESCAPE:
            #Exit
            print("Trying to quit")
            screen.Screen.quit_game()
        
    def key_up(self,key,key_modifiers):
        print("Key went up " + str(key) + " with modifier/s " + str(key_modifiers))
        
class DummyMouseButtonListener(mouse_button_listeners.MouseButtonListener):
    
    def button_down(self,button):
        if (button==mouse_button_listeners.LEFT_BUTTON):
            print("Left mouse button - down!")
        elif (button==mouse_button_listeners.RIGHT_BUTTON):
            print("Right mouse button - down!")
        elif (button==mouse_button_listeners.MIDDLE_BUTTON):
            print("Middle mouse button - down!")
        elif (button==mouse_button_listeners.SCROLL_WHEEL_DOWN):
            print("Scroll wheel down - down!")
        else:
            print("Scroll wheel up - down!")
            
    def button_up(self,button):
        if (button==mouse_button_listeners.LEFT_BUTTON):
            print("Left mouse button - up!")
        elif (button==mouse_button_listeners.RIGHT_BUTTON):
            print("Right mouse button - up!")
        elif (button==mouse_button_listeners.MIDDLE_BUTTON):
            print("Middle mouse button - up!")
        elif (button==mouse_button_listeners.SCROLL_WHEEL_DOWN):
            print("Scroll wheel down - up!")
        else:
            print("Scroll wheel up - up!")

class DummyMouseMotionListener(mouse_motion_listeners.MouseMotionListener):
    
    def mouse_moved(self,mouse_position):
        print("Mouse moved to " + str(mouse_position))

def run():
    current_milli_time = lambda: int(round(time.time() * 1000))
    '''Run the application!!! (For test purposes)'''
    tree = rect_tree.RectangleTree((500,1000))
    tree.insert_rectangle((35,5,50,20,None))
    tree.insert_rectangle((30,5,50,20,None))
    tree.remove_rectangle((35,5,50,20,None))
    tree.remove_rectangle((30,5,50,20,None))
    tree.remove_rectangle((35,5,50,20,None))
    '''Initialise the picture handler!'''
    screen.Screen.initialise("My game")
    picture_handler.PictureHandler.initialise()
    #Create a keyboard listener...
    DummyKeyListener([pygame.locals.K_ESCAPE])
    DummyMouseButtonListener()
    #DummyMouseMotionListener()
    #Start the game loop!
    screen.Screen.start_game_loop()