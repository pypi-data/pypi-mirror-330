"""
Tests for the Indian music functionality of SvaraScala.
"""

import unittest
from svarascala import IndianMusic


class TestIndianMusic(unittest.TestCase):
    """Test cases for the IndianMusic class."""

    def setUp(self):
        """Initialize an IndianMusic instance for testing."""
        self.im = IndianMusic(reference_sa=220.0)

    def test_get_shruti_frequency(self):
        """Test shruti frequency calculations."""
        # Test Sa (Shadja) - shruti 1
        self.assertAlmostEqual(self.im.get_shruti_frequency(1), 220.0)
        
        # Test Pa (Panchama) - shruti 14 (perfect fifth)
        self.assertAlmostEqual(self.im.get_shruti_frequency(14), 330.0)
        
        # Test Ma (Madhyama) - shruti 10 (perfect fourth)
        self.assertAlmostEqual(self.im.get_shruti_frequency(10), 293.33, places=2)
        
        # Test invalid shruti number
        with self.assertRaises(ValueError):
            self.im.get_shruti_frequency(23)
            
    def test_get_swara_frequency(self):
        """Test swara frequency calculations."""
        # Test Sa
        self.assertAlmostEqual(self.im.get_swara_frequency('Sa'), 220.0)
        
        # Test Pa
        self.assertAlmostEqual(self.im.get_swara_frequency('Pa'), 330.0)
        
        # Test komal Re
        self.assertAlmostEqual(self.im.get_swara_frequency('Re', 'komal'), 234.67, places=2)
        
        # Test shuddha Ga
        self.assertAlmostEqual(self.im.get_swara_frequency('Ga', 'shuddha'), 275.0)
        
        # Test tivra Ma
        self.assertAlmostEqual(self.im.get_swara_frequency('Ma', 'tivra'), 313.24, places=2)
        
        # Test invalid swara variant
        with self.assertRaises(ValueError):
            self.im.get_swara_frequency('Re', 'invalid_variant')

    def test_get_raga(self):
        """Test raga structure retrieval."""
        # Test Yaman raga
        yaman = self.im.get_raga('Yaman')
        
        # Check raga length
        self.assertEqual(len(yaman), 7)
        
        # Check first and last notes
        self.assertEqual(yaman[0], ('Sa', 'shuddha'))
        self.assertEqual(yaman[-1], ('Ni', 'shuddha'))
        
        # Check specific swara variants
        self.assertIn(('Ma', 'tivra'), yaman)
        
        # Test invalid raga name
        with self.assertRaises(ValueError):
            self.im.get_raga('NonExistentRaga')

    def test_calculate_raga_frequencies(self):
        """Test raga frequency calculations."""
        # Test Bhairav raga frequencies
        bhairav_freqs = self.im.calculate_raga_frequencies('Bhairav')
        
        # Check dictionary length
        self.assertEqual(len(bhairav_freqs), 7)
        
        # Check specific frequencies
        self.assertAlmostEqual(bhairav_freqs['Sa shuddha'], 220.0)
        self.assertAlmostEqual(bhairav_freqs['Re komal'], 234.67, places=2)
        self.assertAlmostEqual(bhairav_freqs['Pa shuddha'], 330.0)
        
        # Test invalid raga name
        with self.assertRaises(ValueError):
            self.im.calculate_raga_frequencies('InvalidRaga')

    def test_get_all_shrutis(self):
        """Test retrieving all 22 shrutis."""
        shrutis = self.im.get_all_shrutis()
        
        # Check dictionary length
        self.assertEqual(len(shrutis), 22)
        
        # Check first shruti frequency (Sa)
        self.assertAlmostEqual(shrutis['Shruti 1'], 220.0)
        
        # Check last shruti frequency (Tivra Ni)
        # Use 0 decimal places since the actual value may vary slightly
        # based on the just intonation implementation
        self.assertAlmostEqual(shrutis['Shruti 22'] / 220.0, 243.0/128.0, places=4)


if __name__ == '__main__':
    unittest.main()