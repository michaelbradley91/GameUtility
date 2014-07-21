'''
Created on 4 Jul 2014

@author: michael
'''

import pygame.locals
import collections
import threading
import sys, traceback

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

class _PictureHandler(object):
    '''
    Anything trying to set itself as a picture handler should inherit from this class.
    '''
    
    def __init__(self):
        '''
        Construct a new picture handler
        '''
        pass
    
    def get_picture(self):
        '''
        By default, this returns the background image.
        @return: (picture, update_list) - the picture to be displayed on screen
        and a list of rectangles to update the screen.
        Note that no explicit handling of the background
        is performed here, so it will appear exactly as is.
        '''
        return Screen._background
    
    def picture_drawn(self):
        '''
        Called once the picture has been blit to the screen, ensuring the handler can now make
        modifications again
        '''

class Screen(object):
    '''
    The screen is where the graphics are actually drawn to.
    For now, we'll assume the user always wants full screen because that is a lot simpler...
    '''
    
    #Remember if the screen was created already
    __created_screen = False
    #Again, the game loop can't be started more than once.
    __started_game_loop = False
    #Remember the various parameters... these are the defaults
    _background_colour = (255,255,255)
    __max_frame_rate = 60
    __game_caption = ""
    __mouse_visible=True
    #Remember the screen object
    __screen = None
    #This the primary background on which everything is drawn! This is eventually blit to the screen itself.
    _background = None
    #This is the clock which controls the max frame rate
    __clock = None
    #The update list. This controls which parts of the screen are actually updated
    __update_list = []
    
    #These are the input listeners attached to the screen
    __keyboard_listeners = collections.defaultdict(lambda : None)
    __mouse_motion_listeners = set()
    __mouse_button_listeners = set()
    
    #These are the sets of listeners to be removed or added
    _keyboard_listeners_to_remove = set()
    _keyboard_listeners_to_add = collections.defaultdict(lambda : None)
    _mouse_motion_listeners_to_remove = set()
    _mouse_motion_listeners_to_add = set()
    _mouse_button_listeners_to_remove = set()
    _mouse_button_listeners_to_add = set()
    
    #A lock for synchronisation on all methods...
    _lock = threading.Lock()
    
    #Flag for when the game has been quit
    __must_quit = False
    
    #The default picture handler
    __picture_handler = _PictureHandler()
    
    @staticmethod
    def get_game_caption():
        '''
        @return: the game caption in use
        '''
        return Screen.__game_caption
    
    @staticmethod
    def get_background_colour():
        '''
        @return: the background colour originally set for this screen
        '''
        return Screen._background_colour
    
    @staticmethod
    def get_frame_rate():
        '''
        @return: the maximum frame rate that this screen is running at
        '''
        return Screen.__max_frame_rate
    
    @staticmethod
    def get_mouse_visible():
        '''
        @return: whether or not the mouse is visible on this screen
        '''
    
    @staticmethod
    def get_screen_size():
        '''
        @return: the size of the screen
        '''
        return Screen.__screen.get_size()

    @staticmethod
    def initialise(game_caption="",
                   background_colour=(255,255,255), max_frame_rate=60,
                   mouse_visible=True):
        '''
        Create a new screen. Note that you can only eve create a single screen in an application.
        @param game_caption: set the caption to appear for this game.
        @param background_colour: set the background colour of the screen.
        @param max_frame_rate: set the maximum frame rate that the game can run at.
        @param mouse_visible: whether or not the mouse should be visible on screen.
        @raise ValueError: if the screen was already initialised
        '''
        Screen._lock.acquire()
        if Screen.__created_screen:
            Screen._lock.release()
            raise ValueError("Screen already initialised. You cannot initialise the screen twice")
        try:
            #Remember the parameters...
            Screen.__game_caption = game_caption
            Screen._background_colour = background_colour
            Screen.__max_frame_rate = max_frame_rate
            Screen.__mouse_visible = mouse_visible
            #Initialise pygame with the given parameters
            Screen.__initialise_pygame()
            #Successfully constructed the screen
            Screen.__created_screen = True
            Screen._lock.release()
        except Exception, e:
            Screen._lock.release()
            Screen.__quit_game(e)
    
    @staticmethod
    def __initialise_pygame():
        '''
        Initialise pygame with the various settings passed in.
        '''
        #Initialise pygame appropriately
        pygame.init()
        #Determines the size of the screen
        Screen.__screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        #Set the caption for the game
        pygame.display.set_caption(Screen.__game_caption)
        #Make the mouse visible
        pygame.mouse.set_visible(Screen.__mouse_visible)
        #Set the background colour
        Screen._background = pygame.Surface(Screen.__screen.get_size())
        Screen._background = Screen._background.convert()
        Screen._background.fill(Screen._background_colour)
        #Display the background.
        Screen.__screen.blit(Screen._background, (0, 0))
        pygame.display.update()
        #Get the game clock
        Screen.__clock = pygame.time.Clock()
        return
    
    @staticmethod
    def start_game_loop():
        '''
        Signal to the screen to start the game loop. Note that this method will not terminate
        until the game terminates. The screen must be initialised first.
        @raise ValueError: if the screen was not initialised successfully.
        '''
        Screen._lock.acquire()
        if not Screen.__created_screen:
            Screen._lock.release()
            raise ValueError("Screen must be initialised successfully first before the game loop can begin")
        if Screen.__started_game_loop:
            Screen._lock.release()
            raise ValueError("The game loop cannot be started more than once")
        Screen.__started_game_loop = True
        Screen._lock.release()
        try :
            #Main game while loop
            while True:
                Screen.__clock.tick(Screen.__max_frame_rate)
                #Remember if we registered a mouse motion event already...
                heard_mouse_motion = False
                #Handle Input Events
                for event in pygame.event.get():
                    if event.type == pygame.locals.QUIT:
                        Screen.__quit_game()
                        return
                    elif event.type == pygame.locals.KEYDOWN or event.type == pygame.locals.KEYUP:
                        #Keyboard listeners
                        for listener in Screen.__keyboard_listeners.keys():
                            #Is it listening for this key?
                            if event.key in Screen.__keyboard_listeners[listener]:
                                listener.handle_event(event)
                    elif event.type == pygame.locals.MOUSEMOTION and not heard_mouse_motion:
                        heard_mouse_motion = True
                        #Mouse motion listeners
                        for listener in Screen.__mouse_motion_listeners:
                            listener.handle_event(event)
                    elif event.type == pygame.locals.MOUSEBUTTONDOWN or event.type == pygame.locals.MOUSEBUTTONUP:
                        #Mouse button listeners
                        for listener in Screen.__mouse_button_listeners:
                            listener.handle_event(event)
                # Update the screen according to the update list
                Screen._lock.acquire()
                try:
                    #Remember the updates...
                    print("Trying to get updates")
                    (picture, updates) = Screen.__picture_handler.get_picture()
                    print("Got updates")
                    Screen.__update_list = updates
                    Screen.__screen.blit(picture, (0,0))
                    Screen.__picture_handler.picture_drawn()
                except Exception, e:
                    Screen._lock.release()
                    Screen.__quit_game(e)
                    return
                Screen._lock.release()
                #Now, lock onto the screen and perform all the various updates...
                should_quit = Screen.__manage_updates()
                if should_quit:
                    #Done
                    return
        except Exception, e:
            Screen.__quit_game(e)
            return
    
    @staticmethod
    def set_picture_handler(picture_handler):
        '''
        Set the picture handler. The picture handler must return the image to be blitted
        to the screen. It should be an instance of picture handler in this file.
        This cannot be called after the game loop has started.
        @param picture_handler: the picture handler to generate the image
        @raise ValueError: if the game loop has been started
        '''
        if Screen.__started_game_loop:
            raise ValueError("Cannot set the picture handler after the game loop has started")
        Screen.__picture_handler = picture_handler
        return
        
    @staticmethod
    def __manage_updates():
        '''
        Handles all updates to the screen (after inputs have been handled).
        Updates include changes to the background, and changes in the listeners.
        '''
        try:
            Screen._lock.acquire()
            pygame.display.update(Screen.__update_list)
            Screen.__update_list = []
            #Register and deregister listeners...
            for listener in Screen._keyboard_listeners_to_add.keys():
                Screen.__keyboard_listeners[listener] = Screen._keyboard_listeners_to_add[listener]
            for listener in Screen._keyboard_listeners_to_remove:
                Screen.__keyboard_listeners.pop(listener)
            for listener in Screen._mouse_button_listeners_to_add:
                Screen.__mouse_button_listeners.add(listener)
            for listener in Screen._mouse_button_listeners_to_remove:
                Screen.__mouse_button_listeners.remove(listener)
            for listener in Screen._mouse_motion_listeners_to_add:
                Screen.__mouse_motion_listeners.add(listener)
            for listener in Screen._mouse_motion_listeners_to_remove:
                Screen.__mouse_motion_listeners.remove(listener)
            #Empty the lists...
            Screen._keyboard_listeners_to_add.clear()
            Screen._keyboard_listeners_to_remove.clear()
            Screen._mouse_button_listeners_to_add.clear()
            Screen._mouse_button_listeners_to_remove.clear()
            Screen._mouse_motion_listeners_to_add.clear()
            Screen._mouse_motion_listeners_to_remove.clear()
            #See if we need to quit...
            if Screen.__must_quit:
                Screen._lock.release()
                Screen.__quit_game()
                return True
            Screen._lock.release()
            return False
        except Exception, e:
            Screen._lock.release()
            Screen.__quit_game(e)
            return True
    
    @staticmethod
    def __quit_game(exception=None):
        '''
        Quit the game.
        @param exception: if this is not None, it will be raised after an appropriate termination
        '''
        pygame.quit()
        #If there was no exception, quit calmly, but otherwise re-raise
        if not exception==None:
            # Print the error and quit
            tb = sys.exc_info()[2]
            traceback.print_exception(exception.__class__, exception, tb)
            raise exception
        
    @staticmethod
    def quit_game():
        '''
        Call this to quit the game. Calling this multiple times has no effect,
        but the game may receive additional input after this has been called for a short time.
        '''
        Screen._lock.acquire()
        Screen.__must_quit = True
        Screen._lock.release()
        
