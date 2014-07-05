'''
Created on 16 May 2014

@author: michael
'''

import softwire.com.game_utility.graphics.screen as screen
import pygame.locals

'''
Value of the left mouse button
'''
LEFT_BUTTON = 1
'''
Value of the middle mouse button
'''
MIDDLE_BUTTON = 2
'''
Value of the right mouse button
'''
RIGHT_BUTTON = 3
'''
Value when the scroll wheel is rolled up
'''
SCROLL_WHEEL_UP = 4
'''
Value when the scroll wheel is rolled down
'''
SCROLL_WHEEL_DOWN = 5


class MouseButtonListener(object):
    '''
    The mouse button listener hears all mouse button presses!
    '''


    def __init__(self):
        '''
        Construct a new mouse button listener. This will hear any mouse button events!
        It is automatically registered
        '''
        self.is_registered = False
        self.handler = screen._MouseButtonListener(self.__handle_event)
        self.register()
        
    def register(self):
        '''
        Register this mouse button listener to hear any mouse button events.
        If this is already registered, this will have no effect
        '''
        if not self.is_registered:
            self.handler.register()
            self.is_registered = True
    
    def deregister(self):
        '''
        Deregister this listener from the screen
        (Has no effect if already deregistered)
        '''
        if self.is_registered:
            self.handler.deregister()
            self.is_registered = False
    
    def __handle_event(self,event):
        '''
        Private method to handle the mouse button event from the screen
        @param event: the event to handle
        '''
        if (event.type == pygame.locals.MOUSEBUTTONDOWN):
            self.button_down(event.button)
        elif (event.type == pygame.locals.MOUSEBUTTONUP):
            self.button_up(event.button)
    
    def button_down(self, button):
        '''
        Triggered when a mouse button is pushed down. Note that if a scroll wheel is turned,
        then the button will be considered down while it starts turning. (Use the constants of this class
        to check which button this really is!)
        @param button: the button that was pushed down
        '''
        pass
    
    def button_up(self, button):
        '''
        Triggered when a mouse button is released. Note that if a scroll wheel is turned,
        then the button will be considered released when it stops turning. (Use the constants of this class
        to check which button this really is!)
        @param button: the button that was released
        '''
        pass