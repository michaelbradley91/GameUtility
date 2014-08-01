'''
Created on 30 Jul 2014

@author: michael
'''
import unittest
from mjb.dev.game_utility.collisions.screen_collider import ScreenCollider
from mjb.dev.game_utility.collisions.simple_rectangle_collider import SimpleRectangleCollider
from mjb.dev.game_utility.collisions.small_rectangle_tree import SmallRectangleTree
from mjb.dev.game_utility.collisions.large_rectangle_tree import LargeRectangleTree


class TestScreenCollider(unittest.TestCase):

    #Test all of the different kinds of rectangle tree inside the screen collider
    rect_make_list = [lambda size: SimpleRectangleCollider(size),
                      lambda size: SmallRectangleTree(size),
                      lambda size: LargeRectangleTree(size)
                      ]
    
    #The first tests are more or less the same as the rectangle collider tests:
    def test_add_remove(self):
        '''
        Test the add and remove methods of a rectangle collider.
        '''
        for x in range(0,len(TestScreenCollider.rect_make_list)):
            #Firstly, try adding various "simpler" rectangles...
            rect_collider = ScreenCollider(TestScreenCollider.rect_make_list[x]((100,200)),lambda _:[],lambda _:None)
            rect_collider.insert_rectangle((5,25,80,30,"key 1"))
            rect_collider.insert_rectangle((5,25,80,30,"key 2"))
            rect_collider.insert_rectangle((25,5,80,30,"key 1"))
            rect_collider.insert_rectangle((25,5,40,30,"key 1"))
            #Check for some fake rectangles
            self.assertFalse(rect_collider.remove_rectangle((4,90,40,70,"key 3")))
            self.assertFalse(rect_collider.remove_rectangle((5,25,80,31,"key 1")))
            #Now check that they were there...
            self.assertTrue(rect_collider.remove_rectangle((5,25,80,30,"key 1")))
            self.assertFalse(rect_collider.remove_rectangle((5,25,80,30,"key 1")))
            self.assertTrue(rect_collider.remove_rectangle((5,25,80,30,"key 2")))
            self.assertFalse(rect_collider.remove_rectangle((5,25,80,30,"key 2")))
            self.assertTrue(rect_collider.remove_rectangle((25,5,80,30,"key 1")))
            self.assertFalse(rect_collider.remove_rectangle((25,5,80,30,"key 1")))
            self.assertTrue(rect_collider.remove_rectangle((25,5,40,30,"key 1")))
            self.assertFalse(rect_collider.remove_rectangle((25,5,40,30,"key 1")))
            #Good enough for this test
    
    def test_clear(self):
        '''
        Test the clear method of a rectangle collider.
        '''
        for x in range(0,len(TestScreenCollider.rect_make_list)):
            rect_collider = ScreenCollider(TestScreenCollider.rect_make_list[x]((450,200)),lambda _:[],lambda _:None)
            #Insert some stuff...
            rect_collider.insert_rectangle((5,25,80,30,"key 1"))
            rect_collider.insert_rectangle((5,25,80,30,"key 2"))
            rect_collider.insert_rectangle((25,5,80,30,"key 1"))
            rect_collider.insert_rectangle((25,5,40,30,"key 1"))
            #Clear it!
            rect_collider.clear()
            #Check it is empty!
            self.assertFalse(rect_collider.remove_rectangle((5,25,80,30,"key 1")))
            self.assertFalse(rect_collider.remove_rectangle((5,25,80,30,"key 2")))
            self.assertFalse(rect_collider.remove_rectangle((25,5,80,30,"key 1")))
            self.assertFalse(rect_collider.remove_rectangle((25,5,40,30,"key 1")))
            #Good!
        
    def test_clipping(self):
        '''
        Test the clipping by the rectangle collider.
        '''
        for x in range(0,len(TestScreenCollider.rect_make_list)):
            rect_collider = ScreenCollider(TestScreenCollider.rect_make_list[x]((50,50)),lambda _:[],lambda _:None)
            #Firstly, make sure that if we add a rectangle which partially fits inside the collider,
            #it will remain inside
            rect_collider.insert_rectangle((-10,-10,1,1,"key"))
            self.assertTrue(rect_collider.remove_rectangle((-10,-10,1,1,"key")))
            #Now check that a rectangle inserted outside the collider is ignored.
            rect_collider.insert_rectangle((50,50,51,51,"key"))
            self.assertFalse(rect_collider.remove_rectangle((50,50,51,51,"key")))
            #Pretend to swallow the screen...
            rect_collider.insert_rectangle((-5,-5,55,55,"key"))
            self.assertTrue(rect_collider.remove_rectangle((-5,-5,55,55,"key")))
            #Add a non-existent rectangle (expect this to be allowed, but ignored)
            rect_collider.insert_rectangle((10,10,10,15,"key"))
            self.assertFalse(rect_collider.remove_rectangle((-5,-5,55,55,"key")))
            #Done!
        
    def test_collision(self):
        '''
        Test the collision calculations by the rectangle collider. This is the really
        important stuff!
        '''
        size = (50,50)
        (width,height) = size
        for x in range(0,len(TestScreenCollider.rect_make_list)):
            rect_collider = ScreenCollider(TestScreenCollider.rect_make_list[x](size),lambda _:[],lambda _:None)
            #Add a lot of rectangles...
            rect_list = []
            for x in range(0,(width/2)-1):
                for y in range(0,(height/2)-1):
                    rect_list.append((x*2,y*2,(x+1)*2,(y+1)*2,None))
            #Add the rectangles
            for rect in rect_list:
                rect_collider.insert_rectangle(rect)
            #Now collide some rectangles!
            self.collision_check((5,2,30,30), size, rect_list, rect_collider, [], None)
            #Outside the rectangle
            self.collision_check((19,height,20,height+1), size, rect_list, rect_collider, [], None)
            #Arbitrary
            self.collision_check((18,5,30,45), size, rect_list, rect_collider, [], None)
            #Whole screen
            self.collision_check((0,0,width,height), size, rect_list, rect_collider, [], None)
            #Too thin
            self.collision_check((2,4,2,9), size, rect_list, rect_collider, [], None)
            #Good!
    
    def collision_check(self, rect, size, rect_list, rect_collider, inner_rectangles, inner_collider):
        '''
        Perform acollision check!
        @param rect: the colliding rectangle
        @param test_case: the test case running this method
        @param size: the size of the collider's screen
        @param rect_list: the list of rectangles in the collider
        @param rect_collider: the collider itself!
        @param inner_rectangles: the inner rectangles for the colliding rectangle
        @param inner_collider: the inner collider containing those inner rectangles
        '''
        res = rect_collider.collide_rectangle(rect, inner_rectangles, inner_collider)
        #Convert to set...
        res_set = set()
        for temp_rect in res:
            res_set.add(temp_rect)
        correct = self.collision_check_2(rect,size,rect_list)
        #Convert to set...
        correct_set = set()
        for temp_rect in correct:
            correct_set.add(temp_rect)
        self.assertTrue(res_set==correct_set)
        #Check boolean value
        res = rect_collider.is_colliding(rect)
        self.assertTrue(res==(self.collision_check_2(rect,size,rect_list)!=[]))
        #Done
    
    #This is bordering on too complex for a test, but I'm sure it is ok...
    def collision_check_2(self,rect,size,rect_list):
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
    
    @staticmethod
    def default_get_rect_list((a,b,c,d,(rect_list,e))):
        #Get the rectangle list from the keyed rectangle
        return rect_list
    
    @staticmethod
    def default_get_rect_collider((a,b,c,d,(e,rect_collider))):
        #Get the rectangle collider from the keyed rectangle
        return rect_collider

    def test_precise_collision(self):
        '''
        Test collisions using the inner rectangle colliders
        '''
        #This method checks a few cases where the initial collision does not
        #necessarily indicate a genuine collision when examined in detail.
        
        rect_collider = ScreenCollider(SimpleRectangleCollider((100,100))
                                       ,TestScreenCollider.default_get_rect_list,
                                       TestScreenCollider.default_get_rect_collider)
        #Now add some c shaped rectangles...
        inner_collider = SimpleRectangleCollider((30,30))
        '''
             ##########
             ##########
                  #####
                  #####
             ##########
             ##########
        '''
        inner_rectangle_list = [(10,0,30,10),
                                (20,10,30,20),
                                (10,20,30,30)]
        for (x_min,y_min,x_max,y_max) in inner_rectangle_list:
            inner_collider.insert_rectangle((x_min,y_min,x_max,y_max,None))
        #The outer rectangle entered (30*30)
        outer_rectangle = (50,50,80,80,(inner_rectangle_list,inner_collider))
        #Remember this
        original_outer_rectangle = outer_rectangle
        #Add the the rect collider...
        rect_collider.insert_rectangle(outer_rectangle)
        
        #Now construct a slot to "not fit"
        '''
        #####
        #####
        ###############
        ###############
        #####
        #####
        '''
        inner_collider = SimpleRectangleCollider((30,30))
        inner_rectangle_list = [(0,0,10,10),
                                (0,10,30,20),
                                (0,20,10,30)]
        for (x_min,y_min,x_max,y_max) in inner_rectangle_list:
            inner_collider.insert_rectangle((x_min,y_min,x_max,y_max,None))
        outer_rectangle = (40,50,70,80)
        #Now collide!
        self.assertFalse(rect_collider.is_colliding(outer_rectangle, inner_rectangle_list, inner_collider))
        self.assertTrue(rect_collider.collide_rectangle(outer_rectangle, inner_rectangle_list, inner_collider)==[])
        #Now move it slightly, and check the collision is made...
        outer_rectangle = (41,50,71,80)
        self.assertTrue(rect_collider.is_colliding(outer_rectangle, inner_rectangle_list, inner_collider))
        self.assertTrue(rect_collider.collide_rectangle(outer_rectangle, inner_rectangle_list, inner_collider)==[original_outer_rectangle])
        #And again...
        outer_rectangle = (40,51,70,81)
        self.assertTrue(rect_collider.is_colliding(outer_rectangle, inner_rectangle_list, inner_collider))
        self.assertTrue(rect_collider.collide_rectangle(outer_rectangle, inner_rectangle_list, inner_collider)==[original_outer_rectangle])
        #Good enough
        
    
def suite():
    '''
    Add all test methods in this module to the suite!
    '''
    test_suite = unittest.TestSuite(
        [#Add all classes here
         unittest.TestLoader().loadTestsFromTestCase(TestScreenCollider)
        ])
    return test_suite

def load_tests(loader, tests, pattern):
    return suite()