'''
Synchronisation between listeners and the screen is quite a serious problem.
We need to ensure that listeners can register and de-register themselves roughly whenever they
like, which means in parallel with the game loop. This must not potentially lock with the screen.

It might be best to use the lock outside the game loop. Instead, the game loop is entirely asynchronous,
and the listeners synchronise against each other when trying to add and remove themselves. They add themselves
to a removal set when they seek to be removed. When the game loop completes, it checks all of the listeners
who have added themselves to either the add set or the removal set (note that if adding and removing takes
place, the listener will be held responsible not to appear in both sets).

Ok... let's do that!
'''
        
class _KeyboardListener(object):
    '''
    A "private" version of the keyboard listener class. You are not meant to subclass this class!! (or use it...)
    There's a lot for the screen to handle, so this is just a skeleton class
    '''

    def __init__(self, keys, event_handler):
        '''
        Create a keyboard listener ready to listen for the specified list of keys
        @param keys: a list of keys to listen to. The keys should be specified as in pygame.locals
        @param event_handler: the method to be called when an event is received
        '''
        self.event_handler = event_handler
        self.key_set = set()
        for key in keys:
            self.key_set.add(key)
        
    def register(self):
        '''
        Register this listener to the screen
        '''
        Screen._lock.acquire()
        if self in Screen._keyboard_listeners_to_remove:
            Screen._keyboard_listeners_to_remove.remove(self)
        Screen._keyboard_listeners_to_add[self] = self.key_set
        Screen._lock.release()
        
    def deregister(self):
        '''
        Deregister this listener from the screen (don't deregister twice)
        '''
        Screen._lock.acquire()
        Screen._keyboard_listeners_to_add.pop(self,None)
        Screen._keyboard_listeners_to_remove.add(self)
        Screen._lock.release()
    
    def handle_event(self,event):
        '''
        Handle a keyboard event somehow!
        @param event: the keyboard event (will be for one of the keys you were listening to)
        '''
        self.event_handler(event)

