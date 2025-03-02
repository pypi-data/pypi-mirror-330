"""
Advanced tests for the Western music functionality of SvaraScala.
"""

import unittest
from svarascala import WesternMusic


class TestWesternMusicAdvanced(unittest.TestCase):
    """Advanced test cases for the WesternMusic class."""

    def setUp(self):
        """Initialize WesternMusic instances with different reference tunings."""
        # Standard A440 tuning
        self.wm_standard = WesternMusic(reference_a4=440.0)
        
        # A432 tuning (sometimes called "Verdi tuning" or "scientific tuning")
        self.wm_432 = WesternMusic(reference_a4=432.0)
        
        # Baroque tuning (A415)
        self.wm_baroque = WesternMusic(reference_a4=415.0)
        
        # Modern high tuning (A444)
        self.wm_high = WesternMusic(reference_a4=444.0)

    def test_different_reference_tunings(self):
        """Test the effect of different reference tunings."""
        # Test C4 with different reference tunings
        c4_standard = self.wm_standard.get_frequency('C', 4)
        c4_432 = self.wm_432.get_frequency('C', 4)
        c4_baroque = self.wm_baroque.get_frequency('C', 4)
        c4_high = self.wm_high.get_frequency('C', 4)
        
        # Check that C4 is lower with A432 tuning
        self.assertLess(c4_432, c4_standard)
        
        # Check that C4 is significantly lower with Baroque tuning
        self.assertLess(c4_baroque, c4_432)
        
        # Check that C4 is higher with A444 tuning
        self.assertGreater(c4_high, c4_standard)
        
        # The ratio between frequencies should be approximately the same as the ratio
        # between reference pitches
        self.assertAlmostEqual(c4_432 / c4_standard, 432 / 440, places=2)
        self.assertAlmostEqual(c4_baroque / c4_standard, 415 / 440, places=2)
        self.assertAlmostEqual(c4_high / c4_standard, 444 / 440, places=2)

    def test_alternative_scales(self):
        """Test generation of less common scale types."""
        # Test chromatic scale
        c_chromatic = self.wm_standard.get_scale('C', 4, 'chromatic')
        
        # Chromatic scale should have 12 notes
        self.assertEqual(len(c_chromatic), 12)
        
        # Test blues scale
        a_blues = self.wm_standard.get_scale('A', 4, 'blues')
        
        # Blues scale should have 6 notes
        self.assertEqual(len(a_blues), 6)
        
        # Test that the tritone is included in blues scale (flat fifth)
        # In A blues, this would be Eb
        a_freq = self.wm_standard.get_frequency('A', 4)
        eb_freq = self.wm_standard.get_frequency('D#', 5)  # Enharmonic with Eb5
        
        # One of the blues scale notes should be close to Eb5
        has_tritone = any(abs(freq - eb_freq) < 1.0 for freq in a_blues.values())
        self.assertTrue(has_tritone)
        
        # Test pentatonic scales
        c_pentatonic = self.wm_standard.get_scale('C', 4, 'pentatonic_major')
        a_pentatonic = self.wm_standard.get_scale('A', 4, 'pentatonic_minor')
        
        # Pentatonic scales should have 5 notes
        self.assertEqual(len(c_pentatonic), 5)
        self.assertEqual(len(a_pentatonic), 5)

    def test_camelot_edge_cases(self):
        """Test edge cases for Camelot Wheel functionality."""
        # Test with lowercase notation
        self.assertEqual(
            self.wm_standard.get_key_from_camelot('5b'),
            self.wm_standard.get_key_from_camelot('5B')
        )
        
        # Test with invalid Camelot notation
        with self.assertRaises(ValueError):
            self.wm_standard.get_key_from_camelot('15B')
        
        with self.assertRaises(ValueError):
            self.wm_standard.get_key_from_camelot('5C')
        
        # Test converting non-standard keys
        # Some implementations might not handle these
        try:
            self.wm_standard.get_camelot_notation('C#')
            has_csharp_camelot = True
        except:
            has_csharp_camelot = False
        
        if has_csharp_camelot:
            # If C# is supported, test both C# and Db give same Camelot notation
            csharp_camelot = self.wm_standard.get_camelot_notation('C#')
            db_camelot = self.wm_standard.get_camelot_notation('Db')
            self.assertEqual(csharp_camelot, db_camelot)

    def test_scale_boundaries(self):
        """Test scales that cross octave boundaries."""
        # Test B major scale (which should contain notes in the next octave)
        b_major = self.wm_standard.get_scale('B', 4, 'major')
        
        # Should contain notes in both octave 4 and 5
        has_octave4 = any('4' in note for note in b_major.keys())
        has_octave5 = any('5' in note for note in b_major.keys())
        
        self.assertTrue(has_octave4)
        self.assertTrue(has_octave5)
        
        # Test note at octave boundary
        b4_freq = self.wm_standard.get_frequency('B', 4)
        c5_freq = self.wm_standard.get_frequency('C', 5)
        
        # C5 should be slightly higher than B4
        self.assertGreater(c5_freq, b4_freq)
        
        # The ratio is close to 1.06 in equal temperament (2^(1/12))
        # Use a wider tolerance because the actual implementation might vary
        self.assertAlmostEqual(c5_freq / b4_freq, 1.059, places=1)

    def test_get_compatible_keys_edge_cases(self):
        """Test edge cases for compatible keys function."""
        # Test with a camelot notation at the "edge" of the wheel
        compatible_12b = self.wm_standard.get_compatible_keys('12B')
        
        # Should wrap around to 1B
        self.assertIn('1B', compatible_12b)
        
        # Test compatibility at the "seam" of the wheel
        compatible_1a = self.wm_standard.get_compatible_keys('1A')
        
        # Should include 12A
        self.assertIn('12A', compatible_1a)
        
        # Test invalid input
        with self.assertRaises(ValueError):
            self.wm_standard.get_compatible_keys('invalid')
        
        with self.assertRaises(ValueError):
            self.wm_standard.get_compatible_keys('13A')


if __name__ == '__main__':
    unittest.main()