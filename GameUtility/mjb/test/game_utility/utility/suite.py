'''
Created on 28 Jul 2014

@author: michael
'''
import unittest
import mjb.test.game_utility.utility.test_extra_maths as test_extra_maths

def suite():
    '''
    Returns a test suite for all of the modules in this package
    '''
    test_suite = unittest.TestSuite(
        #Add all of the suites here:
        [test_extra_maths.suite()
        ])
    return test_suite

def load_tests(loader, tests, pattern):
    return suite()