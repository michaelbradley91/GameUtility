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
    size = (50,50)
    (width,height) = size
    rect_collider = make_rect_collider(size)
    #Add a lot of rectangles...
    rect_list = []
    for x in range(0,(width/2)-1):
        for y in range(0,(height/2)-1):
            rect_list.append((x*2,y*2,(x+1)*2,(y+1)*2,None))
    #Add the rectangles
    for rect in rect_list:
        rect_collider.insert_rectangle(rect)
    #Now collide some rectangles!
    test_collision_check((5,2,30,30),test_case, size, rect_list, rect_collider)
    #Outside the rectangle
    test_collision_check((19,height,20,height+1),test_case, size, rect_list, rect_collider)
    #Arbitrary
    test_collision_check((18,5,30,45),test_case, size, rect_list, rect_collider)
    #Whole screen
    test_collision_check((0,0,width,height),test_case, size, rect_list, rect_collider)
    #Too thin
    test_collision_check((2,4,2,9),test_case, size, rect_list, rect_collider)
    #Good!

def test_collision_check(rect, test_case, size, rect_list, rect_collider):
    '''
    Perform acollision check!
    @param rect: the colliding rectangle
    @param test_case: the test case running this method
    @param size: the size of the collider's screen
    @param rect_list: the list of rectangles in the collider
    @param rect_collider: the collider itself!
    '''
    res = rect_collider.collide_rectangle(rect)
    #Convert to set...
    res_set = set()
    for temp_rect in res:
        res_set.add(temp_rect)
    correct = collision_check(rect,size,rect_list)
    #Convert to set...
    correct_set = set()
    for temp_rect in correct:
        correct_set.add(temp_rect)
    test_case.assertTrue(res_set==correct_set)
    #Check boolean value
    res = rect_collider.is_colliding(rect)
    test_case.assertTrue(res==(collision_check(rect,size,rect_list)!=[]))
    #Done

#This is bordering on too complex for a test, but I'm sure it is ok...
def collision_check(rect,size,rect_list):
    '''
    Returns the list of rectangles from rect_list which are colliding with the given rectangle
    @param rect: the rectangle to collide against
    @param size: the size of the screen we are colliding against
    @param rect_list: the rectangles to collide rect with
    @return: the list of rectangles in rect_list colliding with rect.
    '''
    (x_min,y_min,x_max,y_max) = rect
    (width,height) = size
    if x_max<=0 or y_max<=0 or x_min>=width or y_min>=height:
        return [] #not in the screen
    if x_max==x_min or y_max==y_min:
        return [] #too thin!
    #Now go through the list...
    res = []
    for (r_x_min,r_y_min,r_x_max,r_y_max,_) in rect_list:
        if x_max>r_x_min and x_min<r_x_max and y_max>r_y_min and y_min<r_y_max:
            res.append((r_x_min,r_y_min,r_x_max,r_y_max,_))
    return res