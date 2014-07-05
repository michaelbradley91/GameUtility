'''
Created on 12 May 2014

@author: michael
'''

import pygame, os

class ImageLoader(object):
    '''
    The image loader manages the loading of images into pygame.
    '''
    
    def __init__(self,directory):
        '''
        Construct a new image loader using the given directory. (This can be set freely afterwards)
        @param directory: a directory where images should be loaded from by this loader. Default ""
        '''
        self.directory = directory
    
    def load_image(self,name, colourkey=None):
        '''
        Load an image with the given name into pygame.
        @param name - the name of the file after the image directory
        @param [colourKey] - the colour that should appear transparent in the image (None by default)
        
        @return - the image and its bounding rectangle
        '''
        fullname = os.path.join(self.directory, name)
        try:
            image = pygame.image.load(fullname)
        except pygame.error, message:
            print 'Cannot load image:', name
            raise SystemExit, message
        image = image.convert()
        if colourkey is not None:
            if colourkey is -1:
                colourkey = image.get_at((0,0))
            image.set_colorkey(colourkey, pygame.locals.RLEACCEL)
        return image, image.get_rect()