"""
Tests for the Navarasa wheel functionality of SvaraScala.
"""

import unittest
from svarascala import NavarasaMap


class TestNavarasaMap(unittest.TestCase):
    """Test cases for the NavarasaMap class."""

    def setUp(self):
        """Initialize a NavarasaMap instance for testing."""
        self.nw = NavarasaMap(reference_sa=220.0)

    def test_get_rasa_info(self):
        """Test retrieving information about a specific rasa."""
        # Test a valid rasa
        info = self.nw.get_rasa_info("Sringara")
        self.assertEqual(info["english"], "Love/Erotic")
        self.assertEqual(info["mood"], "Love")
        
        # Test an invalid rasa
        with self.assertRaises(ValueError):
            self.nw.get_rasa_info("InvalidRasa")

    def test_get_raga_by_rasa(self):
        """Test retrieving ragas associated with a rasa."""
        # Test a valid rasa
        ragas = self.nw.get_raga_by_rasa("Sringara")
        self.assertIsInstance(ragas, list)
        self.assertIn("Yaman", ragas)
        
        # Test an invalid rasa
        with self.assertRaises(ValueError):
            self.nw.get_raga_by_rasa("InvalidRasa")

    def test_get_rasa_from_raga(self):
        """Test finding rasas associated with a raga."""
        # Test a valid raga
        rasas = self.nw.get_rasa_from_raga("Bhairav")
        self.assertIsInstance(rasas, list)
        self.assertIn("Raudra", rasas)
        
        # Test a raga not in the classification
        rasas = self.nw.get_rasa_from_raga("NonExistentRaga")
        self.assertEqual(rasas, [])

    def test_get_raga_frequencies(self):
        """Test retrieving frequencies for a raga."""
        # Test a valid raga
        freqs = self.nw.get_raga_frequencies("Yaman")
        self.assertIsInstance(freqs, dict)
        self.assertTrue(len(freqs) > 0)
        
        # Check specific frequencies
        for swara, freq in freqs.items():
            self.assertIsInstance(freq, float)
            # All frequencies should be positive
            self.assertGreater(freq, 0)

    def test_get_compatible_rasas(self):
        """Test finding compatible emotional transitions."""
        # Test a valid rasa
        transitions = self.nw.get_compatible_rasas("Sringara")
        self.assertIsInstance(transitions, dict)
        self.assertIn("Haasya", transitions)
        
        # Check transition details
        for rasa, details in transitions.items():
            self.assertIn("transition_type", details)
            self.assertIn("energy_difference", details)
            self.assertIn("recommended_ragas", details)
        
        # Test an invalid rasa
        with self.assertRaises(ValueError):
            self.nw.get_compatible_rasas("InvalidRasa")

    def test_suggest_transition_path(self):
        """Test suggesting a transition path between rasas."""
        # Test direct path
        path = self.nw.suggest_transition_path("Sringara", "Haasya")
        self.assertEqual(path, ["Sringara", "Haasya"])
        
        # Test same rasa
        path = self.nw.suggest_transition_path("Sringara", "Sringara")
        self.assertEqual(path, ["Sringara"])
        
        # Test path with intermediate steps
        path = self.nw.suggest_transition_path("Karuna", "Veera")
        self.assertIsNotNone(path)
        self.assertGreater(len(path), 1)
        self.assertEqual(path[0], "Karuna")
        self.assertEqual(path[-1], "Veera")
        
        # Test invalid rasa
        with self.assertRaises(ValueError):
            self.nw.suggest_transition_path("InvalidRasa", "Sringara")

    def test_get_raga_thaat(self):
        """Test retrieving the thaat of a raga."""
        # Test a valid raga
        thaat = self.nw.get_raga_thaat("Yaman")
        self.assertEqual(thaat, "Kalyan")
        
        # Test a raga not in the mapping
        thaat = self.nw.get_raga_thaat("NonExistentRaga")
        self.assertIsNone(thaat)

    def test_get_western_equivalent(self):
        """Test finding Western equivalents for a raga."""
        # Test a valid raga
        equiv = self.nw.get_western_equivalent("Yaman")
        self.assertIsInstance(equiv, dict)
        self.assertEqual(equiv["scale_type"], "Lydian")
        self.assertEqual(equiv["thaat"], "Kalyan")
        
        # Check for rasas
        self.assertIsInstance(equiv["rasas"], list)
        
        # Check for Western correlations
        self.assertIsInstance(equiv["western_correlations"], list)

    def test_compare_raga_to_western_scale(self):
        """Test comparing a raga to a Western scale."""
        # Test a valid raga
        comparison = self.nw.compare_raga_to_western_scale("Yaman", "C", 4)
        self.assertIsInstance(comparison, dict)
        self.assertIn("raga_frequencies", comparison)
        self.assertIn("western_frequencies", comparison)
        
        # Check the Western scale type
        self.assertEqual(comparison["western_scale"], "C Lydian")
        
        # Check frequencies
        for freq_dict in [comparison["raga_frequencies"], comparison["western_frequencies"]]:
            self.assertIsInstance(freq_dict, dict)
            for name, freq in freq_dict.items():
                self.assertIsInstance(freq, float)
                self.assertGreater(freq, 0)

    def test_energy_levels(self):
        """Test the energy levels of rasas."""
        # Check that all rasas have energy levels
        for rasa in self.nw.rasas:
            self.assertIn(rasa, self.nw.energy_levels)
            # Energy levels should be between 1 and 10
            self.assertGreaterEqual(self.nw.energy_levels[rasa], 1)
            self.assertLessEqual(self.nw.energy_levels[rasa], 10)
        
        # Verify some specific energy levels
        self.assertEqual(self.nw.energy_levels["Veera"], 10)  # Highest energy
        self.assertEqual(self.nw.energy_levels["Saantha"], 1)  # Lowest energy


if __name__ == '__main__':
    unittest.main()