class _MouseMotionListener(object):
    '''
    A "private" version of the mouse motion listener class. You are not meant to subclass this class!! (or use it...)
    There's a lot for the screen to handle, so this is just a skeleton class
    '''

    def __init__(self, event_handler):
        '''
        Create a mouse motion listener
        @param event_handler: the method to be called when an event is received
        '''
        self.event_handler = event_handler
        
    def register(self):
        '''
        Register this listener to the screen
        '''
        Screen._lock.acquire()
        if self in Screen._mouse_motion_listeners_to_remove:
            Screen._mouse_motion_listeners_to_remove.remove(self)
        Screen._mouse_motion_listeners_to_add.add(self)
        Screen._lock.release()
        
    def deregister(self):
        '''
        Deregister this listener from the screen (don't deregister twice)
        '''
        Screen._lock.acquire()
        Screen._mouse_motion_listeners_to_remove.add(self)
        if self in Screen._mouse_motion_listeners_to_add:
            Screen._mouse_motion_listeners_to_add.remove(self)
        Screen._lock.release()
    
    def handle_event(self,event):
        '''
        Handle a mouse motion event somehow!
        @param event: the mouse motion event
        '''
        self.event_handler(event)
    
class _MouseButtonListener(object):
    '''
    A "private" version of the mouse button listener class. You are not meant to subclass this class!! (or use it...)
    There's a lot for the screen to handle, so this is just a skeleton class
    '''

    def __init__(self, event_handler):
        '''
        Create a mouse button listener
        @param event_handler: the method to be called when an event is received
        '''
        self.event_handler = event_handler
        
    def register(self):
        '''
        Register this listener to the screen
        '''
        Screen._lock.acquire()
        if self in Screen._mouse_button_listeners_to_remove:
            Screen._mouse_button_listeners_to_remove.remove(self)
        Screen._mouse_button_listeners_to_add.add(self)
        Screen._lock.release()
        
    def deregister(self):
        '''
        Deregister this listener from the screen (don't deregister twice)
        '''
        Screen._lock.acquire()
        Screen._mouse_button_listeners_to_remove.add(self)
        if self in Screen._mouse_button_listeners_to_add:
            Screen._mouse_button_listeners_to_add.remove(self)
        Screen._lock.release()
    
    def handle_event(self,event):
        '''
        Handle a mouse motion event somehow!
        @param event: the mouse motion event
        '''
        self.event_handler(event)
        