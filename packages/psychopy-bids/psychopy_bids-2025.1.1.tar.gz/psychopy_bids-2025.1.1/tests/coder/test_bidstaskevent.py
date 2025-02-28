"""
This file combines the two frameworks doctest and pytest to test various aspects of the
BIDSTaskEvent class.
"""

import doctest
import pytest
from psychopy_bids import bids
from psychopy_bids.bids.bidserror import (
    DatabaseError,
    DurationError,
    HedError,
    IdentifierError,
    OnsetError,
    ResponseTimeError,
    SampleError,
    StimFileError,
    TrialTypeError,
)
from psychopy_bids.bids.bidstaskevent import BIDSTaskEvent

def test_init():
    with pytest.raises(TypeError):
        BIDSTaskEvent()
        BIDSTaskEvent(onset=1.0)
        BIDSTaskEvent(duration=0)

def test_custom_column():
    custom = BIDSTaskEvent(onset=1.0, duration=0, trial=1)
    assert custom.trial == 1

def test_repr():
    assert repr(BIDSTaskEvent(onset=1.0, duration=0)) == "BIDSTaskEvent(onset=1.0, duration=0)"

def test_set_item():
    event = BIDSTaskEvent(0, 0, trial_type="begin")
    event.onset = 2.5
    assert event.onset == 2.5
    event.duration = "n/a"
    assert event.duration == "n/a"
    event.trial_type = "start"
    assert event.trial_type == "start"
    event.sample = 1
    assert event.sample == 1
    event.response_time = 1
    assert event.response_time == 1
    event.value = "value"
    assert event.value == "value"
    event.hed = "hed"
    assert event.hed == "hed"
    event.stim_file = "stim_file"
    assert event.stim_file == "stim_file"
    event.identifier = "identifier"
    assert event.identifier == "identifier"
    event.database = "database"
    assert event.database == "database"
    event.trial = 1
    assert event.trial == 1

def test_onset():
    event = BIDSTaskEvent(onset=1.0, duration=0)
    assert isinstance(event.onset, (int, float))
    event = BIDSTaskEvent(onset="1", duration=0)
    assert isinstance(event.onset, (int, float))

    with pytest.raises(OnsetError):
        BIDSTaskEvent(onset=[0, 1, 2], duration=0)

    with pytest.raises(OnsetError):
        BIDSTaskEvent(onset="A", duration=0)

def test_duration():
    event = BIDSTaskEvent(onset=1.0, duration=0)
    assert isinstance(event.onset, (int, float))
    assert event.duration >= 0

    with pytest.raises(DurationError):
        BIDSTaskEvent(onset=1.0, duration="A")

    with pytest.raises(DurationError):
        BIDSTaskEvent(onset=1.0, duration=-1)

    event = BIDSTaskEvent(onset=1.0, duration="1")
    assert event.duration == 1

    event = BIDSTaskEvent(onset=1.0, duration="n/a")
    assert event.duration == "n/a"

def test_trial_type():
    event = BIDSTaskEvent(onset=1.0, duration=0, trial_type="go")
    assert isinstance(event.trial_type, str)

    with pytest.raises(TrialTypeError):
        BIDSTaskEvent(onset=1.0, duration=0, trial_type=1)

def test_value():
    event = BIDSTaskEvent(onset=1.0, duration=0, value=0)
    assert event.value == 0

def test_sample():
    event = BIDSTaskEvent(onset=1.0, duration=0, sample=1)
    assert isinstance(event.sample, (int, float))

    event = BIDSTaskEvent(onset=1.0, duration=0, sample="1")
    assert isinstance(event.sample, (int, float))

    with pytest.raises(SampleError):
        BIDSTaskEvent(onset=1.0, duration=0, sample="A1")

def test_response_time():
    event = BIDSTaskEvent(onset=1.0, duration=0, response_time=1.0)
    assert isinstance(event.response_time, (int, float))
    assert event.response_time >= 0

    with pytest.raises(ResponseTimeError):
        BIDSTaskEvent(onset=1.0, duration=0, response_time="A")

    with pytest.raises(ResponseTimeError):
        BIDSTaskEvent(onset=1.0, duration=0, response_time=[0, 1, 2])

    event = BIDSTaskEvent(onset=1.0, duration=0, response_time="1")
    assert event.response_time == 1

    event = BIDSTaskEvent(onset=1.0, duration=0, response_time="n/a")
    assert event.response_time == "n/a"

def test_hed():
    event = BIDSTaskEvent(onset=1.0, duration=0, hed="go")
    assert isinstance(event.hed, str)

    with pytest.raises(HedError):
        BIDSTaskEvent(onset=1.0, duration=0, hed=1)

def test_stim_file():
    event = BIDSTaskEvent(onset=1.0, duration=0, stim_file="file.txt")
    assert isinstance(event.stim_file, str)

    with pytest.raises(StimFileError):
        BIDSTaskEvent(onset=1.0, duration=0, stim_file=1)

def test_identifier():
    event = BIDSTaskEvent(onset=1.0, duration=0, identifier="a")
    assert isinstance(event.identifier, str)

    with pytest.raises(IdentifierError):
        BIDSTaskEvent(onset=1.0, duration=0, identifier=1)

def test_database():
    event = BIDSTaskEvent(onset=1.0, duration=0, database="a")
    assert isinstance(event.database, str)

    with pytest.raises(DatabaseError):
        BIDSTaskEvent(onset=1.0, duration=0, database=1)

def test_doc_strings():
    """Test docstrings using doctest."""
    results = doctest.testmod(bids.bidstaskevent)
    assert results.failed == 0, f"{results.failed} doctests failed out of {results.attempted}."