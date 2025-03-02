"""
Tests for the Western music functionality of SvaraScala.
"""

import unittest
from svarascala import WesternMusic


class TestWesternMusic(unittest.TestCase):
    """Test cases for the WesternMusic class."""

    def setUp(self):
        """Initialize a WesternMusic instance for testing."""
        self.wm = WesternMusic(reference_a4=440.0)

    def test_get_frequency(self):
        """Test frequency calculation for various notes."""
        # Test A4 (reference note)
        self.assertAlmostEqual(self.wm.get_frequency('A', 4), 440.0)
        
        # Test C4 (middle C)
        self.assertAlmostEqual(self.wm.get_frequency('C', 4), 261.63, places=2)
        
        # Test F#4
        self.assertAlmostEqual(self.wm.get_frequency('F#', 4), 369.99, places=2)
        
        # Test Bb4 (enharmonic notation)
        self.assertAlmostEqual(self.wm.get_frequency('Bb', 4), 466.16, places=2)

    def test_enharmonic_equivalence(self):
        """Test that enharmonic equivalents produce the same frequency."""
        self.assertAlmostEqual(
            self.wm.get_frequency('C#', 4),
            self.wm.get_frequency('Db', 4)
        )
        
        self.assertAlmostEqual(
            self.wm.get_frequency('F#', 4),
            self.wm.get_frequency('Gb', 4)
        )

    def test_get_scale(self):
        """Test scale generation."""
        # Test C major scale
        c_major = self.wm.get_scale('C', 4, 'major')
        
        # Check scale length
        self.assertEqual(len(c_major), 7)
        
        # Check specific notes are present
        self.assertIn('C4', c_major)
        self.assertIn('G4', c_major)
        
        # Check specific frequencies
        self.assertAlmostEqual(c_major['C4'], 261.63, places=2)
        self.assertAlmostEqual(c_major['G4'], 392.00, places=2)

    def test_harmonic_relationship(self):
        """Test harmonic relationship detection."""
        # Test perfect fifth (C4 to G4)
        is_harmonic, relation = self.wm.are_harmonic('C', 4, 'G', 4)
        self.assertTrue(is_harmonic)
        self.assertIn("3:2", relation)
        
        # Test octave (C4 to C5)
        is_harmonic, relation = self.wm.are_harmonic('C', 4, 'C', 5)
        self.assertTrue(is_harmonic)
        self.assertIn("2:1", relation)
        
        # Test non-harmonic relationship (C4 to F#4)
        is_harmonic, relation = self.wm.are_harmonic('C', 4, 'F#', 4)
        self.assertFalse(is_harmonic)

    def test_solfege_frequency(self):
        """Test solfege name to frequency conversion."""
        # Test Do in C
        do_freq = self.wm.get_solfege_frequency('Do', 4, 'C')
        self.assertAlmostEqual(do_freq, 261.63, places=2)
        
        # Test Sol in C
        sol_freq = self.wm.get_solfege_frequency('Sol', 4, 'C')
        self.assertAlmostEqual(sol_freq, 392.00, places=2)
        
        # Test Do in G (should be G frequency)
        do_in_g = self.wm.get_solfege_frequency('Do', 4, 'G')
        self.assertAlmostEqual(do_in_g, 392.00, places=2)

    def test_camelot_notation(self):
        """Test Camelot wheel notation conversions."""
        # Test C major
        self.assertEqual(self.wm.get_camelot_notation('C', 'major'), '5B')
        
        # Test A minor
        self.assertEqual(self.wm.get_camelot_notation('A', 'minor'), '5A')
        self.assertEqual(self.wm.get_camelot_notation('Am'), '5A')
        
        # Test conversion from Camelot back to key
        key, scale = self.wm.get_key_from_camelot('5B')
        self.assertEqual(key, 'C')
        self.assertEqual(scale, 'major')

    def test_compatible_keys(self):
        """Test finding compatible keys for harmonic mixing."""
        # Test compatible keys for C major (5B)
        compatible = self.wm.get_compatible_keys('5B')
        
        # Should include relative minor (5A - Am)
        self.assertIn('5A', compatible)
        self.assertEqual(compatible['5A'], 'Am')
        
        # Should include perfect fifth up (6B - G)
        self.assertIn('6B', compatible)
        self.assertEqual(compatible['6B'], 'G')


if __name__ == '__main__':
    unittest.main()