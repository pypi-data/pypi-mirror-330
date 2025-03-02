"""
Tests for the SvaraScala package initialization.
"""

import unittest
import importlib
import sys
import os

# Add the parent directory to the path so we can import svarascala
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestInit(unittest.TestCase):
    """Test cases for the package initialization."""
    
    def test_version(self):
        """Test that version is defined and in the correct format."""
        import svarascala
        
        # Check version exists
        self.assertTrue(hasattr(svarascala, '__version__'))
        
        # Check version format (should be 'x.y.z')
        version = svarascala.__version__
        self.assertRegex(version, r'^\d+\.\d+\.\d+$')
    
    def test_imports(self):
        """Test that main classes are properly imported."""
        import svarascala
        
        # Check WesternMusic is imported
        self.assertTrue(hasattr(svarascala, 'WesternMusic'))
        
        # Check IndianMusic is imported
        self.assertTrue(hasattr(svarascala, 'IndianMusic'))
        
        # Test creating instances
        western = svarascala.WesternMusic()
        self.assertIsInstance(western, svarascala.WesternMusic)
        
        indian = svarascala.IndianMusic()
        self.assertIsInstance(indian, svarascala.IndianMusic)
    
    def test_reload(self):
        """Test that the module can be reloaded."""
        import svarascala
        importlib.reload(svarascala)
        
        # Check main classes after reload
        self.assertTrue(hasattr(svarascala, 'WesternMusic'))
        self.assertTrue(hasattr(svarascala, 'IndianMusic'))


if __name__ == '__main__':
    unittest.main()