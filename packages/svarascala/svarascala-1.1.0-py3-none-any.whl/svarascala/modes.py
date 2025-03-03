"""
Western modes functionality for the SvaraScala library.

This module implements emotional mapping for Western musical modes,
providing a parallel to the Navarasa system for Indian classical music.

"What passion cannot Music raise and quell?
When Jubal struck the corded shell,
His listening brethren stood around,
And, wondering, on their faces fell
To worship that celestial sound.
Less than a god they thought there could not dwell
Within the hollow of that shell
That spoke so sweetly and so well."
— John Dryden, "A Song for St. Cecilia's Day" (1687)
"""

from .western import WesternMusic

class WesternModes:
    """
    Class to handle Western modal music and emotional associations.
    """
    def __init__(self, reference_a4=440.0):
        """
        Initialize with a reference frequency for A4 (defaults to 440 Hz).
        
        Args:
            reference_a4 (float): Reference frequency for A4 in Hz. Default is 440.0 Hz.
        """
        self.western = WesternMusic(reference_a4=reference_a4)
        
        # Define the Western modes (as rotations of the major scale)
        self.modes = {
            "Ionian": [0, 2, 4, 5, 7, 9, 11],      # Major scale
            "Dorian": [0, 2, 3, 5, 7, 9, 10],      # Minor with raised 6th
            "Phrygian": [0, 1, 3, 5, 7, 8, 10],    # Minor with lowered 2nd
            "Lydian": [0, 2, 4, 6, 7, 9, 11],      # Major with raised 4th
            "Mixolydian": [0, 2, 4, 5, 7, 9, 10],  # Major with lowered 7th
            "Aeolian": [0, 2, 3, 5, 7, 8, 10],     # Natural minor scale
            "Locrian": [0, 1, 3, 5, 6, 8, 10]      # Diminished scale
        }
        
        # Modal emotional characteristics
        self.modal_emotions = {
            "Ionian": {
                "primary": "Joy",
                "character": "Happy, stable, resolved",
                "moods": ["Cheerful", "Confident", "Triumphant", "Straightforward"],
                "western_parallel": "Major scale",
                "energy_level": 8,
                "emotional_intensity": 7
            },
            "Dorian": {
                "primary": "Serious",
                "character": "Contemplative, balanced, sophisticated",
                "moods": ["Melancholic", "Dignified", "Mysterious", "Introspective"],
                "western_parallel": "Minor scale with raised 6th",
                "energy_level": 5,
                "emotional_intensity": 6
            },
            "Phrygian": {
                "primary": "Tension",
                "character": "Exotic, dark, intense",
                "moods": ["Mystical", "Exotic", "Tense", "Yearning"],
                "western_parallel": "Spanish/Flamenco sound",
                "energy_level": 6,
                "emotional_intensity": 8
            },
            "Lydian": {
                "primary": "Wonder",
                "character": "Bright, dreamlike, transcendent",
                "moods": ["Magical", "Ethereal", "Floating", "Whimsical"],
                "western_parallel": "Sci-fi/Fantasy sound",
                "energy_level": 7,
                "emotional_intensity": 6
            },
            "Mixolydian": {
                "primary": "Playful",
                "character": "Bluesy, restless, adventurous",
                "moods": ["Folky", "Rustic", "Unresolved", "Wandering"],
                "western_parallel": "Blues/Rock sound",
                "energy_level": 9,
                "emotional_intensity": 8
            },
            "Aeolian": {
                "primary": "Sadness",
                "character": "Melancholic, emotional, natural",
                "moods": ["Sorrowful", "Brooding", "Reflective", "Serious"],
                "western_parallel": "Natural minor scale",
                "energy_level": 4,
                "emotional_intensity": 9
            },
            "Locrian": {
                "primary": "Instability",
                "character": "Anxious, unstable, dissonant",
                "moods": ["Tense", "Uncertain", "Chaotic", "Disoriented"],
                "western_parallel": "Diminished scale feel",
                "energy_level": 7,
                "emotional_intensity": 10
            }
        }
        
        # Historical eras and style characteristics
        self.historical_usage = {
            "Ionian": {
                "eras": ["Renaissance", "Classical", "Baroque", "Modern"],
                "prominence": "Dominant from Common Practice Period onward",
                "contexts": ["Hymns", "Anthems", "Triumphant pieces"]
            },
            "Dorian": {
                "eras": ["Medieval", "Renaissance", "Folk", "Jazz", "Modern"],
                "prominence": "Common in early church music, folk music",
                "contexts": ["Folk songs", "Modal jazz", "Renaissance polyphony"]
            },
            "Phrygian": {
                "eras": ["Medieval", "Renaissance", "Flamenco", "Modern"],
                "prominence": "Spanish music, metal, film scoring",
                "contexts": ["Spanish music", "Metal", "Exotic film scoring"]
            },
            "Lydian": {
                "eras": ["Medieval", "Jazz", "Film", "Modern"],
                "prominence": "Popular in film music, jazz",
                "contexts": ["Film scores", "Jazz improvisation", "Dream sequences"]
            },
            "Mixolydian": {
                "eras": ["Medieval", "Folk", "Rock", "Jazz", "Modern"],
                "prominence": "Common in Celtic folk, rock, blues",
                "contexts": ["Folk music", "Blues", "Rock", "Jazz dominant chords"]
            },
            "Aeolian": {
                "eras": ["Baroque", "Romantic", "Pop", "Rock", "Modern"],
                "prominence": "Dominant minor mode since Baroque era",
                "contexts": ["Pop/Rock", "Film music", "Classical minor key works"]
            },
            "Locrian": {
                "eras": ["Modern", "Contemporary", "Avant-garde"],
                "prominence": "Rare, mostly theoretical until 20th century",
                "contexts": ["Experimental music", "Modern jazz", "Metal"]
            }
        }
        
        # Used for suggesting emotional transitions
        self.compatible_transitions = {
            "Ionian": ["Mixolydian", "Lydian", "Dorian"],
            "Dorian": ["Aeolian", "Phrygian", "Mixolydian", "Ionian"],
            "Phrygian": ["Aeolian", "Dorian", "Locrian"],
            "Lydian": ["Ionian", "Mixolydian", "Dorian", "Aeolian"],
            "Mixolydian": ["Ionian", "Dorian", "Lydian", "Aeolian"],
            "Aeolian": ["Dorian", "Phrygian", "Mixolydian", "Lydian"],
            "Locrian": ["Phrygian"]
        }
        
        # Map modes to Navarasa for cultural bridging
        self.mode_to_rasa_map = {
            "Ionian": ["Sringara", "Haasya"],       # Joy ~ Love/Comedy
            "Dorian": ["Adbutham", "Saantha"],      # Serious ~ Wonder/Peace
            "Phrygian": ["Bhayaanaka", "Beebhatsa"], # Tension ~ Fear/Disgust
            "Lydian": ["Adbutham", "Sringara"],     # Wonder ~ Wonder/Love
            "Mixolydian": ["Veera", "Haasya"],      # Playful ~ Heroism/Comedy
            "Aeolian": ["Karuna"],                  # Sadness ~ Compassion
            "Locrian": ["Raudra", "Bhayaanaka"]     # Instability ~ Anger/Fear
        }
        
        # Instruments that particularly emphasize modal characteristics
        self.modal_instruments = {
            "Ionian": ["Piano", "Trumpet", "Violin", "Orchestra"],
            "Dorian": ["Guitar", "Piano", "Saxophone", "Clarinet"],
            "Phrygian": ["Flamenco guitar", "Oud", "Sitar", "Oboe"],
            "Lydian": ["Harp", "Vibraphone", "Flute", "Synthesizer"],
            "Mixolydian": ["Electric guitar", "Fiddle", "Bagpipes", "Banjo"],
            "Aeolian": ["Cello", "Piano", "Violin", "Guitar"],
            "Locrian": ["Percussion", "Prepared piano", "Distorted guitar", "Synthesizer"]
        }
    
    def get_mode_intervals(self, mode_name):
        """
        Get the interval pattern for a specific mode.
        
        Args:
            mode_name (str): Name of the mode (e.g., "Dorian", "Lydian")
            
        Returns:
            list: List of semitone intervals from the root
            
        Examples:
            >>> wm = WesternModes()
            >>> wm.get_mode_intervals("Dorian")
            [0, 2, 3, 5, 7, 9, 10]
        """
        if mode_name not in self.modes:
            raise ValueError(f"Unknown mode: {mode_name}. Available modes: {', '.join(self.modes.keys())}")
        
        return self.modes[mode_name]
    
    def get_mode_info(self, mode_name):
        """
        Get information about a specific Western mode.
        
        Args:
            mode_name (str): Name of the mode (e.g., "Dorian", "Lydian")
            
        Returns:
            dict: Information about the mode
            
        Examples:
            >>> wm = WesternModes()
            >>> info = wm.get_mode_info("Dorian")
            >>> info["primary"]
            'Serious'
        """
        if mode_name not in self.modal_emotions:
            raise ValueError(f"Unknown mode: {mode_name}. Available modes: {', '.join(self.modal_emotions.keys())}")
        
        return self.modal_emotions[mode_name]
    
    def get_mode_frequencies(self, mode_name, root_note, octave):
        """
        Calculate frequencies for all notes in a given mode.
        
        Args:
            mode_name (str): Name of the mode
            root_note (str): Root note of the mode (e.g., 'C', 'F#')
            octave (int): Octave number for the root note
            
        Returns:
            dict: Dictionary mapping note names to frequencies
            
        Examples:
            >>> wm = WesternModes()
            >>> freqs = wm.get_mode_frequencies("Dorian", "D", 4)
            >>> len(freqs)
            7
        """
        # Get the mode intervals
        intervals = self.get_mode_intervals(mode_name)
        
        # Get the index of the root note
        root_index = self.western.notes.index(root_note)
        
        # Calculate all notes in the mode
        scale = {}
        for i, interval in enumerate(intervals):
            # Calculate the note index
            note_index = (root_index + interval) % 12
            actual_note = self.western.notes[note_index]
            
            # Calculate the octave adjustment
            octave_adjustment = (root_index + interval) // 12
            actual_octave = octave + octave_adjustment
            
            # Get the frequency
            frequency = self.western.get_frequency(actual_note, actual_octave)
            
            # Add to the scale dictionary
            scale[f"{actual_note}{actual_octave}"] = frequency
            
        return scale
    
    def get_compatible_modes(self, mode_name):
        """
        Find compatible emotional transitions from one mode to another.
        
        Args:
            mode_name (str): The starting mode
            
        Returns:
            dict: Dictionary of target modes with transition information
            
        Examples:
            >>> wm = WesternModes()
            >>> transitions = wm.get_compatible_modes("Ionian")
            >>> "Lydian" in transitions
            True
        """
        if mode_name not in self.compatible_transitions:
            raise ValueError(f"Unknown mode: {mode_name}. Available modes: {', '.join(self.compatible_transitions.keys())}")
        
        transitions = {}
        for target_mode in self.compatible_transitions[mode_name]:
            # Determine the transition type based on energy levels
            source_energy = self.modal_emotions[mode_name]["energy_level"]
            target_energy = self.modal_emotions[target_mode]["energy_level"]
            
            source_intensity = self.modal_emotions[mode_name]["emotional_intensity"]
            target_intensity = self.modal_emotions[target_mode]["emotional_intensity"]
            
            if target_energy > source_energy:
                energy_type = "Energy boost"
            elif target_energy < source_energy:
                energy_type = "Energy reduction"
            else:
                energy_type = "Energy maintenance"
            
            if target_intensity > source_intensity:
                intensity_type = "Intensity increase"
            elif target_intensity < source_intensity:
                intensity_type = "Intensity decrease"
            else:
                intensity_type = "Intensity maintenance"
            
            # Calculate energy difference percentage
            energy_diff = abs(((target_energy - source_energy) / source_energy) * 100)
            
            transitions[target_mode] = {
                "primary_emotion": self.modal_emotions[target_mode]["primary"],
                "character": self.modal_emotions[target_mode]["character"],
                "energy_transition": energy_type,
                "intensity_transition": intensity_type,
                "energy_difference": f"{energy_diff:.1f}%",
                "energy_level": target_energy,
                "emotional_intensity": target_intensity,
                "recommended_instruments": self.modal_instruments[target_mode]
            }
        
        return transitions
    
    def suggest_transition_path(self, start_mode, end_mode, max_steps=3):
        """
        Suggest a transition path from one mode to another.
        
        Args:
            start_mode (str): The starting mode
            end_mode (str): The target mode
            max_steps (int): Maximum number of transitions allowed
            
        Returns:
            list: List of modes forming the transition path, or None if no path found
            
        Examples:
            >>> wm = WesternModes()
            >>> path = wm.suggest_transition_path("Ionian", "Aeolian")
            >>> len(path) > 0
            True
        """
        if start_mode not in self.compatible_transitions:
            raise ValueError(f"Unknown starting mode: {start_mode}")
            
        if end_mode not in self.modal_emotions:
            raise ValueError(f"Unknown ending mode: {end_mode}")
            
        if start_mode == end_mode:
            return [start_mode]
        
        # Simple BFS to find shortest path
        visited = {start_mode}
        queue = [[start_mode]]
        
        while queue:
            path = queue.pop(0)
            current = path[-1]
            
            if current == end_mode:
                return path
            
            if len(path) >= max_steps:
                continue
            
            for next_mode in self.compatible_transitions[current]:
                if next_mode not in visited:
                    visited.add(next_mode)
                    queue.append(path + [next_mode])
        
        return None  # No path found within max_steps
    
    def get_corresponding_rasa(self, mode_name):
        """
        Get the Navarasa (Indian emotion) equivalents for a Western mode.
        
        Args:
            mode_name (str): Name of the Western mode
            
        Returns:
            list: List of corresponding Navarasa emotions
            
        Examples:
            >>> wm = WesternModes()
            >>> rasas = wm.get_corresponding_rasa("Ionian")
            >>> "Sringara" in rasas
            True
        """
        if mode_name not in self.mode_to_rasa_map:
            raise ValueError(f"Unknown mode: {mode_name}. Available modes: {', '.join(self.mode_to_rasa_map.keys())}")
        
        return self.mode_to_rasa_map[mode_name]
    
    def get_historical_usage(self, mode_name):
        """
        Get historical usage information for a specific mode.
        
        Args:
            mode_name (str): Name of the mode
            
        Returns:
            dict: Historical usage information
            
        Examples:
            >>> wm = WesternModes()
            >>> history = wm.get_historical_usage("Dorian")
            >>> "eras" in history
            True
        """
        if mode_name not in self.historical_usage:
            raise ValueError(f"Unknown mode: {mode_name}. Available modes: {', '.join(self.historical_usage.keys())}")
        
        return self.historical_usage[mode_name]
    
    def compare_mode_to_raga(self, mode_name, root_note, octave, from_navarasa=None):
        """
        Compare a Western mode to related Indian ragas based on emotional qualities.
        
        Args:
            mode_name (str): Name of the Western mode
            root_note (str): Root note for the mode
            octave (int): Octave number
            from_navarasa (object, optional): NavarasaMap instance for raga lookup
            
        Returns:
            dict: Comparison information
            
        Examples:
            >>> wm = WesternModes()
            >>> from navarasa import NavarasaMap
            >>> nv = NavarasaMap()
            >>> comparison = wm.compare_mode_to_raga("Dorian", "D", 4, nv)
            >>> "western_frequencies" in comparison
            True
        """
        # Get the mode frequencies
        mode_freqs = self.get_mode_frequencies(mode_name, root_note, octave)
        
        # Get corresponding rasas
        corresponding_rasas = self.get_corresponding_rasa(mode_name)
        
        result = {
            "mode": mode_name,
            "root": root_note,
            "octave": octave,
            "corresponding_rasas": corresponding_rasas,
            "emotional_character": self.modal_emotions[mode_name]["character"],
            "western_frequencies": mode_freqs
        }
        
        # If NavarasaMap is provided, get related ragas
        if from_navarasa is not None:
            related_ragas = []
            for rasa in corresponding_rasas:
                try:
                    ragas = from_navarasa.get_raga_by_rasa(rasa)
                    related_ragas.extend(ragas)
                except ValueError:
                    # Rasa might not exist in the NavarasaMap implementation
                    pass
            
            # De-duplicate ragas
            related_ragas = list(set(related_ragas))
            
            # Get frequencies for the first related raga if available
            raga_frequencies = {}
            if related_ragas:
                try:
                    raga_frequencies = from_navarasa.get_raga_frequencies(related_ragas[0])
                except Exception:
                    pass
            
            result["related_ragas"] = related_ragas
            result["example_raga_frequencies"] = raga_frequencies
        
        return result
    
    def get_common_chord_progressions(self, mode_name):
        """
        Get common chord progressions that exemplify a particular mode.
        
        Args:
            mode_name (str): Name of the mode
            
        Returns:
            list: List of common chord progressions in Roman numerals
            
        Examples:
            >>> wm = WesternModes()
            >>> progressions = wm.get_common_chord_progressions("Ionian")
            >>> len(progressions) > 0
            True
        """
        # Define common chord progressions for each mode
        progressions = {
            "Ionian": [
                "I - IV - V - I",
                "I - vi - IV - V",
                "I - V - vi - IV",
                "I - IV - I - V"
            ],
            "Dorian": [
                "i - IV - i",
                "i - IV - VII",
                "i - IV - v - i",
                "i - VII - IV - i"
            ],
            "Phrygian": [
                "i - ♭II - i",
                "i - ♭II - ♭VII - i",
                "i - v - ♭II - i",
                "i - ♭II - ♭III - ♭II"
            ],
            "Lydian": [
                "I - II - I",
                "I - II - vii - I",
                "I - II - V - I",
                "I - II - IV# - I"  # IV# is the augmented fourth
            ],
            "Mixolydian": [
                "I - ♭VII - I",
                "I - ♭VII - IV - I",
                "I - v - ♭VII - IV",
                "I - ♭VII - v - IV"
            ],
            "Aeolian": [
                "i - ♭VI - ♭VII - i",
                "i - ♭VII - ♭VI - i",
                "i - iv - ♭VII - i",
                "i - v - ♭VI - ♭VII"
            ],
            "Locrian": [
                "i° - ♭II - ♭VII - i°",  # i° = diminished i chord
                "i° - ♭V - ♭II - i°",
                "i° - ♭II - ♭III - i°",
                "i° - ♭VII - ♭VI - ♭VII"
            ]
        }
        
        if mode_name not in progressions:
            raise ValueError(f"Unknown mode: {mode_name}. Available modes: {', '.join(progressions.keys())}")
        
        return progressions[mode_name]


'''
"The Greeks distinguished three genera of music: the diatonic, the chromatic,
and the enharmonic. The diatonic was thought to be the most natural... The 
chromatic was so called from the Greek word for color, because it was a 
modification of the natural scale, and because the chromatic scale was often
marked with colored characters. The enharmonic was so called because it was
perfectly consonant throughout, or, as others think, because of the agreement
of the unison."
- Thomas Morley, A Plain and Easy Introduction to Practical Music (1597)
'''