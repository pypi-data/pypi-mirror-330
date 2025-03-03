"""
Indian classical music frequency calculations for the SvaraScala library.

"तत्र स्वराः -
षड्‍जश्‍च ऋषभश्‍चैव गान्धारो मध्यमस्तथा ।
पञ्‍चमो धैवतश्‍चैव सप्तमोऽथ निषादवान् ॥ २१॥"
— Natya Shastra, 28.21

"There, the notes are:
Shadja and Rishabha, as well as Gandhara and similarly Madhyama,
Panchama and Dhaivata, and the seventh, which is Nishada."
— Natya Shastra, 28.21

"""

class IndianMusic:
    """
    Class to handle frequency calculations for Indian classical music.
    """
    def __init__(self, reference_sa=220.0):
        """
        Initialize with a reference frequency for Sa (defaults to 220 Hz).
        
        Args:
            reference_sa (float): Reference frequency for Sa in Hz. Default is 220.0 Hz.
        """
        self.reference_sa = reference_sa
        
        # Initialize shruti ratios based on traditional just intonation
        self.shruti_ratios = {
            1: 1,       # Sa (Shadja)
            2: 256/243, # Komal Re (Suddha Rishabha)
            3: 16/15,   # Re (Chyuta Rishabha)
            4: 10/9,    # Shuddha Re (Tivra Rishabha)
            5: 9/8,     # Tivra Re (Tivratara Rishabha)
            6: 32/27,   # Komal Ga (Suddha Gandhara)
            7: 6/5,     # Ga (Chyuta Gandhara)
            8: 5/4,     # Shuddha Ga (Antara Gandhara)
            9: 81/64,   # Tivra Ga (Tivra Gandhara)
            10: 4/3,    # Ma (Suddha Madhyama)
            11: 27/20,  # Tivra Ma (Tivra Madhyama)
            12: 45/32,  # Tivratar Ma (Prati Madhyama)
            13: 729/512,# Ati-Tivra Ma
            14: 3/2,    # Pa (Panchama)
            15: 128/81, # Komal Dha (Suddha Dhaivata)
            16: 8/5,    # Dha (Chyuta Dhaivata)
            17: 5/3,    # Shuddha Dha (Antara Dhaivata)
            18: 27/16,  # Tivra Dha (Tivra Dhaivata)
            19: 16/9,   # Komal Ni (Suddha Nishada)
            20: 9/5,    # Ni (Chyuta Nishada)
            21: 15/8,   # Shuddha Ni (Kakali Nishada)
            22: 243/128 # Tivra Ni (Tivra Nishada)
        }
        
        # Mapping of swaras to their shruti numbers
        self.swara_to_shruti = {
            "Sa": 1,
            "Re": {
                "komal": 3,   # Some traditions use 2
                "shuddha": 5  # Some traditions use 4
            },
            "Ga": {
                "komal": 6,
                "shuddha": 8  # Some traditions use 9
            },
            "Ma": {
                "shuddha": 10,
                "tivra": 13   # Some traditions use 11 or 12
            },
            "Pa": 14,
            "Dha": {
                "komal": 16,  # Some traditions use 15
                "shuddha": 17 # Some traditions use 18
            },
            "Ni": {
                "komal": 19,
                "shuddha": 21 # Some traditions use 20
            }
        }
        
        # Define common ragas
        self.ragas = {
            "Bhairav": [
                ("Sa", "shuddha"),
                ("Re", "komal"),
                ("Ga", "shuddha"),
                ("Ma", "shuddha"),
                ("Pa", "shuddha"),
                ("Dha", "komal"),
                ("Ni", "shuddha")
            ],
            "Yaman": [
                ("Sa", "shuddha"),
                ("Re", "shuddha"),
                ("Ga", "shuddha"),
                ("Ma", "tivra"),
                ("Pa", "shuddha"),
                ("Dha", "shuddha"),
                ("Ni", "shuddha")
            ],
            "Bhairavi": [
                ("Sa", "shuddha"),
                ("Re", "komal"),
                ("Ga", "komal"),
                ("Ma", "shuddha"),
                ("Pa", "shuddha"),
                ("Dha", "komal"),
                ("Ni", "komal")
            ],
            "Todi": [
                ("Sa", "shuddha"),
                ("Re", "komal"),
                ("Ga", "komal"),
                ("Ma", "tivra"),
                ("Pa", "shuddha"),
                ("Dha", "komal"),
                ("Ni", "komal")
            ],
            "Kafi": [
                ("Sa", "shuddha"),
                ("Re", "shuddha"),
                ("Ga", "komal"),
                ("Ma", "shuddha"),
                ("Pa", "shuddha"),
                ("Dha", "shuddha"),
                ("Ni", "komal")
            ]
        }
    
    def get_shruti_frequency(self, shruti_number):
        """
        Calculate frequency for a specific shruti based on reference Sa.
        
        Args:
            shruti_number: Integer from 1 to 22 representing the shruti
        
        Returns:
            float: Frequency in Hz
        
        Examples:
            >>> im = IndianMusic(220.0)
            >>> round(im.get_shruti_frequency(1), 1)  # Sa
            220.0
            >>> round(im.get_shruti_frequency(14), 1)  # Pa
            330.0
        """
        if shruti_number < 1 or shruti_number > 22:
            raise ValueError("Shruti number must be between 1 and 22")
        
        ratio = self.shruti_ratios[shruti_number]
        return self.reference_sa * ratio
    
    def get_swara_frequency(self, swara, variant="shuddha"):
        """
        Calculate frequency for a specific swara with variant.
        
        Args:
            swara: One of 'Sa', 'Re', 'Ga', 'Ma', 'Pa', 'Dha', 'Ni'
            variant: 'komal', 'shuddha', or 'tivra' (as applicable)
        
        Returns:
            float: Frequency in Hz
        
        Examples:
            >>> im = IndianMusic(220.0)
            >>> round(im.get_swara_frequency("Sa"), 1)
            220.0
            >>> round(im.get_swara_frequency("Pa"), 1)
            330.0
            >>> round(im.get_swara_frequency("Ga", "shuddha"), 1)
            275.0
        """
        if swara == "Sa" or swara == "Pa":
            shruti_num = self.swara_to_shruti[swara]
        else:
            if variant not in self.swara_to_shruti[swara]:
                available_variants = ", ".join(self.swara_to_shruti[swara].keys())
                raise ValueError(f"Invalid variant '{variant}' for {swara}. Available: {available_variants}")
            
            shruti_num = self.swara_to_shruti[swara][variant]
        
        return self.get_shruti_frequency(shruti_num)
    
    def get_raga(self, raga_name):
        """
        Get the swara specification for a named raga.
        
        Args:
            raga_name: Name of the raga
        
        Returns:
            list: List of tuples (swara, variant)
        
        Examples:
            >>> im = IndianMusic()
            >>> raga = im.get_raga("Yaman")
            >>> len(raga)
            7
            >>> raga[0]
            ('Sa', 'shuddha')
        """
        if raga_name not in self.ragas:
            raise ValueError(f"Unknown raga: {raga_name}. Available ragas: {', '.join(self.ragas.keys())}")
        
        return self.ragas[raga_name]
    
    def calculate_raga_frequencies(self, raga_name):
        """
        Calculate frequencies for all notes in a raga.
        
        Args:
            raga_name: Name of the raga
        
        Returns:
            dict: Dictionary mapping swara names to frequencies
        
        Examples:
            >>> im = IndianMusic(220.0)
            >>> freqs = im.calculate_raga_frequencies("Yaman")
            >>> len(freqs)
            7
            >>> 'Sa shuddha' in freqs
            True
        """
        swara_specification = self.get_raga(raga_name)
        frequencies = {}
        
        for swara, variant in swara_specification:
            if swara == "Sa" or swara == "Pa":
                variant = "shuddha"  # Sa and Pa don't have variants
                
            freq = self.get_swara_frequency(swara, variant)
            frequencies[f"{swara} {variant}"] = freq
        
        return frequencies
    
    def get_all_shrutis(self):
        """
        Get frequencies for all 22 shrutis.
        
        Returns:
            dict: Dictionary mapping shruti names to frequencies
        
        Examples:
            >>> im = IndianMusic(220.0)
            >>> shrutis = im.get_all_shrutis()
            >>> len(shrutis)
            22
        """
        frequencies = {}
        for i in range(1, 23):
            freq = self.get_shruti_frequency(i)
            frequencies[f"Shruti {i}"] = freq
        return frequencies
    
'''
यानीमानि प्रयुक्तानि मया शास्त्राणि भूतले।
नाट्यवेदादुपादाय तानि रक्षतु केशवः॥
संसारसागरोत्तारे सर्वे भवन्तु नामिनः।
नाट्यशास्त्रमिदं येन प्रणीतं शंकरः स्वयम्॥
यस्मै यस्मै यदा दद्यादेतच्छास्त्रं द्विजोत्तमाः।
तस्मै तस्मै तदा देया मद्भक्तिः सत्त्वसंश्रया॥
पठनाच्छ्रवणाच्चापि धारणाच्छिक्षणादपि।
नाट्यवेदस्य विप्रेन्द्राः सर्वपापैः प्रमुच्यते॥

May Keshava (Vishnu) protect these teachings that I have presented on earth,
Having derived them from the Natya Veda (the knowledge of dramatic arts).
May all those who are on the path of worldly existence cross the ocean of samsara.
This Natya Shastra was composed by Shankara (Shiva) himself.

O best among the twice-born, to whomever and whenever this knowledge is given,
To them at that time should also be given my devotion that rests in goodness.
Through recitation, listening, retention, and instruction
Of the Natya Veda, O foremost among the wise, one is liberated from all sins.
'''