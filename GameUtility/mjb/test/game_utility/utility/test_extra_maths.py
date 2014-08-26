'''
Created on 26 Aug 2014

@author: michael
'''

import unittest
import mjb.dev.game_utility.utility.extra_maths as extra_maths
import math

class TestExtraMaths(unittest.TestCase):
    '''
    Test class for simple_rectangle_collider.py
    '''
    
    def test_rotation(self):
        point_error = 0.0000001
        #Check how it rotates points!
        my_point = (3,6)
        #Rotate!
        res = extra_maths.rotate_anti_clockwise_by_origin(my_point, math.radians(0))
        self.assertTrue(abs(res[0]-3)<=point_error and abs(res[1]-6)<=point_error)
        res = extra_maths.rotate_anti_clockwise_by_origin(my_point, math.radians(90))
        self.assertTrue(abs(res[0]-(-6))<=point_error and abs(res[1]-3)<=point_error)
        res = extra_maths.rotate_anti_clockwise_by_origin(my_point, math.radians(180))
        self.assertTrue(abs(res[0]-(-3))<=point_error and abs(res[1]-(-6))<=point_error)
        res = extra_maths.rotate_anti_clockwise_by_origin(my_point, math.radians(270))
        self.assertTrue(abs(res[0]-6)<=point_error and abs(res[1]-(-3))<=point_error)
        #Done
        
        #Now rotate around a different point...
        origin = (2,2)
        res = extra_maths.rotate_anti_clockwise(my_point, origin, math.radians(0))
        self.assertTrue(abs(-2+res[0]-1)<=point_error and abs(-2+res[1]-4)<=point_error)
        res = extra_maths.rotate_anti_clockwise(my_point, origin, math.radians(90))
        self.assertTrue(abs(-2+res[0]-(-4))<=point_error and abs(-2+res[1]-1)<=point_error)
        res = extra_maths.rotate_anti_clockwise(my_point, origin, math.radians(180))
        self.assertTrue(abs(-2+res[0]-(-1))<=point_error and abs(-2+res[1]-(-4))<=point_error)
        res = extra_maths.rotate_anti_clockwise(my_point, origin, math.radians(270))
        self.assertTrue(abs(-2+res[0]-4)<=point_error and abs(-2+res[1]-(-1))<=point_error)
        
        #Good enough
    def test_rectangle_collision(self):
        #Check the simple cases first...
        self.assertTrue(extra_maths.are_rotated_rectangles_colliding(
            ((3,3),(6,3),math.radians(0)),
            ((5,3),(2,2),math.radians(0)),
            False))
        self.assertTrue(extra_maths.are_rotated_rectangles_colliding(
            ((3,3),(6,3),math.radians(0)),
            ((5,3),(2,2),math.radians(0)),
            True))
        #Check for the simple case of the touching calculator...
        self.assertFalse(extra_maths.are_rotated_rectangles_colliding(
            ((3,4),(1,1),math.radians(0)),
            ((5,4),(1,1),math.radians(0)),
            False))
        self.assertTrue(extra_maths.are_rotated_rectangles_colliding(
            ((3,4),(1,1),math.radians(0)),
            ((5,4),(1,1),math.radians(0)),
            True))
        
        #Now for something more complex....
        self.assertTrue(extra_maths.are_rotated_rectangles_colliding(
            ((3,4),(1,1),math.radians(19)),
            ((5,4),(1,1),math.radians(-5)),
            False))
        self.assertTrue(extra_maths.are_rotated_rectangles_colliding(
            ((3,4),(1,1),math.radians(20)),
            ((5,4),(1,1),math.radians(-78)),
            True))
        self.assertFalse(extra_maths.are_rotated_rectangles_colliding(
            ((3,4),(1,1),math.radians(19)),
            ((8,4),(1,1),math.radians(-5)),
            False))
        self.assertFalse(extra_maths.are_rotated_rectangles_colliding(
            ((3,4),(1,1),math.radians(20)),
            ((8,4),(1,1),math.radians(-78)),
            True))
        
        #Now for the touching case
        self.assertFalse(extra_maths.are_rotated_rectangles_colliding(
            ((1,1),(6,math.sqrt(2)),math.radians(-45)),
            ((4,2),(math.sqrt(2),12),math.radians(45)),
            False))
        self.assertTrue(extra_maths.are_rotated_rectangles_colliding(
            ((1,1),(6,math.sqrt(2)),math.radians(-45)),
            ((4,2),(math.sqrt(2),12),math.radians(45)),
            True))
        
def suite():
    '''
    Add all test methods in this module to the suite!
    '''
    test_suite = unittest.TestSuite(
        [#Add all classes here
         unittest.TestLoader().loadTestsFromTestCase(TestExtraMaths)
        ])
    return test_suite

def load_tests(loader, tests, pattern):
    return suite()