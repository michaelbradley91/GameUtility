'''
Created on 16 May 2014

@author: michael
'''

import mjb.dev.game_utility.graphics.screen as screen, pygame.locals

class KeyboardListener(object):
    '''
    The keyboard listener will receive all key up and key down events that it registers for.
    There are many keys, so you are asked to register for specific keys via a list.
    Any subclass should call the super constructor!
    '''

    def __init__(self, keys):
        '''
        Construct a new keyboard listener. This will automatically be registered to the screen
        @param keys: the list of keys you intend to listen to for events (either up or down)
        '''
        self.is_registered = False
        self.handler = screen._KeyboardListener(keys,self.__handle_event)
        self.register()
    
    def register(self):
        '''
        Register this listener to the screen to hear keyboard events
        (Has no effect if already registered)
        '''
        if not self.is_registered:
            self.is_registered = True
            self.handler.register()
    
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
        Private method to handle the keyboard event from the screen
        @param event: the event to handle
        '''
        if (event.type == pygame.locals.KEYDOWN):
            self.key_down(event.key,pygame.key.get_mods())
        elif (event.type == pygame.locals.KEYUP):
            self.key_up(event.key,pygame.key.get_mods())
        
    def key_down(self, key, key_modifiers):
        '''
        Called when a key is pressed for the first time (only once - not continually while held)
        @param key: the key that was pushed down
        @param key_modifiers: any modifiers (shift etc) pressed when the key was pressed
        '''
        pass
    
    def key_up(self, key, key_modifiers):
        '''
        Called when a key is released
        @param key: the key that was released
        @param key_modifiers: any modifiers (shift etc) pressed while the key was released
        '''
        pass
    