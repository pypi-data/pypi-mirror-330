"""
Test suite runner for SvaraScala.

Run this file to execute all tests for the SvaraScala library.
"""

import unittest
import sys
import os

# Add the parent directory to the path so we can import the tests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import all the test modules
from tests.test_init import TestInit
from tests.test_western import TestWesternMusic
from tests.test_indian import TestIndianMusic
from tests.test_main import TestMainCLI
from tests.test_western_advanced import TestWesternMusicAdvanced
from tests.test_indian_advanced import TestIndianMusicAdvanced
from tests.test_main_advanced import TestMainCLIAdvanced

def create_test_suite():
    """Create a test suite containing all SvaraScala tests."""
    test_suite = unittest.TestSuite()
    test_loader = unittest.TestLoader()
    
    # Add test cases for each module
    test_suite.addTest(test_loader.loadTestsFromTestCase(TestInit))
    test_suite.addTest(test_loader.loadTestsFromTestCase(TestWesternMusic))
    test_suite.addTest(test_loader.loadTestsFromTestCase(TestIndianMusic))
    test_suite.addTest(test_loader.loadTestsFromTestCase(TestMainCLI))
    test_suite.addTest(test_loader.loadTestsFromTestCase(TestWesternMusicAdvanced))
    test_suite.addTest(test_loader.loadTestsFromTestCase(TestIndianMusicAdvanced))
    test_suite.addTest(test_loader.loadTestsFromTestCase(TestMainCLIAdvanced))
    
    return test_suite

if __name__ == '__main__':
    # Create a test runner
    runner = unittest.TextTestRunner(verbosity=2)
    
    # Create and run the test suite
    test_suite = create_test_suite()
    runner.run(test_suite)