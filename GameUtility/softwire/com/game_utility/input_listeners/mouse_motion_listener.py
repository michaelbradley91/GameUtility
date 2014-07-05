'''
Created on 16 May 2014

@author: michael
'''

import softwire.com.game_utility.graphics.screen as screen
import pygame

def get_mouse_position():
    '''
    @return: the current mouse position (especially important during initialisation. Otherwise, it can be tracked with a mouse
    motion listener)
    '''
    return pygame.mouse.get_pos()

class MouseMotionListener(object):
    '''
    The mouse motion listener hears any changes to the mouse position!
    
    Technical note:
    pygame.event.get(): can return multiple motion events if the code is running slowly, since it returns the entire queue!
    Only the current mouse position is returned by this event, so only one motion event per call to this method will actually be considered.
    '''
    
    def __init__(self):
        '''
        Construct a new mouse motion listener. This will hear any mouse motion events!
        It is automatically registered
        '''
        self.is_registered = False
        self.handler = screen._MouseMotionListener(self.__handle_event)
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
        Private method to handle the mouse motion event from the screen
        @param event: the event to handle
        '''
        self.mouse_moved(pygame.mouse.get_pos())
            
    def mouse_moved(self,mouse_position):
        '''
        Triggered whenever the mouse changes position on the screen. mouse_position returns the current position of the mouse.
        (If you want the relative position - record it yourself! :)) If this event is handled slowly, then mouse motion events
        could build up in the queue. Handle it quickly!!
        @param mouse_position: the position of the mouse
        '''
        pass