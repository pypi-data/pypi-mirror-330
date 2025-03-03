"""
Tests for the Western modes functionality of SvaraScala.
"""

import unittest
from svarascala import WesternModes, WesternMusic, NavarasaMap


class TestWesternModes(unittest.TestCase):
    """Test cases for the WesternModes class."""

    def setUp(self):
        """Initialize WesternModes instances for testing."""
        # Standard A440 tuning
        self.wm = WesternModes(reference_a4=440.0)
        
        # Create WesternMusic and NavarasaMap instances for cross-functionality testing
        self.western = WesternMusic(reference_a4=440.0)
        self.navarasa = NavarasaMap(reference_sa=220.0)

    def test_get_mode_intervals(self):
        """Test retrieving mode intervals."""
        # Test Ionian (major scale)
        ionian = self.wm.get_mode_intervals("Ionian")
        self.assertEqual(ionian, [0, 2, 4, 5, 7, 9, 11])
        
        # Test Dorian
        dorian = self.wm.get_mode_intervals("Dorian")
        self.assertEqual(dorian, [0, 2, 3, 5, 7, 9, 10])
        
        # Test invalid mode
        with self.assertRaises(ValueError):
            self.wm.get_mode_intervals("InvalidMode")

    def test_get_mode_info(self):
        """Test retrieving mode information."""
        # Test Lydian
        lydian_info = self.wm.get_mode_info("Lydian")
        self.assertEqual(lydian_info["primary"], "Wonder")
        self.assertEqual(lydian_info["energy_level"], 7)
        
        # Test Aeolian
        aeolian_info = self.wm.get_mode_info("Aeolian")
        self.assertEqual(aeolian_info["primary"], "Sadness")
        self.assertEqual(aeolian_info["energy_level"], 4)
        
        # Test invalid mode
        with self.assertRaises(ValueError):
            self.wm.get_mode_info("InvalidMode")

    def test_get_mode_frequencies(self):
        """Test calculating frequencies for modes."""
        # Test C Ionian
        c_ionian = self.wm.get_mode_frequencies("Ionian", "C", 4)
        self.assertIn("C4", c_ionian)
        self.assertIn("G4", c_ionian)
        self.assertIn("B4", c_ionian)
        
        # Test D Dorian
        d_dorian = self.wm.get_mode_frequencies("Dorian", "D", 4)
        self.assertIn("D4", d_dorian)
        self.assertIn("B4", d_dorian)
        
        # Check specific frequencies
        self.assertAlmostEqual(c_ionian["C4"], 261.63, places=2)
        self.assertAlmostEqual(d_dorian["D4"], 293.66, places=2)
        
        # Test mode that crosses octave boundary
        b_phrygian = self.wm.get_mode_frequencies("Phrygian", "B", 3)
        self.assertIn("B3", b_phrygian)
        self.assertIn("C4", b_phrygian)
        self.assertGreater(b_phrygian["C4"], b_phrygian["B3"])

    def test_get_compatible_modes(self):
        """Test finding compatible modal transitions."""
        # Test Ionian transitions
        ionian_transitions = self.wm.get_compatible_modes("Ionian")
        self.assertIn("Mixolydian", ionian_transitions)
        self.assertIn("Lydian", ionian_transitions)
        
        # Check transition details
        for mode, details in ionian_transitions.items():
            self.assertIn("primary_emotion", details)
            self.assertIn("energy_transition", details)
            self.assertIn("energy_difference", details)
            self.assertIn("recommended_instruments", details)
        
        # Test invalid mode
        with self.assertRaises(ValueError):
            self.wm.get_compatible_modes("InvalidMode")

    def test_suggest_transition_path(self):
        """Test suggesting transition paths between modes."""
        # Test direct transition
        direct_path = self.wm.suggest_transition_path("Ionian", "Mixolydian")
        self.assertEqual(direct_path, ["Ionian", "Mixolydian"])
        
        # Test same mode
        same_path = self.wm.suggest_transition_path("Dorian", "Dorian")
        self.assertEqual(same_path, ["Dorian"])
        
        # Test path with intermediate steps
        multi_step_path = self.wm.suggest_transition_path("Lydian", "Aeolian")
        self.assertIsNotNone(multi_step_path)
        self.assertGreater(len(multi_step_path), 1)
        self.assertEqual(multi_step_path[0], "Lydian")
        self.assertEqual(multi_step_path[-1], "Aeolian")
        
        # Test path exceeding max steps
        no_path = self.wm.suggest_transition_path("Lydian", "Locrian", max_steps=1)
        self.assertIsNone(no_path)
        
        # Test invalid mode
        with self.assertRaises(ValueError):
            self.wm.suggest_transition_path("InvalidMode", "Ionian")

    def test_get_corresponding_rasa(self):
        """Test retrieving corresponding Indian rasas."""
        # Test Ionian-Rasa mapping
        ionian_rasas = self.wm.get_corresponding_rasa("Ionian")
        self.assertIn("Sringara", ionian_rasas)
        self.assertIn("Haasya", ionian_rasas)
        
        # Test Aeolian-Rasa mapping
        aeolian_rasas = self.wm.get_corresponding_rasa("Aeolian")
        self.assertIn("Karuna", aeolian_rasas)
        
        # Test invalid mode
        with self.assertRaises(ValueError):
            self.wm.get_corresponding_rasa("InvalidMode")

    def test_get_historical_usage(self):
        """Test retrieving historical usage information."""
        # Test Dorian historical info
        dorian_history = self.wm.get_historical_usage("Dorian")
        self.assertIn("eras", dorian_history)
        self.assertIn("prominence", dorian_history)
        self.assertIn("contexts", dorian_history)
        
        # Check specific historical features
        self.assertIn("Medieval", dorian_history["eras"])
        self.assertIn("Folk songs", dorian_history["contexts"])
        
        # Test invalid mode
        with self.assertRaises(ValueError):
            self.wm.get_historical_usage("InvalidMode")

    def test_compare_mode_to_raga(self):
        """Test comparing Western modes to Indian ragas."""
        # Test comparison without NavarasaMap
        basic_comparison = self.wm.compare_mode_to_raga("Dorian", "D", 4)
        self.assertIn("mode", basic_comparison)
        self.assertIn("corresponding_rasas", basic_comparison)
        self.assertIn("emotional_character", basic_comparison)
        
        # Test with NavarasaMap
        full_comparison = self.wm.compare_mode_to_raga("Dorian", "D", 4, self.navarasa)
        self.assertIn("related_ragas", full_comparison)
        self.assertGreater(len(full_comparison["related_ragas"]), 0)
        
        # Check emotional correlations
        self.assertIn("Saantha", full_comparison["corresponding_rasas"])
        
        # Test invalid mode
        with self.assertRaises(ValueError):
            self.wm.compare_mode_to_raga("InvalidMode", "C", 4)

    def test_get_common_chord_progressions(self):
        """Test retrieving common chord progressions for modes."""
        # Test Ionian progressions
        ionian_progressions = self.wm.get_common_chord_progressions("Ionian")
        self.assertIsInstance(ionian_progressions, list)
        self.assertGreater(len(ionian_progressions), 0)
        self.assertIn("I - IV - V - I", ionian_progressions)
        
        # Test Dorian progressions
        dorian_progressions = self.wm.get_common_chord_progressions("Dorian")
        self.assertIn("i - IV - i", dorian_progressions)
        
        # Test invalid mode
        with self.assertRaises(ValueError):
            self.wm.get_common_chord_progressions("InvalidMode")

    def test_different_reference_tunings(self):
        """Test the effect of different reference tunings."""
        # Create instances with different reference tunings
        wm_432 = WesternModes(reference_a4=432.0)
        wm_415 = WesternModes(reference_a4=415.0)
        
        # Calculate C Dorian frequencies with different tunings
        c_dorian_440 = self.wm.get_mode_frequencies("Dorian", "C", 4)
        c_dorian_432 = wm_432.get_mode_frequencies("Dorian", "C", 4)
        c_dorian_415 = wm_415.get_mode_frequencies("Dorian", "C", 4)
        
        # Frequencies should be different with different tunings
        self.assertNotEqual(c_dorian_440["C4"], c_dorian_432["C4"])
        self.assertNotEqual(c_dorian_440["C4"], c_dorian_415["C4"])
        
        # But the frequency ratios within each mode should be preserved
        ratio_440 = c_dorian_440["G4"] / c_dorian_440["C4"]
        ratio_432 = c_dorian_432["G4"] / c_dorian_432["C4"]
        self.assertAlmostEqual(ratio_440, ratio_432, places=3)


if __name__ == '__main__':
    unittest.main()