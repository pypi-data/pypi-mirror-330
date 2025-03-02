"""
Advanced tests for the command-line interface of SvaraScala.
"""

import unittest
from unittest.mock import patch
import io
import sys
import svarascala.__main__ as main_module
from svarascala.__main__ import main


class TestMainCLIAdvanced(unittest.TestCase):
    """Advanced test cases for the command-line interface."""

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_western_note_with_reference(self, mock_stdout):
        """Test western-note command with custom reference frequency."""
        test_args = ['svarascala', 'western-note', 'A', '4', '--reference', '432']
        with patch.object(sys, 'argv', test_args):
            main()
        
        output = mock_stdout.getvalue()
        self.assertIn('Note: A4', output)
        self.assertIn('Frequency: 432.00 Hz', output)
        
        # The reference affects all notes, so C4 should be lower
        # with A4=432Hz than with standard A4=440Hz
        test_args = ['svarascala', 'western-note', 'C', '4', '--reference', '432']
        with patch.object(sys, 'argv', test_args):
            mock_stdout.seek(0)
            mock_stdout.truncate()
            main()
        
        c4_432_output = mock_stdout.getvalue()
        c4_432_freq = float(c4_432_output.split('Frequency: ')[1].split(' Hz')[0])
        
        test_args = ['svarascala', 'western-note', 'C', '4', '--reference', '440']
        with patch.object(sys, 'argv', test_args):
            mock_stdout.seek(0)
            mock_stdout.truncate()
            main()
        
        c4_440_output = mock_stdout.getvalue()
        c4_440_freq = float(c4_440_output.split('Frequency: ')[1].split(' Hz')[0])
        
        # C4 with A4=432Hz should be lower than C4 with A4=440Hz
        self.assertLess(c4_432_freq, c4_440_freq)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_western_scale_various_types(self, mock_stdout):
        """Test western-scale command with various scale types."""
        # Test major scale
        test_args = ['svarascala', 'western-scale', 'D', '4', '--scale-type', 'major']
        with patch.object(sys, 'argv', test_args):
            main()
        
        major_output = mock_stdout.getvalue()
        self.assertIn('Scale: D major', major_output)
        self.assertIn('D4', major_output)
        self.assertIn('A4', major_output)  # Perfect fifth
        
        # Test minor scale
        test_args = ['svarascala', 'western-scale', 'D', '4', '--scale-type', 'minor']
        with patch.object(sys, 'argv', test_args):
            mock_stdout.seek(0)
            mock_stdout.truncate()
            main()
        
        minor_output = mock_stdout.getvalue()
        self.assertIn('Scale: D minor', minor_output)
        self.assertIn('D4', minor_output)
        self.assertIn('F4', minor_output)  # Minor third
        
        # Test blues scale
        test_args = ['svarascala', 'western-scale', 'D', '4', '--scale-type', 'blues']
        with patch.object(sys, 'argv', test_args):
            mock_stdout.seek(0)
            mock_stdout.truncate()
            main()
        
        blues_output = mock_stdout.getvalue()
        self.assertIn('Scale: D blues', blues_output)
        # Blues scale has 6 notes
        note_lines = [line for line in blues_output.split('\n') if 'D4' in line or 
                                                                  'F4' in line or 
                                                                  'G4' in line or 
                                                                  'G#4' in line or 
                                                                  'A4' in line or 
                                                                  'C5' in line]
        self.assertEqual(len(note_lines), 6)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_camelot_wheel(self, mock_stdout):
        """Test camelot command with various inputs."""
        # Test with camelot notation
        test_args = ['svarascala', 'camelot', '--camelot', '8B']
        with patch.object(sys, 'argv', test_args):
            main()
        
        camelot_output = mock_stdout.getvalue()
        self.assertIn('Camelot Notation: 8B', camelot_output)
        self.assertIn('Corresponding Key: A major', camelot_output)
        self.assertIn('8A', camelot_output)  # Relative minor
        
        # Test with key
        test_args = ['svarascala', 'camelot', '--key', 'C', '--scale-type', 'major']
        with patch.object(sys, 'argv', test_args):
            mock_stdout.seek(0)
            mock_stdout.truncate()
            main()
        
        key_output = mock_stdout.getvalue()
        self.assertIn('Key: C major', key_output)
        self.assertIn('Camelot Notation: 5B', key_output)
        
        # Test with frequencies
        test_args = ['svarascala', 'camelot', '--key', 'C', '--scale-type', 'major', 
                     '--octave', '4', '--with-frequencies']
        with patch.object(sys, 'argv', test_args):
            mock_stdout.seek(0)
            mock_stdout.truncate()
            main()
        
        freq_output = mock_stdout.getvalue()
        self.assertIn('Scale: C major, Octave: 4', freq_output)
        self.assertIn('C4', freq_output)
        self.assertIn('G4', freq_output)
        self.assertIn('Hz', freq_output)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_indian_swara_variants(self, mock_stdout):
        """Test indian-swara command with different variants."""
        # Test komal Re
        test_args = ['svarascala', 'indian-swara', 'Re', '--variant', 'komal']
        with patch.object(sys, 'argv', test_args):
            main()
        
        komal_output = mock_stdout.getvalue()
        self.assertIn('Swara: Re komal', komal_output)
        
        # Extract komal Re frequency
        komal_freq = float(komal_output.split('Frequency: ')[1].split(' Hz')[0])
        
        # Test shuddha Re
        test_args = ['svarascala', 'indian-swara', 'Re', '--variant', 'shuddha']
        with patch.object(sys, 'argv', test_args):
            mock_stdout.seek(0)
            mock_stdout.truncate()
            main()
        
        shuddha_output = mock_stdout.getvalue()
        self.assertIn('Swara: Re shuddha', shuddha_output)
        
        # Extract shuddha Re frequency
        shuddha_freq = float(shuddha_output.split('Frequency: ')[1].split(' Hz')[0])
        
        # Shuddha Re should be higher than komal Re
        self.assertGreater(shuddha_freq, komal_freq)
        
        # Test with custom reference
        test_args = ['svarascala', 'indian-swara', 'Sa', '--reference', '240']
        with patch.object(sys, 'argv', test_args):
            mock_stdout.seek(0)
            mock_stdout.truncate()
            main()
        
        sa_240_output = mock_stdout.getvalue()
        self.assertIn('Frequency: 240.00 Hz', sa_240_output)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_raga_comparisons(self, mock_stdout):
        """Test comparing different ragas using the indian-raga command."""
        # Test Yaman raga
        test_args = ['svarascala', 'indian-raga', 'Yaman']
        with patch.object(sys, 'argv', test_args):
            main()
        
        yaman_output = mock_stdout.getvalue()
        self.assertIn('Raga: Yaman', yaman_output)
        self.assertIn('Sa shuddha', yaman_output)
        self.assertIn('Ma tivra', yaman_output)  # Characteristic of Yaman
        
        # Test Bhairav raga
        test_args = ['svarascala', 'indian-raga', 'Bhairav']
        with patch.object(sys, 'argv', test_args):
            mock_stdout.seek(0)
            mock_stdout.truncate()
            main()
        
        bhairav_output = mock_stdout.getvalue()
        self.assertIn('Raga: Bhairav', bhairav_output)
        self.assertIn('Re komal', bhairav_output)  # Characteristic of Bhairav
        self.assertIn('Dha komal', bhairav_output)  # Characteristic of Bhairav
        
        # Simply check that Yaman has Re shuddha and Bhairav has Re komal
        self.assertIn('Re shuddha', yaman_output)
        self.assertIn('Re komal', bhairav_output)
    
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_help_output(self, mock_stdout):
        """Test CLI help output."""
        # Test main help
        test_args = ['svarascala', '--help']
        with patch.object(sys, 'argv', test_args):
            try:
                main()
                self.fail("Expected SystemExit was not raised")
            except SystemExit:
                pass  # Expected behavior - help command exits with code 0
        
        help_output = mock_stdout.getvalue()
        self.assertIn('SvaraScala', help_output)
        self.assertIn('Command', help_output)
        
        # Test command-specific help
        test_args = ['svarascala', 'western-note', '--help']
        with patch.object(sys, 'argv', test_args):
            try:
                mock_stdout.seek(0)
                mock_stdout.truncate()
                main()
                self.fail("Expected SystemExit was not raised")
            except SystemExit:
                pass  # Expected behavior - help command exits with code 0
        
        cmd_help_output = mock_stdout.getvalue()
        self.assertIn('western-note', cmd_help_output)
        self.assertIn('Note name', cmd_help_output)


if __name__ == '__main__':
    unittest.main()