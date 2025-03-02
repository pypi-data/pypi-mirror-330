"""
Western music frequency calculations for the SvaraScala library.

"Sunt autem haec: proslambanomenos, hypate hypaton, parhypate hypaton, lichanos
hypaton, hypate meson, parhypate meson, lichanos meson, mese, paramese, trite
diezeugmenon, paranete diezeugmenon, nete diezeugmenon, trite hyperbolaeon,
paranete hyperbolaeon, nete hyperbolaeon."
— Boethius, De institutione musica, Book IV

"These are as follows: the added note, the lowest of the lowest, the next to
lowest of the lowest, the index finger of the lowest, the lowest of the middle,
the next to lowest of the middle, the index finger of the middle, the middle,
the next to middle, the third of the separated, the next to last of the
separated, the last of the separated, the third of the highest, the next to
last of the highest, the last of the highest."

"Ut queant laxis
Resonare fibris,
Mira gestorum
Famuli tuorum,
Solve polluti
Labii reatum,
Sancte Ioannes."
- Guido d'Arezzo, Micrologus

"So that your servants
May sing with clear voices
The wonders of your deeds,
Remove the guilt
From our stained lips,
O Saint John."

"""

class WesternMusic:
    """
    Class to handle frequency calculations for Western music.
    """
    def __init__(self, reference_a4=440.0):
        """
        Initialize with a reference frequency for A4 (defaults to 440 Hz).
        
        Args:
            reference_a4 (float): Reference frequency for A4 in Hz. Default is 440.0 Hz.
        """
        self.reference_a4 = reference_a4
        self.notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        
        # Mapping between sharp and flat notations
        self.enharmonic_map = {
            'C#': 'Db', 'Db': 'C#',
            'D#': 'Eb', 'Eb': 'D#',
            'F#': 'Gb', 'Gb': 'F#',
            'G#': 'Ab', 'Ab': 'G#',
            'A#': 'Bb', 'Bb': 'A#'
        }
        
        self.solfege = ['Do', 'Di', 'Re', 'Ri', 'Mi', 'Fa', 'Fi', 'Sol', 'Si', 'La', 'Li', 'Ti']
        
        # Define Camelot Wheel mapping
        # The Camelot Wheel is organized with minor keys (A) and major keys (B) 
        # in a circle of fifths arrangement
        self.camelot_wheel = {
            # Major keys (B position)
            'B': {
                1: 'Ab',
                2: 'Eb',
                3: 'Bb',
                4: 'F',
                5: 'C',
                6: 'G',
                7: 'D',
                8: 'A',
                9: 'E',
                10: 'B',
                11: 'F#',
                12: 'Db'
            },
            # Minor keys (A position)
            'A': {
                1: 'Fm',
                2: 'Cm',
                3: 'Gm',
                4: 'Dm',
                5: 'Am',
                6: 'Em',
                7: 'Bm',
                8: 'F#m',
                9: 'C#m',
                10: 'G#m',
                11: 'D#m',
                12: 'A#m'
            }
        }
        
        # Reverse mapping for looking up Camelot notation from key
        self.key_to_camelot = {}
        for position in self.camelot_wheel:
            for number, key in self.camelot_wheel[position].items():
                self.key_to_camelot[key] = f"{number}{position}"
                
                # Add entries for enharmonic equivalents for major keys
                if position == 'B' and key in self.enharmonic_map:
                    enharmonic_key = self.enharmonic_map[key]
                    self.key_to_camelot[enharmonic_key] = f"{number}{position}"
                
                # Add entries for enharmonic equivalents for minor keys
                if position == 'A' and key.endswith('m'):
                    root = key[:-1]
                    if root in self.enharmonic_map:
                        enharmonic_root = self.enharmonic_map[root]
                        self.key_to_camelot[f"{enharmonic_root}m"] = f"{number}{position}"
    
    def get_frequency(self, note, octave):
        """
        Calculate the frequency of a given note in a given octave.
        
        Args:
            note (str): Note name (e.g., 'C', 'D#', 'F', etc.)
            octave (int): Octave number (e.g., 4 for middle C)
            
        Returns:
            float: Frequency in Hz
        
        Examples:
            >>> wm = WesternMusic()
            >>> round(wm.get_frequency('A', 4), 1)
            440.0
            >>> round(wm.get_frequency('C', 4), 1)
            261.6
            >>> round(wm.get_frequency('Db', 4), 1)  # Flat notation
            277.2
        """
        # Convert flat notation to sharp if needed
        if note not in self.notes and note in self.enharmonic_map:
            note = self.enharmonic_map[note]
        
        # Calculate semitone distance from A4
        if note not in self.notes:
            raise ValueError(f"Unknown note: {note}. Available notes: {', '.join(self.notes + list(set(self.enharmonic_map.keys()) - set(self.notes)))}")
            
        note_index = self.notes.index(note)
        a_index = self.notes.index('A')
        
        # Calculate semitone distance
        distance = note_index - a_index + (octave - 4) * 12
        
        # Calculate frequency using the formula: f = reference_a4 * (2^(n/12))
        frequency = self.reference_a4 * (2 ** (distance / 12))
        
        return frequency
    
    def get_solfege_frequency(self, solfege_name, octave, key='C'):
        """
        Calculate the frequency of a solfege syllable in a given key.
        
        Args:
            solfege_name (str): Solfege name (e.g., 'Do', 'Re', 'Mi', etc.)
            octave (int): Octave number
            key (str): Key to use as 'Do' (default is 'C')
            
        Returns:
            float: Frequency in Hz
        
        Examples:
            >>> wm = WesternMusic()
            >>> round(wm.get_solfege_frequency('Do', 4, 'C'), 1)
            261.6
            >>> round(wm.get_solfege_frequency('Sol', 4, 'C'), 1)
            392.0
        """
        # Find the index of the solfege name
        solfege_index = self.solfege.index(solfege_name)
        
        # Find the index of the key
        key_index = self.notes.index(key)
        
        # Calculate the actual note
        note_index = (key_index + solfege_index) % 12
        actual_note = self.notes[note_index]
        
        # Adjust octave if solfege crosses octave boundary
        octave_adjustment = (key_index + solfege_index) // 12
        actual_octave = octave + octave_adjustment
        
        return self.get_frequency(actual_note, actual_octave)
    
    def get_scale(self, root_note, octave, scale_type='major'):
        """
        Get frequencies for notes in a given scale.
        
        Args:
            root_note (str): Root note of the scale (e.g., 'C', 'F#', etc.)
            octave (int): Octave number for the root note
            scale_type (str): Type of scale ('major', 'minor', 'minor_harmonic', etc.)
            
        Returns:
            dict: Dictionary mapping note names to frequencies
        
        Examples:
            >>> wm = WesternMusic()
            >>> c_major = wm.get_scale('C', 4, 'major')
            >>> len(c_major)
            7
            >>> 'C4' in c_major
            True
        """
        # Define scale patterns (semitone intervals)
        scale_patterns = {
            'major': [0, 2, 4, 5, 7, 9, 11],
            'minor': [0, 2, 3, 5, 7, 8, 10],
            'minor_harmonic': [0, 2, 3, 5, 7, 8, 11],
            'minor_melodic': [0, 2, 3, 5, 7, 9, 11],
            'chromatic': list(range(12)),
            'pentatonic_major': [0, 2, 4, 7, 9],
            'pentatonic_minor': [0, 3, 5, 7, 10],
            'blues': [0, 3, 5, 6, 7, 10]
        }
        
        if scale_type not in scale_patterns:
            raise ValueError(f"Unknown scale type: {scale_type}")
        
        # Get the pattern for the requested scale
        pattern = scale_patterns[scale_type]
        
        # Get the index of the root note
        root_index = self.notes.index(root_note)
        
        # Calculate all notes in the scale
        scale = {}
        for i, interval in enumerate(pattern):
            # Calculate the note index
            note_index = (root_index + interval) % 12
            actual_note = self.notes[note_index]
            
            # Calculate the octave adjustment
            octave_adjustment = (root_index + interval) // 12
            actual_octave = octave + octave_adjustment
            
            # Get the frequency
            frequency = self.get_frequency(actual_note, actual_octave)
            
            # Add to the scale dictionary
            scale[f"{actual_note}{actual_octave}"] = frequency
            
        return scale
    
    def are_harmonic(self, note1, octave1, note2, octave2, tolerance=0.01):
        """
        Determine if two notes have a harmonic relationship.
        
        Args:
            note1 (str): First note name
            octave1 (int): Octave of first note
            note2 (str): Second note name
            octave2 (int): Octave of second note
            tolerance (float): Tolerance for ratio comparison
            
        Returns:
            tuple: (bool, str) - Whether harmonic and description of relationship
        
        Examples:
            >>> wm = WesternMusic()
            >>> wm.are_harmonic('C', 4, 'G', 4)[0]  # Perfect fifth
            True
            >>> wm.are_harmonic('C', 4, 'F#', 4)[0]  # Tritone
            False
        """
        # Get frequencies of both notes
        freq1 = self.get_frequency(note1, octave1)
        freq2 = self.get_frequency(note2, octave2)
        
        # Make sure freq1 is the lower frequency
        if freq1 > freq2:
            freq1, freq2 = freq2, freq1
        
        # Calculate the frequency ratio
        ratio = freq2 / freq1
        
        # Common harmonic ratios
        harmonic_ratios = [
            (2, 1),  # octave
            (3, 2),  # perfect fifth
            (4, 3),  # perfect fourth
            (5, 4),  # major third
            (6, 5),  # minor third
            (5, 3),  # major sixth
            (8, 5),  # minor sixth
            (9, 8),  # major second
            (16, 15) # minor second
        ]
        
        for num, denom in harmonic_ratios:
            harmonic_ratio = num / denom
            if abs(ratio - harmonic_ratio) < tolerance:
                return True, f"{num}:{denom} ratio ({harmonic_ratio:.3f})"
        
        return False, "Not a harmonic relationship"
    
    def get_camelot_notation(self, key, scale_type='major'):
        """
        Get the Camelot Wheel notation for a given key and scale type.
        
        Args:
            key (str): Root note of the key (e.g., 'C', 'F#', etc.)
            scale_type (str): Type of scale ('major' or 'minor')
            
        Returns:
            str: Camelot Wheel notation (e.g., '8B' for C major)
            
        Examples:
            >>> wm = WesternMusic()
            >>> wm.get_camelot_notation('C', 'major')
            '5B'
            >>> wm.get_camelot_notation('Am', 'minor')
            '5A'
        """
        # Handle minor keys with 'm' suffix
        if key.endswith('m'):
            key = key[:-1]
            scale_type = 'minor'
        
        # Create key string for lookup
        key_str = key
        if scale_type == 'minor':
            key_str += 'm'
        
        # Try to find the key in our mapping
        if key_str in self.key_to_camelot:
            return self.key_to_camelot[key_str]
        
        # If not found, try enharmonic equivalent
        if key in self.enharmonic_map:
            enharmonic_key = self.enharmonic_map[key]
            enharmonic_key_str = enharmonic_key
            if scale_type == 'minor':
                enharmonic_key_str += 'm'
            
            if enharmonic_key_str in self.key_to_camelot:
                return self.key_to_camelot[enharmonic_key_str]
        
        # If still not found, return None
        # This might happen if a non-standard key is provided
        return None
    
    def get_key_from_camelot(self, camelot_notation):
        """
        Get the musical key from a Camelot Wheel notation.
        
        Args:
            camelot_notation (str): Camelot Wheel notation (e.g., '8B')
            
        Returns:
            tuple: (key, scale_type) - e.g., ('C', 'major')
            
        Examples:
            >>> wm = WesternMusic()
            >>> wm.get_key_from_camelot('5B')
            ('C', 'major')
            >>> wm.get_key_from_camelot('5A')
            ('A', 'minor')
        """
        # Parse the Camelot notation
        if not camelot_notation or len(camelot_notation) < 2:
            raise ValueError("Invalid Camelot notation. Format should be like '8B'.")
        
        # Get number and position
        number = int(camelot_notation[:-1])
        position = camelot_notation[-1].upper()
        
        if position not in ['A', 'B']:
            raise ValueError("Invalid Camelot position. Should be 'A' or 'B'.")
        
        if number < 1 or number > 12:
            raise ValueError("Invalid Camelot number. Should be between 1 and 12.")
        
        # Get the key from the Camelot Wheel
        key = self.camelot_wheel[position][number]
        
        # Determine scale type and clean key name
        if position == 'A':  # Minor
            scale_type = 'minor'
            key = key[:-1]  # Remove 'm' suffix
        else:  # Major
            scale_type = 'major'
        
        return (key, scale_type)
    
    def get_compatible_keys(self, camelot_notation):
        """
        Get compatible keys for harmonic mixing based on Camelot Wheel.
        
        Args:
            camelot_notation (str): Camelot Wheel notation (e.g., '8B')
            
        Returns:
            dict: Dictionary of compatible keys and their Camelot notations
            
        Examples:
            >>> wm = WesternMusic()
            >>> compatible = wm.get_compatible_keys('5B')
            >>> '5A' in compatible
            True
        """
        if not camelot_notation or len(camelot_notation) < 2:
            raise ValueError("Invalid Camelot notation. Format should be like '8B'.")
        
        # Parse the Camelot notation
        number = int(camelot_notation[:-1])
        position = camelot_notation[-1].upper()
        
        if position not in ['A', 'B']:
            raise ValueError("Invalid Camelot position. Should be 'A' or 'B'.")
        
        if number < 1 or number > 12:
            raise ValueError("Invalid Camelot number. Should be between 1 and 12.")
        
        # Build dictionary of compatible keys
        compatible = {}
        
        # Same number, different position (relative major/minor)
        opposite_position = 'A' if position == 'B' else 'B'
        relative_key = f"{number}{opposite_position}"
        key, scale_type = self.get_key_from_camelot(relative_key)
        compatible[relative_key] = f"{key}{'m' if scale_type == 'minor' else ''}"
        
        # Same position, adjacent numbers (+1, -1) (perfect fifth transitions)
        for adj in [-1, 1]:
            adj_number = (number + adj) % 12
            if adj_number == 0:
                adj_number = 12
            adj_key = f"{adj_number}{position}"
            key, scale_type = self.get_key_from_camelot(adj_key)
            compatible[adj_key] = f"{key}{'m' if scale_type == 'minor' else ''}"
        
        # Diagonal movement (energy boost/drop)
        diagonal_number = (number + 1) % 12
        if diagonal_number == 0:
            diagonal_number = 12
        diagonal_key = f"{diagonal_number}{opposite_position}"
        key, scale_type = self.get_key_from_camelot(diagonal_key)
        compatible[diagonal_key] = f"{key}{'m' if scale_type == 'minor' else ''}"
        
        return compatible
    
    def get_scale_with_camelot(self, root_note, octave, scale_type='major'):
        """
        Get scale with Camelot Wheel information.
        
        Args:
            root_note (str): Root note of the scale (e.g., 'C', 'F#', etc.)
            octave (int): Octave number for the root note
            scale_type (str): Type of scale ('major' or 'minor')
            
        Returns:
            dict: Dictionary with frequencies, Camelot notation, and compatible keys
            
        Examples:
            >>> wm = WesternMusic()
            >>> scale_info = wm.get_scale_with_camelot('C', 4, 'major')
            >>> 'camelot_notation' in scale_info
            True
            >>> 'compatible_keys' in scale_info
            True
        """
        # Get the scale frequencies
        scale_freqs = self.get_scale(root_note, octave, scale_type)
        
        # Get the Camelot notation
        camelot = self.get_camelot_notation(root_note, scale_type)
        
        # Get compatible keys
        compatible_keys = self.get_compatible_keys(camelot) if camelot else {}
        
        # Combine into one result
        result = {
            'frequencies': scale_freqs,
            'camelot_notation': camelot,
            'compatible_keys': compatible_keys
        }
        
        return result
    
'''
"Sed haec quae de Musica breviter dicta sunt, tironibus interim satisfaciant,
quatenus huius artis prima vestibula ingredientes, hanc multiplicem variamque
notarum formam sine magistro penetrare valeant; quod hactenus neminem potuisse
vidimus. Vocum autem industria iuxta consimilem modificationem diligens lector
poterit inspicere. His itaque praelibatis, cum divina gratia, omnium opifice
bonorum, quae sine invidia communicat affluentissime, ea quae de Musica dicenda
sunt, quibuslibet cantoribus utilissima percipiant."
- Guido d'Arezzo, Micrologus

"But let these things, which have been briefly said about Music, satisfy
beginners for now, so that those entering the first doors of this art may be
able to penetrate this complex and varied form of notation without a teacher;
which we have seen no one able to do until now. The diligent reader will be
able to examine the industry of voices according to a similar modification. So,
having touched on these things, with divine grace, the maker of all good
things, which communicates most abundantly without envy, may they receive those
things which are to be said about Music, most useful to any singers."
'''