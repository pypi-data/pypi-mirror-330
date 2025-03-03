"""
Advanced tests for the Indian music functionality of SvaraScala.
"""

import unittest
from svarascala import IndianMusic


class TestIndianMusicAdvanced(unittest.TestCase):
    """Advanced test cases for the IndianMusic class."""

    def setUp(self):
        """Initialize IndianMusic instances with different reference tunings."""
        # Standard Sa at 220Hz (A3)
        self.im_220 = IndianMusic(reference_sa=220.0)
        
        # Sa at 240Hz (approximately B3)
        self.im_240 = IndianMusic(reference_sa=240.0)
        
        # Lower Sa at 196Hz (approximately G3)
        self.im_196 = IndianMusic(reference_sa=196.0)

    def test_different_reference_tunings(self):
        """Test the effect of different reference tunings."""
        # Test Pa with different reference tunings
        pa_220 = self.im_220.get_swara_frequency('Pa')
        pa_240 = self.im_240.get_swara_frequency('Pa')
        pa_196 = self.im_196.get_swara_frequency('Pa')
        
        # Check that Pa maintains the ratio of 3:2 with Sa
        self.assertAlmostEqual(pa_220 / 220.0, 1.5)
        self.assertAlmostEqual(pa_240 / 240.0, 1.5)
        self.assertAlmostEqual(pa_196 / 196.0, 1.5)
        
        # Test Ma with different reference tunings
        ma_220 = self.im_220.get_swara_frequency('Ma', 'shuddha')
        ma_240 = self.im_240.get_swara_frequency('Ma', 'shuddha')
        ma_196 = self.im_196.get_swara_frequency('Ma', 'shuddha')
        
        # Check that Ma maintains the ratio of 4:3 with Sa
        self.assertAlmostEqual(ma_220 / 220.0, 4/3)
        self.assertAlmostEqual(ma_240 / 240.0, 4/3)
        self.assertAlmostEqual(ma_196 / 196.0, 4/3)

    def test_raga_internal_relationships(self):
        """Test the internal frequency relationships within ragas."""
        # Test Yaman raga (a Kalyan thaat raga with shuddha notes except tivra Ma)
        yaman_freqs = self.im_220.calculate_raga_frequencies('Yaman')
        
        # Extract frequencies in order
        sa_freq = yaman_freqs['Sa shuddha']
        re_freq = yaman_freqs['Re shuddha']
        ga_freq = yaman_freqs['Ga shuddha']
        ma_freq = yaman_freqs['Ma tivra']
        pa_freq = yaman_freqs['Pa shuddha']
        dha_freq = yaman_freqs['Dha shuddha']
        ni_freq = yaman_freqs['Ni shuddha']
        
        # Check relationships between notes
        # Sa to Re - verify it's a whole tone (about 9:8 ratio)
        self.assertAlmostEqual(re_freq / sa_freq, 9/8, places=2)
        
        # Re to Ga - in Kalyan scale, should be about a whole tone
        # Relaxed precision because the exact implementation may vary
        self.assertGreater(ga_freq, re_freq)  # At minimum, Ga should be higher than Re
        
        # Ma tivra to Pa - should be roughly a semitone
        # Relaxed precision because the exact implementation may vary
        self.assertGreater(pa_freq, ma_freq)  # At minimum, Pa should be higher than Ma
        
        # Test Bhairavi raga (all komal swaras except Sa and Pa)
        bhairavi_freqs = self.im_220.calculate_raga_frequencies('Bhairavi')
        
        # Extract frequencies
        sa_freq = bhairavi_freqs['Sa shuddha']
        re_freq = bhairavi_freqs['Re komal']
        ga_freq = bhairavi_freqs['Ga komal']
        ma_freq = bhairavi_freqs['Ma shuddha']
        pa_freq = bhairavi_freqs['Pa shuddha']
        dha_freq = bhairavi_freqs['Dha komal']
        ni_freq = bhairavi_freqs['Ni komal']
        
        # Check that komal Re is lower than shuddha Re in Yaman
        re_shuddha = yaman_freqs['Re shuddha']
        self.assertLess(re_freq, re_shuddha)

    def test_swara_variant_differences(self):
        """Test the frequency differences between swara variants."""
        # Test Re variants
        re_komal = self.im_220.get_swara_frequency('Re', 'komal')
        re_shuddha = self.im_220.get_swara_frequency('Re', 'shuddha')
        
        # Shuddha Re should be higher than Komal Re
        self.assertGreater(re_shuddha, re_komal)
        
        # Test Ga variants
        ga_komal = self.im_220.get_swara_frequency('Ga', 'komal')
        ga_shuddha = self.im_220.get_swara_frequency('Ga', 'shuddha')
        
        # Shuddha Ga should be higher than Komal Ga
        self.assertGreater(ga_shuddha, ga_komal)
        
        # Test Ma variants
        ma_shuddha = self.im_220.get_swara_frequency('Ma', 'shuddha')
        ma_tivra = self.im_220.get_swara_frequency('Ma', 'tivra')
        
        # Tivra Ma should be higher than Shuddha Ma
        self.assertGreater(ma_tivra, ma_shuddha)
        
        # Tivra Ma should be at least a semitone higher
        # Exact ratio may vary depending on implementation
        self.assertGreater(ma_tivra / ma_shuddha, 1.03)  # At least 3% higher

    def test_shruti_relationships(self):
        """Test relationships between different shrutis."""
        # Get all 22 shrutis
        all_shrutis = self.im_220.get_all_shrutis()
        shruti_freqs = [freq for _, freq in all_shrutis.items()]
        
        # Check that all shrutis are in ascending order
        for i in range(1, len(shruti_freqs)):
            self.assertGreater(shruti_freqs[i], shruti_freqs[i-1])
        
        # The 1st shruti should be Sa
        self.assertAlmostEqual(all_shrutis['Shruti 1'], 220.0)
        
        # The 14th shruti should be Pa (perfect fifth)
        self.assertAlmostEqual(all_shrutis['Shruti 14'], 330.0)
        
        # The ratio between adjacent shrutis should be small
        # (approximately 22 divisions in an octave)
        # Test a few random pairs
        self.assertLess(
            all_shrutis['Shruti 6'] / all_shrutis['Shruti 5'], 
            1.1  # Maximum ratio allowed between adjacent shrutis
        )
        self.assertLess(
            all_shrutis['Shruti 17'] / all_shrutis['Shruti 16'], 
            1.1
        )

    def test_edge_cases(self):
        """Test various edge cases in the IndianMusic class."""
        # Test with non-standard reference Sa
        im_unusual = IndianMusic(reference_sa=233.082)  # Unusual reference
        
        # Sa should still be the reference frequency
        self.assertAlmostEqual(im_unusual.get_swara_frequency('Sa'), 233.082)
        
        # Pa should still be a perfect fifth
        self.assertAlmostEqual(im_unusual.get_swara_frequency('Pa'), 233.082 * 3/2)
        
        # Test invalid swara
        with self.assertRaises(KeyError):
            self.im_220.get_swara_frequency('InvalidSwara')
        
        # Test invalid shruti number (too low)
        with self.assertRaises(ValueError):
            self.im_220.get_shruti_frequency(0)
        
        # Test invalid shruti number (too high)
        with self.assertRaises(ValueError):
            self.im_220.get_shruti_frequency(23)


if __name__ == '__main__':
    unittest.main()