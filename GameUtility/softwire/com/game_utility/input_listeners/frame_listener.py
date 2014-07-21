'''
Created on 21 Jul 2014

@author: michael
'''

import softwire.com.game_utility.graphics.screen as screen

class FrameListener(object):
    '''
    The frame listener will be called once for every frame that passes. This is useful
    for timing events and other regular updates.
    '''

    def __init__(self):
        '''
        Construct a new frame listener. This will automatically be registered to the screen
        '''
        self.is_registered = False
        self.handler = screen._FrameListener(self.frame_passed)
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
        
    def frame_passed(self):
        '''
        Called whenever a frame passes.
        '''
        pass