'''
Created on 12 May 2014

@author: michael
'''

import pygame, os

class SoundLoader(object):
    '''
    The sound loader manages the loading of sounds into pygame.
    '''
    
    def __init__(self, directory=""):
        '''
        Construct a new sound loader using the given directory. (This can be set freely afterwards)
        @param directory: a directory where sounds should be loaded from by this loader. Default ""
        '''
        self.directory = directory
    
    def load_sound(self,name):
        '''
        Load a sound with the given name in pygame.
        @param name - the name of the file containing the sound, after the sound directory.
        @return the sound loaded into the system!
        '''
        class NoneSound:
            def play(self): pass
        if not pygame.mixer:
            return NoneSound()
        fullname = os.path.join(self.directory, name)
        try:
            sound = pygame.mixer.Sound(fullname)
        except pygame.error, message:
            print 'Cannot load sound:', fullname
            raise SystemExit, message
        return sound