"""This module provides the class BIDSBehEvent"""


class BIDSBehEvent(dict):
    """A class that represents events of behavioral experiments.

    This class is used for events that do not include the mandatory onset and duration columns.
    Events are, for example, stimuli presented to the participant or participant responses.

    Examples
    --------
    >>> from psychopy_bids import bids
    >>> event = bids.BIDSBehEvent(trial=1, resp='L')

    Notes
    -----
    For more details on behavioral experiment files, see [BIDS Specification](https://bids-specification.readthedocs.io/en/stable/04-modality-specific-files/07-behavioral-experiments.html).
    """

    def __init__(self, *args: tuple, **kwargs: dict) -> None:
        """Initialize a BIDSBehEvent object.

        Parameters
        ----------
        *args : tuple
            Any arguments that the object's superclass's `__init__` method might require.
        **kwargs : dict
            Any keyword arguments that the object's superclass's `__init__` method might require.
        """
        super().__init__(*args, **kwargs)
        self.__dict__ = self

    # -------------------------------------------------------------------------------------------- #

    def __repr__(self) -> str:
        """Return a printable representational string of the given object.

        This method returns a string representation of the BIDSBehEvent object containing its
        attribute-value pairs.

        Returns:
        -------
        str
            A string representation of the BIDSBehEvent object.
        """
        items = [f"{key}={value}" for key, value in self.items() if value is not None]
        return f"BIDSBehEvent({', '.join(items)})" if items else "BIDSBehEvent()"
