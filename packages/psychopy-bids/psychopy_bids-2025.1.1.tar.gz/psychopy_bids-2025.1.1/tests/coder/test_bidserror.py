"""
This file contains unit tests for the BIDS error classes.
"""

import pytest
from psychopy_bids.bids.bidserror import (
    BIDSError,
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

def test_onset_error():
    assert str(OnsetError("A")) == "A -> Property 'onset' MUST be a number"

def test_duration_error():
    msg = "A -> Property 'duration' MUST be either zero or positive (or n/a if unavailable)"
    assert str(DurationError("A")) == msg

def test_trial_type_error():
    assert str(TrialTypeError(1)) == "1 -> Property 'trial_type' MUST be a string"

def test_sample_error():
    assert str(SampleError("A")) == "A -> Property 'sample' MUST be an integer"

def test_response_time_error():
    msg = "A -> Property 'response_time' MUST be a number (or n/a if unavailable)"
    assert str(ResponseTimeError("A")) == msg

def test_hed_error():
    assert str(HedError(1)) == "1 -> Property 'hed' MUST be a string"

def test_stim_file_error():
    assert str(StimFileError("A")) == "A -> Property 'stim_file' MUST be a string"

def test_identifier_error():
    assert str(IdentifierError("A")) == "A -> Property 'identifier' MUST be a string"

def test_database_error():
    assert str(DatabaseError("A")) == "A -> Property 'database' MUST be a string"