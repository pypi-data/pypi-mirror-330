"""
Navarasa (Nine Sentiments) functionality for the SvaraScala library.

This module implements a map system for Indian classical music based on the
Navarasas (nine sentiments or emotions) from Indian aesthetic theory, similar
to how the Camelot Wheel functions for Western music.

"तत्र विभावानुभावव्यभिचारिसंयोगाद् रसनिष्पत्तिः"
— Natyashastra, 6.33

"The sentiment (rasa) is produced from the combination of determinants
(vibhava), consequents (anubhava), and transitory states
(vyabhicharibhava)."

"नवरसा: कला का आत्मा हैं। ये रस हमारे अंतर्मन के भावों को संगीत के माध्यम से व्यक्त करते हैं।"
— Traditional Sanskrit saying

"The nine rasas are the soul of art. These sentiments express our inner emotions
through the medium of music."
"""

from .indian import IndianMusic
from .western import WesternMusic

class NavarasaMap:
    """
    Class to create a harmonic wheel based on the Navarasas (nine sentiments)
    of Indian classical music.
    """
    
    def __init__(self, reference_sa=220.0):
        """
        Initialize with a reference frequency for Sa (defaults to 220 Hz).
        
        Args:
            reference_sa (float): Reference frequency for Sa in Hz. Default is 220.0 Hz.
        """
        self.indian = IndianMusic(reference_sa=reference_sa)
        
        # Define the nine rasas and their characteristics
        self.rasas = {
            "Sringara": {
                "english": "Love/Erotic",
                "mood": "Love",
                "time": "Evening",
                "color": "Light green"
            },
            "Haasya": {
                "english": "Comedy/Laughter",
                "mood": "Satire",
                "time": "Morning",
                "color": "White"
            },
            "Karuna": {
                "english": "Compassion/Sympathy",
                "mood": "Pathos",
                "time": "Late evening",
                "color": "Grey"
            },
            "Raudra": {
                "english": "Anger/Fury",
                "mood": "Fury",
                "time": "Noon",
                "color": "Red"
            },
            "Veera": {
                "english": "Bravery/Heroism",
                "mood": "Valour",
                "time": "Dawn",
                "color": "Yellow"
            },
            "Bhayaanaka": {
                "english": "Terror/Fear",
                "mood": "Fright",
                "time": "Night",
                "color": "Black"
            },
            "Beebhatsa": {
                "english": "Disgust/Aversion",
                "mood": "Aversion",
                "time": "Dusk",
                "color": "Blue"
            },
            "Adbutham": {
                "english": "Wonder/Amazement",
                "mood": "Amazement",
                "time": "Midnight",
                "color": "Yellow"
            },
            "Saantha": {
                "english": "Peace/Tranquility",
                "mood": "Serenity",
                "time": "Late night",
                "color": "White"
            }
        }
        
        # Define ragas associated with each rasa
        # These associations are based on traditional classifications
        self.rasa_ragas = {
            "Sringara": ["Yaman", "Behag", "Hameer", "Tilak Kamod", "Desh"],
            "Haasya": ["Durga", "Pahadi", "Jog", "Nat Kamod", "Bahar"],
            "Karuna": ["Bhairavi", "Malkauns", "Bageshri", "Todi", "Bilaskhani Todi"],
            "Raudra": ["Bhairav", "Marwa", "Chandrakauns", "Shree", "Hindol"],
            "Veera": ["Bilawal", "Darbari", "Jaijaiwanti", "Maand", "Kedar"],
            "Bhayaanaka": ["Shree", "Purvi", "Gauri", "Lalit", "Vrindavani Sarang"],
            "Beebhatsa": ["Todi", "Komal Rishabh Asavari", "Bhimpalasi", "Jogiya", "Vibhas"],
            "Adbutham": ["Darbari", "Miyan Ki Malhar", "Champakali", "Madhuvanti", "Gaud Sarang"],
            "Saantha": ["Bhimpalasi", "Jaunpuri", "Ahir Bhairav", "Bairagi", "Pahadi"]
        }
        
        # Define transition rules between rasas
        # These transitions represent emotionally coherent progressions
        self.compatible_transitions = {
            "Sringara": ["Haasya", "Adbutham", "Saantha", "Karuna"],
            "Haasya": ["Sringara", "Veera", "Adbutham", "Saantha"],
            "Karuna": ["Saantha", "Sringara", "Bhayaanaka", "Beebhatsa", "Veera"],
            "Raudra": ["Veera", "Bhayaanaka", "Beebhatsa"],
            "Veera": ["Raudra", "Haasya", "Adbutham", "Sringara", "Karuna"],
            "Bhayaanaka": ["Raudra", "Karuna", "Beebhatsa"],
            "Beebhatsa": ["Bhayaanaka", "Raudra", "Karuna"],
            "Adbutham": ["Sringara", "Veera", "Haasya", "Saantha"],
            "Saantha": ["Karuna", "Sringara", "Adbutham", "Haasya"]
        }
        
        # Define energy levels for DJ transitions (1-10 scale)
        self.energy_levels = {
            "Sringara": 7,
            "Haasya": 8,
            "Karuna": 3,
            "Raudra": 9,
            "Veera": 10,  # Highest energy
            "Bhayaanaka": 6,
            "Beebhatsa": 5,
            "Adbutham": 7,
            "Saantha": 1   # Lowest energy
        }
        
        # Define corresponding Western musical qualities
        # This helps bridge the gap between Indian and Western music
        self.western_correlations = {
            "Sringara": ["Major", "Lydian", "major 7th chords"],
            "Haasya": ["Major pentatonic", "Mixolydian", "dominant 7th chords"],
            "Karuna": ["Minor", "Phrygian", "minor 7th chords"],
            "Raudra": ["Diminished", "Locrian", "diminished chords"],
            "Veera": ["Major", "Lydian dominant", "sus4 chords"],
            "Bhayaanaka": ["Half-diminished", "Locrian", "minor 7♭5 chords"],
            "Beebhatsa": ["Altered dominant", "Phrygian dominant", "altered chords"],
            "Adbutham": ["Augmented", "Whole tone", "augmented chords"],
            "Saantha": ["Natural minor", "Dorian", "minor 9th chords"]
        }
        
        # Mapping of ragas to their Thaat classification
        # This helps in finding Western equivalents
        self.raga_thaats = {
            "Yaman": "Kalyan",
            "Bhairav": "Bhairav",
            "Bhairavi": "Bhairavi",
            "Todi": "Todi",
            "Bilawal": "Bilawal",
            "Kafi": "Kafi",
            "Asavari": "Asavari",
            "Marwa": "Marwa",
            "Purvi": "Purvi",
            "Desh": "Khamaj",
            "Malkauns": "Bhairavi",
            "Darbari": "Asavari",
            "Bageshri": "Kafi",
            "Durga": "Bilawal",
            "Jaunpuri": "Asavari",
            "Bhimpalasi": "Kafi",
            "Ahir Bhairav": "Bhairav",
            "Pahadi": "Bilawal",
            "Jog": "Kafi",
            "Kedar": "Kalyan",
            "Hameer": "Kalyan",
            "Chandrakauns": "Bhairavi",
            "Miyan Ki Malhar": "Kafi",
            "Tilak Kamod": "Khamaj",
            "Shree": "Purvi",
            "Bairagi": "Bhairav",
            "Nat Kamod": "Khamaj",
            "Hindol": "Kalyan",
            "Jaijaiwanti": "Khamaj",
            "Lalit": "Marwa",
            "Bahar": "Kafi",
            "Gauri": "Bhairav",
            "Vibhas": "Bhairav",
            "Maand": "Bilawal",
            "Vrindavani Sarang": "Kafi",
            "Gaud Sarang": "Bilawal",
            "Jogiya": "Bhairav",
            "Komal Rishabh Asavari": "Asavari",
            "Bilaskhani Todi": "Todi",
            "Champakali": "Khamaj",
            "Madhuvanti": "Todi"
        }
        
        # Mapping of Thaats to Western scale equivalents
        self.thaat_western_map = {
            "Bilawal": "Major",
            "Khamaj": "Mixolydian",
            "Kafi": "Dorian",
            "Asavari": "Natural Minor",
            "Bhairavi": "Phrygian",
            "Bhairav": "Double Harmonic Major",
            "Kalyan": "Lydian",
            "Marwa": "Marwa (no Western equivalent)",
            "Purvi": "Purvi (no Western equivalent)",
            "Todi": "Todi (no Western equivalent)"
        }
    
    def get_rasa_info(self, rasa):
        """
        Get information about a specific rasa.
        
        Args:
            rasa (str): The name of the rasa
            
        Returns:
            dict: Information about the rasa
            
        Examples:
            >>> nw = NavarasaMap()
            >>> info = nw.get_rasa_info("Sringara")
            >>> info["english"]
            'Love/Erotic'
        """
        if rasa not in self.rasas:
            raise ValueError(f"Unknown rasa: {rasa}. Available rasas: {', '.join(self.rasas.keys())}")
        
        return self.rasas[rasa]
    
    def get_raga_by_rasa(self, rasa):
        """
        Get a list of ragas associated with a particular rasa/sentiment.
        
        Args:
            rasa (str): The name of the rasa
            
        Returns:
            list: List of ragas associated with the rasa
            
        Examples:
            >>> nw = NavarasaMap()
            >>> ragas = nw.get_raga_by_rasa("Sringara")
            >>> "Yaman" in ragas
            True
        """
        if rasa not in self.rasa_ragas:
            raise ValueError(f"Unknown rasa: {rasa}. Available rasas: {', '.join(self.rasa_ragas.keys())}")
        
        return self.rasa_ragas[rasa]
    
    def get_rasa_from_raga(self, raga):
        """
        Find which rasa(s) a particular raga is associated with.
        
        Args:
            raga (str): The name of the raga
            
        Returns:
            list: List of rasas associated with the raga
            
        Examples:
            >>> nw = NavarasaMap()
            >>> rasas = nw.get_rasa_from_raga("Bhairav")
            >>> "Raudra" in rasas
            True
        """
        matching_rasas = []
        for rasa, ragas in self.rasa_ragas.items():
            if raga in ragas:
                matching_rasas.append(rasa)
        
        return matching_rasas
    
    def get_raga_frequencies(self, raga_name):
        """
        Get the frequencies for a specific raga.
        
        Args:
            raga_name (str): The name of the raga
            
        Returns:
            dict: Dictionary mapping swara names to frequencies
            
        Examples:
            >>> nw = NavarasaMap(220.0)
            >>> freqs = nw.get_raga_frequencies("Yaman")
            >>> len(freqs)
            7
        """
        return self.indian.calculate_raga_frequencies(raga_name)
    
    def get_compatible_rasas(self, rasa):
        """
        Find compatible transitions from one emotional state to another.
        
        Args:
            rasa (str): The starting rasa
            
        Returns:
            dict: Dictionary of target rasas with transition information
            
        Examples:
            >>> nw = NavarasaMap()
            >>> transitions = nw.get_compatible_rasas("Sringara")
            >>> "Haasya" in transitions
            True
        """
        if rasa not in self.compatible_transitions:
            raise ValueError(f"Unknown rasa: {rasa}. Available rasas: {', '.join(self.compatible_transitions.keys())}")
        
        transitions = {}
        for target_rasa in self.compatible_transitions[rasa]:
            # Determine the transition type based on energy levels
            current_energy = self.energy_levels[rasa]
            target_energy = self.energy_levels[target_rasa]
            
            if target_energy > current_energy:
                transition_type = "Energy boost"
            elif target_energy < current_energy:
                transition_type = "Energy reduction"
            else:
                transition_type = "Energy maintenance"
            
            # Calculate energy difference percentage
            energy_diff = abs(((target_energy - current_energy) / current_energy) * 100)
            
            transitions[target_rasa] = {
                "transition_type": transition_type,
                "energy_difference": f"{energy_diff:.1f}%",
                "energy_level": target_energy,
                "description": self.rasas[target_rasa]["english"],
                "recommended_ragas": self.rasa_ragas[target_rasa]
            }
        
        return transitions
    
    def suggest_transition_path(self, start_rasa, end_rasa, max_steps=3):
        """
        Suggest a transition path from one rasa to another.
        
        Args:
            start_rasa (str): The starting rasa
            end_rasa (str): The target rasa
            max_steps (int): Maximum number of transitions allowed
            
        Returns:
            list: List of rasas forming the transition path, or None if no path found
            
        Examples:
            >>> nw = NavarasaMap()
            >>> path = nw.suggest_transition_path("Karuna", "Veera")
            >>> len(path) > 0
            True
        """
        if start_rasa not in self.compatible_transitions:
            raise ValueError(f"Unknown starting rasa: {start_rasa}")
            
        if end_rasa not in self.rasas:
            raise ValueError(f"Unknown ending rasa: {end_rasa}")
            
        if start_rasa == end_rasa:
            return [start_rasa]
        
        # Simple BFS to find shortest path
        visited = {start_rasa}
        queue = [[start_rasa]]
        
        while queue:
            path = queue.pop(0)
            current = path[-1]
            
            if current == end_rasa:
                return path
            
            if len(path) >= max_steps:
                continue
            
            for next_rasa in self.compatible_transitions[current]:
                if next_rasa not in visited:
                    visited.add(next_rasa)
                    queue.append(path + [next_rasa])
        
        return None  # No path found within max_steps
    
    def get_raga_thaat(self, raga_name):
        """
        Get the thaat (parent scale) of a raga.
        
        Args:
            raga_name (str): The name of the raga
            
        Returns:
            str: The thaat name, or None if not found
            
        Examples:
            >>> nw = NavarasaMap()
            >>> nw.get_raga_thaat("Yaman")
            'Kalyan'
        """
        return self.raga_thaats.get(raga_name)
    
    def get_western_equivalent(self, raga_name):
        """
        Find Western scales that approximate the given raga.
        
        Args:
            raga_name (str): The name of the raga
            
        Returns:
            dict: Information about Western equivalents
            
        Examples:
            >>> nw = NavarasaMap()
            >>> equiv = nw.get_western_equivalent("Yaman")
            >>> equiv["scale_type"]
            'Lydian'
        """
        # Get the thaat for this raga
        thaat = self.get_raga_thaat(raga_name)
        if not thaat:
            return {"message": f"No thaat information available for {raga_name}"}
        
        # Get Western equivalent for this thaat
        western_scale = self.thaat_western_map.get(thaat)
        if not western_scale:
            return {"message": f"No Western equivalent for thaat {thaat}"}
        
        # Get rasas associated with this raga
        rasas = self.get_rasa_from_raga(raga_name)
        
        # Combine with Western correlations
        western_qualities = []
        for rasa in rasas:
            western_qualities.extend(self.western_correlations.get(rasa, []))
        
        # De-duplicate
        western_qualities = list(set(western_qualities))
        
        # Create a WesternMusic instance to get Camelot notation
        wm = WesternMusic()
        
        # Map thaats to suggested Western keys
        thaat_to_key_map = {
            "Bilawal": "C",        # Major scale
            "Khamaj": "G",         # Mixolydian
            "Kafi": "D",           # Dorian
            "Asavari": "A",        # Natural Minor
            "Bhairavi": "E",       # Phrygian
            "Bhairav": "C",        # Double Harmonic Major
            "Kalyan": "F",         # Lydian
            "Marwa": "C",          # No direct equivalent
            "Purvi": "C",          # No direct equivalent
            "Todi": "D"            # No direct equivalent
        }
        
        # Get suggested Western key
        key = thaat_to_key_map.get(thaat, "C")
        
        # Determine scale type for Camelot notation
        camelot_scale_type = "major"
        if western_scale in ["Natural Minor", "Phrygian", "Dorian"]:
            camelot_scale_type = "minor"
        
        # Get Camelot notation
        camelot_notation = wm.get_camelot_notation(key, camelot_scale_type)
        
        # Get compatible Camelot keys
        compatible_keys = {}
        if camelot_notation:
            compatible_keys = wm.get_compatible_keys(camelot_notation)
        
        return {
            "raga": raga_name,
            "thaat": thaat,
            "scale_type": western_scale,
            "suggested_key": key,
            "camelot_notation": camelot_notation,
            "compatible_camelot_keys": compatible_keys,
            "rasas": rasas,
            "western_correlations": western_qualities
        }
    
    def compare_raga_to_western_scale(self, raga_name, western_root="C", octave=4):
        """
        Compare a raga's frequencies to a corresponding Western scale.
        
        Args:
            raga_name (str): The name of the raga
            western_root (str): Root note for Western scale
            octave (int): Octave number for Western scale
            
        Returns:
            dict: Comparison information
            
        Examples:
            >>> nw = NavarasaMap()
            >>> comparison = nw.compare_raga_to_western_scale("Yaman")
            >>> "raga_frequencies" in comparison
            True
        """
        # Get the Western equivalent information
        equiv = self.get_western_equivalent(raga_name)
        
        # Get the raga frequencies
        raga_freqs = self.get_raga_frequencies(raga_name)
        
        # Initialize WesternMusic
        wm = WesternMusic()
        
        # Determine the scale type to use
        scale_type = "major"  # Default
        if equiv["scale_type"] == "Natural Minor":
            scale_type = "minor"
        elif equiv["scale_type"] == "Lydian":
            scale_type = "major"  # Will need adjustments for the raised 4th
        elif equiv["scale_type"] == "Dorian" or equiv["scale_type"] == "Mixolydian":
            scale_type = "major"  # Will need adjustments
        
        # Get Western scale frequencies
        western_freqs = wm.get_scale(western_root, octave, scale_type)
        
        # Handle Lydian (raised 4th)
        if equiv["scale_type"] == "Lydian":
            # Find the 4th note
            for note in western_freqs:
                if note[0] == 'F':
                    # Get the next semitone up
                    if 'F#' + note[1:] not in western_freqs:
                        western_freqs['F#' + note[1:]] = wm.get_frequency('F#', int(note[1:]))
                    # Remove the natural 4th
                    western_freqs.pop(note)
                    break
        
        # Handle Mixolydian (lowered 7th)
        if equiv["scale_type"] == "Mixolydian":
            # Find the 7th note (leading tone)
            for note in list(western_freqs.keys()):  # Use list() to avoid runtime modification issues
                if note[0] == 'B':
                    # Replace with B-flat
                    western_freqs.pop(note)
                    western_freqs['Bb' + note[1:]] = wm.get_frequency('Bb', int(note[1:]))
                    break
        
        # Handle Dorian (raised 6th compared to minor)
        if equiv["scale_type"] == "Dorian":
            # Start with a minor scale
            western_freqs = wm.get_scale(western_root, octave, "minor")
            # Find the 6th note and raise it
            for note in list(western_freqs.keys()):
                if note[0] == 'A':
                    # Replace with A-natural (in a C minor scale the 6th would be Ab)
                    western_freqs.pop(note)
                    western_freqs['A' + note[1:]] = wm.get_frequency('A', int(note[1:]))
                    break
        
        # Get Camelot notation for the Western scale
        camelot_scale_type = "major"
        if equiv["scale_type"] in ["Natural Minor", "Phrygian", "Dorian"]:
            camelot_scale_type = "minor"
        
        camelot_notation = wm.get_camelot_notation(western_root, camelot_scale_type)
        
        # Get compatible Camelot keys
        compatible_keys = {}
        if camelot_notation:
            compatible_keys = wm.get_compatible_keys(camelot_notation)
        
        return {
            "raga": raga_name,
            "western_scale": f"{western_root} {equiv['scale_type']}",
            "thaat": equiv["thaat"],
            "camelot_notation": camelot_notation,
            "compatible_camelot_keys": compatible_keys,
            "raga_frequencies": raga_freqs,
            "western_frequencies": western_freqs,
            "rasas": equiv["rasas"]
        }