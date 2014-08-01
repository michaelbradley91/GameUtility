'''
Created on 22 Jul 2014

@author: michael
'''

class ImageController(object):
    '''
    I'm re-factoring the project quite a lot after several thoughts...
    
    
    '''
    
    def save_current_image_data(self):
        '''
        Save the current image data in memory. This is useful for storing transformations
        of the image on the fly. This is in RAM, so don't do it too often
        (this does not write to a file or anything).
        If a transformation of an image is stored in RAM, and that transformation
        is needed again, it will be loaded much more quickly! (Along with
        collision stuff probably...not implemented yet).
        It is not worth doing if the image is never transformed.
        
        @return: a key representing what was saved. It is saved statically
        so all drawers can access this saved image.
        '''
        pass
    
    @staticmethod
    def forget_image_data(key):
        '''
        Forget a saved image. This is important for freeing up memory.
        @param key: the key that was received when the image was saved. (Keep it!)
        '''
        pass
    
    @staticmethod
    def forget_all_image_data():
        '''
        Forget all of the saved image data. This is quite brutal, but useful
        if you lost your keys!
        (It is a lot faster than iterating over all the keys though).
        If you don't know what I mean by keys, hopefully you didn't save any images,
        in which case there is nothing to forget. Images are not saved like
        this by default.
        '''
        pass
        