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
import softwire.com.game_utility.graphics.picture_handling.rectangle_filler as rect_filler
import softwire.com.game_utility.graphics.drawers.rectangle_drawer as rectangle_drawer
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
    #Test the rectangle filler!
    #print(rect_filler.RectangleFiller.fill_grid([
    #    (0,0),(0,1),(0,2),(1,1),(2,0),(2,1),(2,2)]))
    '''
    tree = rect_tree.RectangleTree((64,64))
    #Test the rectangle tree!
    for x in range(0,32):
        for y in range(0,32):
            tree.insert_rectangle((x*2,y*2,(x+1)*2,(y+1)*2,None))
    #tree.insert_rectangle((6, 8, 8, 10,None))
    #tree.print_tree()
    #Try a collision
    res = tree.collide_rectangle((4,4,16,16,None))
    #tree = rect_tree.RectangleTree((500,1000))
    #tree.insert_rectangle((0,0,5,5,None))
    #tree.insert_rectangle((4,4,7,8,None))
    #tree.insert_rectangle((20,20,26,25,None))
    #Try colliding a rectangle...
    #res = tree.collide_rectangle((0,0,5,5,None))
    print(res); #[0,0,0,0,1,2,2,2]
    '''
    '''Initialise the picture handler!'''
    current_milli_time = lambda: int(round(time.time() * 1000))
    
    screen.Screen.initialise("My game",(100,100,100))
    picture_handler.PictureHandler.initialise()
    #Draw a rectangle!!
    rectangle_drawer.RectangleDrawer((5,5,100,100),(255,0,0))
    #Create a keyboard listener...
    DummyKeyListener([pygame.locals.K_ESCAPE])
    DummyMouseButtonListener()
    #DummyMouseMotionListener()
    #Start the game loop!
    screen.Screen.start_game_loop()
    