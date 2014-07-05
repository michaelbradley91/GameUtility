'''
Created on 5 Jul 2014

@author: michael
'''

import softwire.com.game_utility.graphics.screen as screen
import pygame
import threading

class DummyPictureHandler(screen._PictureHandler):
    '''
    This handler just passes the calls to the static class
    '''
    def __init__(self):
        pass

    def get_picture(self):
        return PictureHandler._get_picture()
    
    def picture_drawn(self):
        PictureHandler._picture_drawn()

class PictureHandler(object):
    '''
    This class handles how things are drawn to the screen.
    The class ensures that images can be moved around on screen, and expect overlapping to be managed
    correctly.
    '''
        
    #The dummy picture handler to link with the screen
    __handler = DummyPictureHandler()
    #Stats about the screen, held here for convenience
    __background_colour = None
    __size = None
    #Whether or not the PictureHandler has been initialised
    __initialised = False
    #The picture being blitted
    __picture = None
    #The lock held on the picture when it is modified
    __picture_lock = threading.Semaphore()
    
    @staticmethod
    def initialise():
        '''
        Initialise the picture handler. This should be done strictly after the screen has been
        initialised, and strictly before any requests are made to the picture handler.
        This should only be called once
        '''
        if PictureHandler.__initialised:
            raise ValueError("Cannot initialise the picture handler more than once")
        #Remember some stats about the screen
        PictureHandler.__background_colour = screen.Screen.get_background_colour()
        PictureHandler.__size = screen.Screen.get_screen_size()
        #Initialise the picture
        PictureHandler.__picture = pygame.Surface(PictureHandler.__size)
        PictureHandler.__picture = PictureHandler.__picture.convert()
        PictureHandler.__picture.fill(PictureHandler.__background_colour)
        #Assign self as the picture handler
        screen.Screen.set_picture_handler(PictureHandler.__handler)
        #Remember we did this!
        PictureHandler.__initialised = True
        
    @staticmethod
    def _get_picture():
        PictureHandler.__picture_lock.acquire()
        #Fixing git
        return PictureHandler.__picture
    
    @staticmethod
    def _picture_drawn():
        PictureHandler.__picture_lock.release()
        return
        
    