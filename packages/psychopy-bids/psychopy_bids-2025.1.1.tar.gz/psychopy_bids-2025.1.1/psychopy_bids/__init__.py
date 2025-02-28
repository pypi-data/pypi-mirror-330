"""
Package to support the creation of valid bids-datasets.
"""

from importlib.metadata import version

__version__ = version("psychopy_bids")

from .bids_event import BidsEventComponent
from .bids_settings import BidsExportRoutine
from .deprecated.bids_beh import BidsBehEventComponent
from .deprecated.bids_task import BidsTaskEventComponent

__all__ = [
    "BidsEventComponent",
    "BidsExportRoutine",
    "BidsBehEventComponent",
    "BidsTaskEventComponent",
]
