"""
Configuration file for pytest.
"""

import pytest
from svarascala import WesternMusic, IndianMusic


@pytest.fixture
def western_music_standard():
    """Fixture for standard A440 Western music instance."""
    return WesternMusic(reference_a4=440.0)


@pytest.fixture
def western_music_baroque():
    """Fixture for Baroque tuning (A415) Western music instance."""
    return WesternMusic(reference_a4=415.0)


@pytest.fixture
def western_music_verdi():
    """Fixture for Verdi tuning (A432) Western music instance."""
    return WesternMusic(reference_a4=432.0)


@pytest.fixture
def indian_music_standard():
    """Fixture for standard Sa=220Hz Indian music instance."""
    return IndianMusic(reference_sa=220.0)


@pytest.fixture
def indian_music_high():
    """Fixture for higher Sa=240Hz Indian music instance."""
    return IndianMusic(reference_sa=240.0)


@pytest.fixture
def indian_music_low():
    """Fixture for lower Sa=196Hz Indian music instance."""
    return IndianMusic(reference_sa=196.0)


# Sample test data for parametrized tests
@pytest.fixture
def western_notes_data():
    """Sample Western notes test data."""
    return [
        ('C', 4, 261.63),
        ('A', 4, 440.00),
        ('F#', 4, 369.99),
        ('G', 3, 196.00),
        ('B', 5, 987.77),
    ]


@pytest.fixture
def indian_swaras_data():
    """Sample Indian swaras test data."""
    return [
        ('Sa', 'shuddha', 220.00),
        ('Pa', 'shuddha', 330.00),
        ('Ma', 'shuddha', 293.33),
        ('Re', 'komal', 234.67),
        ('Ni', 'shuddha', 391.11),
    ]


@pytest.fixture
def ragas_data():
    """Sample raga test data."""
    return [
        'Yaman',
        'Bhairav',
        'Bhairavi',
        'Todi',
        'Kafi',
    ]