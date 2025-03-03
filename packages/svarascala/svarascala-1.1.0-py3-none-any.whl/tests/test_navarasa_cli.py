"""
Tests for the Navarasa wheel CLI functionality of SvaraScala.
"""

import unittest
from unittest.mock import patch
import io
import sys
import svarascala.__main__ as main_module
from svarascala.__main__ import main


class TestNavarasaCLI(unittest.TestCase):
    """Test cases for the Navarasa wheel CLI functionality."""

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_navarasa_general_info(self, mock_stdout):
        """Test the navarasa command with no specific parameters."""
        test_args = ['svarascala', 'navarasa']
        with patch.object(sys, 'argv', test_args):
            main()
        
        output = mock_stdout.getvalue()
        self.assertIn('Navarasa (Nine Sentiments)', output)
        self.assertIn('Sringara', output)
        self.assertIn('Karuna', output)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_navarasa_rasa_info(self, mock_stdout):
        """Test the navarasa command with a specific rasa."""
        test_args = ['svarascala', 'navarasa', '--rasa', 'Sringara']
        with patch.object(sys, 'argv', test_args):
            main()
        
        output = mock_stdout.getvalue()
        self.assertIn('Rasa: Sringara', output)
        self.assertIn('English: Love/Erotic', output)
        self.assertIn('Associated Ragas:', output)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_navarasa_raga_info(self, mock_stdout):
        """Test the navarasa command with a specific raga."""
        test_args = ['svarascala', 'navarasa', '--raga', 'Yaman']
        with patch.object(sys, 'argv', test_args):
            main()
        
        output = mock_stdout.getvalue()
        self.assertIn('Raga: Yaman', output)
        self.assertIn('Associated Rasas:', output)
        self.assertIn('Sringara', output)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_navarasa_raga_with_frequencies(self, mock_stdout):
        """Test the navarasa command with a raga and frequencies."""
        test_args = ['svarascala', 'navarasa', '--raga', 'Yaman', '--with-frequencies']
        with patch.object(sys, 'argv', test_args):
            main()
        
        output = mock_stdout.getvalue()
        self.assertIn('Raga: Yaman', output)
        self.assertIn('Frequencies:', output)
        self.assertIn('Hz', output)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_navarasa_raga_with_western(self, mock_stdout):
        """Test the navarasa command with a raga and Western equivalents."""
        test_args = ['svarascala', 'navarasa', '--raga', 'Yaman', '--with-western']
        with patch.object(sys, 'argv', test_args):
            main()
        
        output = mock_stdout.getvalue()
        self.assertIn('Raga: Yaman', output)
        self.assertIn('Western equivalent:', output)
        self.assertIn('Thaat:', output)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_navarasa_rasa_with_transitions(self, mock_stdout):
        """Test the navarasa command with a rasa and transitions."""
        test_args = ['svarascala', 'navarasa', '--rasa', 'Sringara', '--with-transitions']
        with patch.object(sys, 'argv', test_args):
            main()
        
        output = mock_stdout.getvalue()
        self.assertIn('Rasa: Sringara', output)
        self.assertIn('Compatible Emotional Transitions:', output)
        self.assertIn('Recommended ragas:', output)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_navarasa_transition_path(self, mock_stdout):
        """Test the navarasa command with transition path."""
        test_args = ['svarascala', 'navarasa', '--from-rasa', 'Karuna', '--to-rasa', 'Veera']
        with patch.object(sys, 'argv', test_args):
            main()
        
        output = mock_stdout.getvalue()
        self.assertIn('Finding transition path from Karuna to Veera', output)
        self.assertIn('Recommended path:', output)
        self.assertIn('Details for each stage:', output)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_navarasa_invalid_rasa(self, mock_stdout):
        """Test the navarasa command with an invalid rasa."""
        test_args = ['svarascala', 'navarasa', '--rasa', 'InvalidRasa']
        with patch.object(sys, 'argv', test_args):
            main()
        
        output = mock_stdout.getvalue()
        self.assertIn('Error:', output)
        self.assertIn('Unknown rasa', output)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_navarasa_unknown_raga(self, mock_stdout):
        """Test the navarasa command with a raga not in the classification."""
        test_args = ['svarascala', 'navarasa', '--raga', 'UnknownRaga']
        with patch.object(sys, 'argv', test_args):
            main()
        
        output = mock_stdout.getvalue()
        self.assertIn('Raga: UnknownRaga', output)
        self.assertIn('This raga is not classified in the Navarasa system', output)


if __name__ == '__main__':
    unittest.main()