'''
Created on 28 Jul 2014

@author: michael
'''
import unittest
import mjb.test.game_utility.graphics.drawers.suite as drawers_suite

def suite():
    '''
    Returns a test suite for all of the modules in this package
    '''
    test_suite = unittest.TestSuite(
        #Add all of the suites here:
        [drawers_suite.suite(),
        ])
    return test_suite

def load_tests(loader, tests, pattern):
    return suite()