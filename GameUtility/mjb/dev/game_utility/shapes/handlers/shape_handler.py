'''
Created on 1 Aug 2014

@author: michael
'''

import threading

class ShapeHandler(object):
    '''
    The shape handler enables capabilities to be added to shapes.
    A capability makes use of the shape only.
    The shape handler also holds a unique id to break ties in the depth, and thus provides
    a consistency in the depth if the shape handler is kept for the same logical object in the game.
    (I.e.: each logical object should be assigned to one shape handler)
    
    Note to self:
    There were several capabilities that cared about the shape, but none other than
    the drawer cared about actually drawing the shapes on screen. Changes in appearance but not shape
    do not need to be reported to capabilities, so it is handled separately.
    '''
    
    #Constant flags for the updates to capabilities
    _DEPTH_UPDATE = 0
    _BOUNDING_RECTANGLE_UPDATE = 1
    #A shape update means the internal shape has been updated. This should be considered to mean
    #everything has changed, as that is possible.
    _SHAPE_UPDATE = 2
    
    #A static lock for the unique id
    __lock = threading.Semaphore()
    __unique_id = 0

    def __init__(self, shape, depth, top_left):
        '''
        Construct a new shape handler. A shape handler enables capabilities to be added to shape
        calculators. (You must call this constructor if you subclass this)
        @param shape: the shape used when capabilities are added.
        @param depth: the depth that this shape handler should consider its shape to be at.
        (will be augmented with a tie-breaking unique id)
        @param top_left: An (x,y) coordinate representing where the top left of the shape
        should appear on screen (as in the shape will be put into (x,y,width,height) for width
        and height determined by the shape's size)
        '''
        self.__shape = shape
        self.__top_left = top_left
        #Figure out the bounding rectangle for convenience...
        (x,y) = self.__top_left
        (width,height) = self.__shape.get_size()
        self.__bounding_rectangle = (x,y,x+width,y+height)
        self.__depth = depth
        #Set the unique id
        ShapeHandler.__lock.acquire()
        self.__unique_id = ShapeHandler.__unique_id
        ShapeHandler.__unique_id+=1
        ShapeHandler.__lock.release()
        #The capabilities maintained
        self.__capabilities = set()
        
    def get_shape(self):
        '''
        @return: the shape held by this shape handler
        '''
        return self.__shape
    
    def set_shape(self,shape, top_left=None, depth=None):
        '''
        @param shape: the shape this handler should now use.
        @param top_left: the new top left coordinate for this shape. Leave as None (default)
        if you wish for this to remain unchanged
        @param depth: the depth to use with the new shape. None will leave the depth unchanged.
        '''
        if ((shape==self.__shape) and
            (depth==None or self.__depth==depth) and
            (top_left==None or self.__top_left==top_left)):
            #Nothing changed
            return
        #Tell the handlers what is happening before the update...
        self.__prior_update(ShapeHandler._SHAPE_UPDATE)
        self.__shape = shape
        if depth!=None:
            self.__depth = depth
        if top_left!=None:
            self.__top_left = top_left
        #Calculate the bounding rectangle...
        (x,y) = self.__top_left
        (width,height) = self.__shape.get_size()
        self.__bounding_rectangle = (x,y,x+width,y+height)
        #and update them...
        self.__post_update(ShapeHandler._SHAPE_UPDATE)
    
    def get_top_left(self):
        '''
        @return: the top left coordinate where the shape being handled is positioned on screen
        as (x,y)
        '''
        return self.__top_left
    
    def get_bounding_rectangle(self):
        '''
        @return: a single rectangle covering the whole shape in the form of (x_min,y_min,x_max,y_max)
        '''
        return self.__bounding_rectangle
        
    def set_top_left(self, top_left):
        '''
        @param top_left: the new top left coordinate for the shape as (x,y).
        '''
        if top_left==self.__top_left:
            return
        #Tell the handlers what is happening before the update...
        self.__prior_update(ShapeHandler._BOUNDING_RECTANGLE_UPDATE)
        self.__top_left = top_left
        #Update the bounding rectangle...
        (x,y) = self.__top_left
        (width,height) = self.__shape.get_size()
        self.__bounding_rectangle = (x,y,x+width,y+height)
        #and update them...
        self.__post_update(ShapeHandler._BOUNDING_RECTANGLE_UPDATE)
        
    def get_depth(self):
        '''
        @return: a pair of (depth,unique_id) representing the depth at which this image exists.
        If image one has depth x and image two has depth y, if x>y, image one will appear behind image two.
        The unique id should be used to break ties in the same way.
        '''
        return (self.__depth,self.__unique_id)
        
    def set_depth(self, depth):
        '''
        @param depth: the depth of the shape on screen.
        '''
        #Note to self: Nothing ever needs to know the depth has been updated, so this is a waste
        #of time even if it helps the abstraction...
        if self.__depth==depth:
            return
        #Tell the handlers what is happening before the update...
        self.__prior_update(ShapeHandler._DEPTH_UPDATE)
        self.__depth = depth
        #and update them...
        self.__post_update(ShapeHandler._DEPTH_UPDATE)
    
    def __prior_update(self, flag):
        '''
        Tell all of the attached capabilities about the update strictly before anything has changed
        @param flag: a flag signalling what kind of update this is (constants defined in the shape handler)
        '''
        for capability in self.__capabilities:
            capability.prior_update(flag)
    
    def __post_update(self, flag):
        '''
        Tell all of the attached capabilities about the update strictly after everything has been changed
        @param flag: a flag signalling what kind of update this is (constants defined in the shape handler)
        '''
        for capability in self.__capabilities:
            capability.post_update(flag)
    
    def _enable_capability(self, capability):
        '''
        This method is called by the capability itself when it is enabled.
        @param capability: the capability being added
        '''
        self.__capabilities.add(capability)
        
    def _disable_capability(self, capability):
        '''
        This method is called by the capability itself when it is disabled.
        @param capability: the capability being removed
        '''
        self.__capabilities.remove(capability)
    
    def dispose(self):
        '''
        Dispose of this shape handler. You should not use this shape handler
        again once it has been disposed...
        '''
        #For each enabled capability, dispose it!
        for capability in self.__capabilities:
            capability.dispose()
        self.__capabilities.clear()