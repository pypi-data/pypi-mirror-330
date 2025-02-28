"""
This file combines the two frameworks doctest and pytest to test various aspects of the
BIDSBehEvent class.
"""

import doctest
from psychopy_bids import bids

def test_init():
    """Test case for the __init__ method of BIDSBehEvent"""
    event = bids.BIDSBehEvent(some_attribute=42, another_attribute="abc")
    assert event.some_attribute == 42
    assert event.another_attribute == "abc"

def test_repr():
    """Test case for the __repr__ method of BIDSBehEvent"""
    event = bids.BIDSBehEvent(some_attribute=42, another_attribute="abc")
    expected_repr = "BIDSBehEvent(some_attribute=42, another_attribute=abc)"
    assert repr(event) == expected_repr

def test_doc_strings():
    """Test docstrings using doctest."""
    results = doctest.testmod(bids.bidsbehevent)
    assert results.failed == 0, f"{results.failed} doctests failed out of {results.attempted}."