'''
Created on 29 Jul 2014

@author: michael
'''

'''
This module contains tests applicable to all of the standard colliders.
The relevant methods are:

def insert_rectangle(self, rect):
def remove_rectangle(self, rect):
def collide_rectangle(self, rect):
def is_colliding(self,rect):
def clear(self):
def __init__(self, size):
'''

def test_add_remove(test_case, make_rect_collider):
    '''
    Test the add and remove methods of a rectangle collider.
    @param test_case: the test case that is being run.
    @param make_rect_collider: a method to construct the rectangle collider. This should
    expect a size parameter.
    '''
    #Firstly, try adding various "simpler" rectangles...
    rect_collider = make_rect_collider((100,200))
    rect_collider.insert_rectangle((5,25,80,30,"key 1"))
    rect_collider.insert_rectangle((5,25,80,30,"key 2"))
    rect_collider.insert_rectangle((25,5,80,30,"key 1"))
    rect_collider.insert_rectangle((25,5,40,30,"key 1"))
    #Check for some fake rectangles
    test_case.assertFalse(rect_collider.remove_rectangle((4,90,40,70,"key 3")))
    test_case.assertFalse(rect_collider.remove_rectangle((5,25,80,31,"key 1")))
    #Now check that they were there...
    test_case.assertTrue(rect_collider.remove_rectangle((5,25,80,30,"key 1")))
    test_case.assertFalse(rect_collider.remove_rectangle((5,25,80,30,"key 1")))
    test_case.assertTrue(rect_collider.remove_rectangle((5,25,80,30,"key 2")))
    test_case.assertFalse(rect_collider.remove_rectangle((5,25,80,30,"key 2")))
    test_case.assertTrue(rect_collider.remove_rectangle((25,5,80,30,"key 1")))
    test_case.assertFalse(rect_collider.remove_rectangle((25,5,80,30,"key 1")))
    test_case.assertTrue(rect_collider.remove_rectangle((25,5,40,30,"key 1")))
    test_case.assertFalse(rect_collider.remove_rectangle((25,5,40,30,"key 1")))
    #Good enough for this test

def test_clear(test_case, make_rect_collider):
    '''
    Test the clear method of a rectangle collider.
    @param test_case: the test case that is being run.
    @param make_rect_collider: a method to construct the rectangle collider. This should
    expect a size parameter.
    '''
    rect_collider = make_rect_collider((450,200))
    #Insert some stuff...
    rect_collider.insert_rectangle((5,25,80,30,"key 1"))
    rect_collider.insert_rectangle((5,25,80,30,"key 2"))
    rect_collider.insert_rectangle((25,5,80,30,"key 1"))
    rect_collider.insert_rectangle((25,5,40,30,"key 1"))
    #Clear it!
    rect_collider.clear()
    #Check it is empty!
    test_case.assertFalse(rect_collider.remove_rectangle((5,25,80,30,"key 1")))
    test_case.assertFalse(rect_collider.remove_rectangle((5,25,80,30,"key 2")))
    test_case.assertFalse(rect_collider.remove_rectangle((25,5,80,30,"key 1")))
    test_case.assertFalse(rect_collider.remove_rectangle((25,5,40,30,"key 1")))
    #Good!
    
def test_clipping(test_case, make_rect_collider):
    '''
    Test the clipping by the rectangle collider.
    @param test_case: the test case that is being run.
    @param make_rect_collider: a method to construct the rectangle collider. This should
    expect a size parameter.
    '''
    rect_collider = make_rect_collider((50,50))
    #Firstly, make sure that if we add a rectangle which partially fits inside the collider,
    #it will remain inside
    rect_collider.insert_rectangle((-10,-10,1,1,"key"))
    test_case.assertTrue(rect_collider.remove_rectangle((-10,-10,1,1,"key")))
    #Now check that a rectangle inserted outside the collider is ignored.
    rect_collider.insert_rectangle((50,50,51,51,"key"))
    test_case.assertFalse(rect_collider.remove_rectangle((50,50,51,51,"key")))
    #Pretend to swallow the screen...
    rect_collider.insert_rectangle((-5,-5,55,55,"key"))
    test_case.assertTrue(rect_collider.remove_rectangle((-5,-5,55,55,"key")))
    #Add a non-existent rectangle (expect this to be allowed, but ignored)
    rect_collider.insert_rectangle((10,10,10,15,"key"))
    test_case.assertFalse(rect_collider.remove_rectangle((-5,-5,55,55,"key")))
    #Done!
    
def test_collision(test_case, make_rect_collider):
    '''
    Test the collision calculations by the rectangle collider. This is the really
    important stuff!
    @param test_case: the test case that is being run.
    @param make_rect_collider: a method to construct the rectangle collider. This should
    expect a size parameter.
    '''
    rect_collider = make_rect_collider((50,50))