'''
Created on 3 Aug 2014

@author: michael
'''

class Capability(object):
    '''
    This is just an interface for reference. A capability can be attached to a shape handler
    to detect certain kinds of events.
    Most (maybe all) capabilities will actually be controlled by static classes.
    
    How should this work...
    The shae handler wants an add_capability method, in which you pass in the capability
    and it gets added.
    
    Or you construct a capability and add the shape handler. It can then add the capability
    into its references and update them accordingly. This is probably the best way, as it helps
    to avoid the storing of references, and makes it easier to dispose through the single
    shape handler object.
    '''
    
    def __init__(self, shape_handler, precision, event_handler, enabled=True):
        '''
        A suggested constructor. This should call the capability
        @param shape_handler: the shape handler this is concerned with
        @param precision: the precision at which the capability should use the shape inside the shape
        handler.
        @param event_handler: a method to be called whenever this capability activates.
        @param enabled: true by default, whether or not the capability should be active
        '''
        pass
    
    def get_precision(self):
        '''
        @return: the precision used by this capability
        '''
        pass
    
    def set_precision(self, precision):
        '''
        @param precision: the new precision this capability should use.
        '''
        pass
    
    def prior_update(self, flag):
        '''
        Called strictly before the relevant shape handler updates its state.
        This is a chance for the capability to deregister the handler where appropriate.
        @param flag: a flag stating what is updating (constants held in the shape handler)
        '''
        pass
    
    def post_update(self, flag):
        '''
        Called strictly after the relevant shape handler updates its state.
        This is a chance for the capability to register (again) the handler where appropriate.
        @param flag: a flag stating what is updating (constants held in the shape handler)
        '''
        pass
    
    def enable(self):
        '''
        Enable this capability
        '''
        
    def disable(self):
        '''
        Disable this capability
        '''
        pass
    