'''
Created on 28 Jul 2014

@author: michael
'''
import unittest
import mjb.test.game_utility.collisions.test_simple_rectangle_collider as test_simple_rectangle_collider
import mjb.test.game_utility.collisions.test_small_rectangle_tree as test_small_rectangle_tree
import mjb.test.game_utility.collisions.test_large_rectangle_tree as test_large_rectangle_tree
import mjb.test.game_utility.collisions.test_screen_collider as test_screen_collider

def suite():
    '''
    Returns a test suite for all of the modules in this package
    '''
    test_suite = unittest.TestSuite(
        #Add all of the suites here:
        [test_simple_rectangle_collider.suite(),
         test_small_rectangle_tree.suite(),
         test_large_rectangle_tree.suite(),
         test_screen_collider.suite()
        ])
    return test_suite

def load_tests(loader, tests, pattern):
    return suite()
    