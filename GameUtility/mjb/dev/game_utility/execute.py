'''
Created on 4 Jul 2014

@author: michael
'''
import mjb.dev.game_utility.graphics.screen as screen
import mjb.dev.game_utility.input_listeners.keyboard_listener as key_listeners
import mjb.dev.game_utility.input_listeners.mouse_button_listener as mouse_button_listeners
import mjb.dev.game_utility.input_listeners.mouse_motion_listener as mouse_motion_listeners
import mjb.dev.game_utility.graphics.picture_handler as picture_handler
import pygame.locals
import mjb.dev.game_utility.collisions.large_rectangle_tree as rect_tree
import mjb.dev.game_utility.utility.rectangle_filler as rect_filler
import mjb.dev.game_utility.graphics.drawers.rectangle_drawer as rectangle_drawer
import mjb.dev.game_utility.input_listeners.frame_listener as frame_listeners
import time
import mjb.dev.game_utility.test_bed as test_bed
import mjb.dev.game_utility.graphics.image as image

class DummyKeyListener(key_listeners.KeyboardListener,frame_listeners.FrameListener):
    
    def __init__(self, keys):
        #Initialise both keys...
        key_listeners.KeyboardListener.__init__(self,keys)
        frame_listeners.FrameListener.__init__(self)
    
    #A rectangle to play with
    def start(self):
        self.rectangle = rectangle_drawer.RectangleDrawer((5,5,100,100),(255,0,0),10)
        rectangle_drawer.RectangleDrawer((220,200,70,30),(0,255,0),20)
        rectangle_drawer.RectangleDrawer((280,210,50,40),(0,0,255),5)
        rectangle_drawer.RectangleDrawer((260,205,100,10),(255,0,255),12)
        for x in range(0,100):
            rectangle_drawer.RectangleDrawer((220+(x*2),400+(x*2),70,30+(x*1)),(x*1,255-(x*1),0),20)
        self.key_UP = False
        self.key_DOWN = False
        self.key_LEFT = False
        self.key_RIGHT = False
    
    def key_down(self,key,key_modifiers):
        #print("Key went down: " + str(key) + " with modifier/s " + str(key_modifiers))
        if key==pygame.locals.K_ESCAPE:
            #Exit
            print("Trying to quit")
            screen.Screen.quit_game()
        if key==pygame.locals.K_LEFT:
            self.key_LEFT = True
        if key==pygame.locals.K_RIGHT:
            self.key_RIGHT = True
        if key==pygame.locals.K_UP:
            self.key_UP = True
        if key==pygame.locals.K_DOWN:
            self.key_DOWN = True
            
    def key_up(self,key,key_modifiers):
        #print("Key went up " + str(key) + " with modifier/s " + str(key_modifiers))
        if key==pygame.locals.K_LEFT:
            self.key_LEFT = False
        if key==pygame.locals.K_RIGHT:
            self.key_RIGHT = False
        if key==pygame.locals.K_UP:
            self.key_UP = False
        if key==pygame.locals.K_DOWN:
            self.key_DOWN = False
    
    def frame_passed(self):
        if self.key_LEFT:
            #Move the rectangle
            self.rectangle.move_rectangle(x_move=-1)
        if self.key_RIGHT:
            #Move the rectangle
            self.rectangle.move_rectangle(x_move=1)
        if self.key_UP:
            #Move the rectangle
            self.rectangle.move_rectangle(y_move=-1)
        if self.key_DOWN:
            #Move the rectangle
            self.rectangle.move_rectangle(y_move=1)
        
class DummyMouseButtonListener(mouse_button_listeners.MouseButtonListener):
    
    def button_down(self,button):
        if (button==mouse_button_listeners.LEFT_BUTTON):
            pass
            #print("Left mouse button - down!")
        elif (button==mouse_button_listeners.RIGHT_BUTTON):
            pass
            #print("Right mouse button - down!")
        elif (button==mouse_button_listeners.MIDDLE_BUTTON):
            pass
            #print("Middle mouse button - down!")
        elif (button==mouse_button_listeners.SCROLL_WHEEL_DOWN):
            pass
            #print("Scroll wheel down - down!")
        else:
            pass
            #print("Scroll wheel up - down!")
            
    def button_up(self,button):
        if (button==mouse_button_listeners.LEFT_BUTTON):
            pass
            #print("Left mouse button - up!")
        elif (button==mouse_button_listeners.RIGHT_BUTTON):
            pass
            #print("Right mouse button - up!")
        elif (button==mouse_button_listeners.MIDDLE_BUTTON):
            pass
            #print("Middle mouse button - up!")
        elif (button==mouse_button_listeners.SCROLL_WHEEL_DOWN):
            pass
            #print("Scroll wheel down - up!")
        else:
            #print("Scroll wheel up - up!")
            pass

class DummyMouseMotionListener(mouse_motion_listeners.MouseMotionListener):
    
    def mouse_moved(self,mouse_position):
        pass
        #print("Mouse moved to " + str(mouse_position))

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
    
    screen.Screen.initialise("My game",(100,100,100),max_frame_rate=60)
    picture_handler.PictureHandler.initialise()
    #Create a keyboard listener...
    
    key_listener = DummyKeyListener([pygame.locals.K_ESCAPE,
                                     pygame.locals.K_LEFT,
                                     pygame.locals.K_RIGHT,
                                     pygame.locals.K_UP,
                                     pygame.locals.K_DOWN])
    
    key_listener.start()
    DummyMouseButtonListener()
    DummyMouseMotionListener()
    #Start the game loop!
    screen.Screen.start_game_loop()
    #Test it out...
    '''
    my_surface = pygame.Surface((6,6))
    invisible = (255,0,0)
    my_surface.set_colorkey(invisible,pygame.locals.RLEACCEL)
    print("Got color key " + str(my_surface.get_colorkey()))
    print("Got pixel at " + str(my_surface.get_at((3,3))))
    my_surface.fill((128,128,128))
    print("Got pixel at " + str(my_surface.get_at((3,3))))
    
    #Blank out part of the surface...
    my_surface.fill(invisible,(3,0,6,6))
    print("Got pixel at " + str(my_surface.get_at((3,3))))
    print("Is colour key? " + str(my_surface.get_at((3,3))==my_surface.get_colorkey()))
    my_image = image.Image(my_surface)
    precision = 1
    print("Covering rect " + str(my_image._calculate_rectangle_approximation(precision)))
    '''
    #test_bed.run()
    