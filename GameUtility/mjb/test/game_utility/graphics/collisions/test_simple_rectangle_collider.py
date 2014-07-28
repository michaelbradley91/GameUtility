'''
Created on 28 Jul 2014

@author: michael
'''
import unittest

class TestSimpleRectangleTree(unittest.TestCase):
    '''
    Test class for simple_rectangle_collider.py
    '''

    def test_dummy(self):
        self.assertEqual(5, 4, "5 and 4 are not equal")

def suite():
    '''
    Add all test methods in this module to the suite!
    '''
    test_suite = unittest.TestSuite(
        [#Add all classes here
         unittest.TestLoader().loadTestsFromTestCase(TestSimpleRectangleTree)
        ])
    return test_suite

def load_tests(loader, tests, pattern):
    return suite()