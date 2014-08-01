'''
Created on 1 Aug 2014

@author: michael
'''

import collections
import threading

class ShapeHandler(object):
    '''
    
    
    TODO: more as a note to self. It may be worth enabling a sort of auto forget
    feature, where shapes keep track of their handlers, and are only forgotten
    when no more handlers exist.
    '''


    def __init__(self, shape_calculator):
        '''
        Construct a new shape handler. A shape handler enables capabilities to be added to shape
        calculators.
        @param shape_calculator: the (default) shape calculator used when abilities are added.
        '''
        self.__shape_calculator = shape_calculator
    
    #For thread safety
    __lock = threading.Semaphore()
    #The saved shape calculations
    __memorised_calculations = collections.defaultdict(lambda:None)
    #This remembers all of the precisions saved for a particular shape
    __memorised_shape_precisions = collections.defaultdict(lambda:set())
    
    @staticmethod
    def remember_shape_calculation(shape_calculator, precision):
        '''
        Remember the shape calculator's calculated shape (?!) at a particular precision.
        If this precision is requested from any capability again, the calculation can be looked
        up much more quickly and will bypass the shape calculator. (Note that this does not save
        the shape calculator in some sense. You'll want to save images yourself by reusing
        the same references... Since you can only save immutable shape calculators, this is highly
        recommended). It is important to forget saves when you no longer need them!
        @warning: this only makes any difference if the shape calculator is labelled as immutable.
        Otherwise, this call does nothing!! It also does nothing if it was saved previously...
        @param shape_calculator: the shape calculator
        @param precision: the precision that the calculation should be performed at
        '''
        ShapeHandler.__lock.acquire()
        if shape_calculator.is_immutable() and ShapeHandler.__memorised_calculations[(shape_calculator,precision)]==None:
            #Calculate and save
            ShapeHandler.__memorised_shape_precisions[shape_calculator].add(precision)
            ShapeHandler.__memorised_calculations[(shape_calculator,precision)] = shape_calculator.calculate_shape(precision)
        ShapeHandler.__lock.release()
    
    @staticmethod
    def forget_shape_calculation(shape_calculator, precision):
        '''
        @param shape_calculator: the shape calculator whose calculation should be forgotten
        @param precision: the specific precision to be forgotten
        '''
        ShapeHandler.__lock.acquire()
        if ShapeHandler.__memorised_calculations[(shape_calculator,precision)]!=None:
            #Remove the key
            ShapeHandler.__memorised_calculations.pop((shape_calculator,precision))
            #Remove the precision
            ShapeHandler.__memorised_shape_precisions[shape_calculator].remove(precision)
            if len(ShapeHandler.__memorised_shape_precisions[shape_calculator])==0:
                ShapeHandler.__memorised_shape_precisions.pop(shape_calculator)
        ShapeHandler.__lock.release()
        
    @staticmethod
    def forget_shape_calculations(shape_calculator):
        '''
        @param shape_calculator: the shape calculator whose calculations should be forgotten.
        This forgets all of the precisions saved. Typically, this is the recommended forget method to be used,
        as your game will likely not need certain shapes (images usually) in certain sections.
        '''
        ShapeHandler.__lock.acquire()
        precisions = ShapeHandler.__memorised_shape_precisions[shape_calculator]
        if len(precisions)!=0:
            #Remove keys...
            for precision in precisions:
                ShapeHandler.__memorised_calculations.pop((shape_calculator,precision))
            #Remove from the precisions
            ShapeHandler.__memorised_shape_precisions.pop(shape_calculator)
        ShapeHandler.__lock.release()
        
    @staticmethod
    def forget_all_shape_calculations():
        '''
        Forget all shape calculations ever saved. This really does forget everything. Note that
        everything will still function, but if calculations were saved for efficiency things might slow
        down. This will free up memory in an emergency.
        '''
        ShapeHandler.__memorised_shape_precisions.clear()
        ShapeHandler.__memorised_calculations.clear()