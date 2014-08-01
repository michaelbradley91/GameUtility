'''
Created on 28 Jul 2014

@author: michael
'''
import unittest
import mjb.test.game_utility.collisions.test_rectangle_collider as test_rectangle_collider
from mjb.dev.game_utility.collisions.large_rectangle_tree import LargeRectangleTree 

class TestLargeRectangleTree(unittest.TestCase):
    '''
    Test class for simple_rectangle_collider.py
    '''

    def test_add_remove(self):
        test_rectangle_collider.test_add_remove(self, lambda size: LargeRectangleTree(size))
    
    def test_clear(self):
        test_rectangle_collider.test_clear(self, lambda size: LargeRectangleTree(size))
        
    def test_clipping(self):
        test_rectangle_collider.test_clipping(self, lambda size: LargeRectangleTree(size))
    
    def test_collision(self):
        test_rectangle_collider.test_collision(self, lambda size: LargeRectangleTree(size))
    
    
def suite():
    '''
    Add all test methods in this module to the suite!
    '''
    test_suite = unittest.TestSuite(
        [#Add all classes here
         unittest.TestLoader().loadTestsFromTestCase(TestLargeRectangleTree)
        ])
    return test_suite

def load_tests(loader, tests, pattern):
    return suite()