"""
Tests for the command-line interface of SvaraScala.
"""

import unittest
from unittest.mock import patch
import io
import sys
import svarascala.__main__ as main_module
from svarascala.__main__ import main


class TestMainCLI(unittest.TestCase):
    """Test cases for the command-line interface."""

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_western_note_info(self, mock_stdout):
        """Test the western-note command."""
        test_args = ['svarascala', 'western-note', 'A', '4']
        with patch.object(sys, 'argv', test_args):
            main()
        
        output = mock_stdout.getvalue()
        self.assertIn('Note: A4', output)
        self.assertIn('Frequency: 440.00 Hz', output)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_western_scale_info(self, mock_stdout):
        """Test the western-scale command."""
        test_args = ['svarascala', 'western-scale', 'C', '4', '--scale-type', 'major']
        with patch.object(sys, 'argv', test_args):
            main()
        
        output = mock_stdout.getvalue()
        self.assertIn('Scale: C major', output)
        self.assertIn('C4', output)
        self.assertIn('G4', output)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_indian_swara_info(self, mock_stdout):
        """Test the indian-swara command."""
        test_args = ['svarascala', 'indian-swara', 'Sa']
        with patch.object(sys, 'argv', test_args):
            main()
        
        output = mock_stdout.getvalue()
        self.assertIn('Swara: Sa shuddha', output)
        self.assertIn('220.00 Hz', output)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_indian_raga_info(self, mock_stdout):
        """Test the indian-raga command."""
        test_args = ['svarascala', 'indian-raga', 'Yaman']
        with patch.object(sys, 'argv', test_args):
            main()
        
        output = mock_stdout.getvalue()
        self.assertIn('Raga: Yaman', output)
        self.assertIn('Sa shuddha', output)
        self.assertIn('Ma tivra', output)


if __name__ == '__main__':
    unittest.main()