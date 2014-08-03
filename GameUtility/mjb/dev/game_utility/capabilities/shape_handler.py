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

    def __init__(self, shape, depth, bounding_rectangle):
        '''
        Construct a new shape handler. A shape handler enables capabilities to be added to shape
        calculators. (You must call this constructor if you subclass this)
        @param shape: the shape used when capabilities are added.
        @param depth: the depth that this shape handler should consider its shape to be at.
        (will be augmented with a tie-breaking unique id)
        @param bounding_rectangle: a bounding rectangle for the shape, which should be wide and high enough
        to completely contain the shape's calculations of itself. The bounding rectangle's top left
        coordinate represents the top left coordinate of the shape on screen.
        '''
        self.__shape = shape
        self.__bounding_rectangle = bounding_rectangle
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
    
    def set_shape(self,shape, bounding_rectangle=None, depth=None):
        '''
        @param shape: the shape this handler should now use.
        @param bounding_rectangle: the bounding rectangle to use with the new shape.
        I the shape has changed size, it is important to set this to keep it consistent. None will
        leave the bounding rectangle unchanged.
        @param depth: the depth to use with the new shape. None will leave the depth unchanged.
        '''
        if ((shape==self.__shape) and
            (depth==None or self.__depth==depth) and
            (bounding_rectangle==None or self.__bounding_rectangle==bounding_rectangle)):
            #Nothing changed
            return
        #Tell the handlers what is happening before the update...
        self.__prior_update(ShapeHandler._SHAPE_UPDATE)
        if depth!=None:
            self.__depth = depth
        if bounding_rectangle!=None:
            self.__bounding_rectangle = bounding_rectangle
        self.__shape = shape
        #and update them...
        self.__post_update(ShapeHandler._SHAPE_UPDATE)
    
    def get_bounding_rectangle(self):
        '''
        @return: a single rectangle covering the whole shape in the form of (x_min,y_min,x_max,y_max)
        '''
        return self.__bounding_rectangle
        
    def set_bounding_rectangle(self, bounding_rectangle):
        '''
        @param bounding_rectangle: the new bounding rectangle to use.
        '''
        if bounding_rectangle==self.__bounding_rectangle:
            return
        #Tell the handlers what is happening before the update...
        self.__prior_update(ShapeHandler._BOUNDING_RECTANGLE_UPDATE)
        self.__bounding_rectangle = bounding_rectangle
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