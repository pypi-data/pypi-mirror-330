"""
This module provides the error classes for BIDS.
"""


class BIDSError(Exception):
    """
    Base class for all BIDS-related exceptions.

    This class serves as the base exception class for all exceptions related to BIDS (Brain
    Imaging Data Structure) specifications and operations.
    """


class OnsetError(BIDSError):
    """Exception raised when onset value is incorrect.

    This exception is raised when the provided onset value does not meet the expected criteria
    for correctness according to BIDS (Brain Imaging Data Structure) specifications.
    """

    def __init__(
        self, onset: object, msg: str = "Property 'onset' MUST be a number"
    ) -> None:
        """Initialize the OnsetError instance.

        Parameters
        ----------
        onset : object
            The onset value that caused the error.
        msg : str, optional
            Explanation of the error.
        """
        self.onset = onset
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self) -> str:
        """Return a string representation of the error.

        Returns
        -------
        str
            A string containing the onset value and the error message.
        """
        return f"{self.onset} -> {self.msg}"


class DurationError(BIDSError):
    """Exception raised when duration value is incorrect.

    This exception is raised when the provided duration value does not meet the expected criteria
    for correctness according to BIDS (Brain Imaging Data Structure) specifications.
    """

    def __init__(
        self,
        duration: object,
        msg: str = "Property 'duration' MUST be either zero or positive (or n/a if unavailable)",
    ) -> None:
        """Initialize the DurationError instance.

        Parameters
        ----------
        duration : object
            The duration value that caused the error.
        msg : str, optional
            Explanation of the error.
        """
        self.duration = duration
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self) -> str:
        """Return a string representation of the error.

        Returns
        -------
        str
            A string containing the duration value and the error message.
        """
        return f"{self.duration} -> {self.msg}"


class TrialTypeError(BIDSError):
    """Exception raised when trial_type value is incorrect.

    This exception is raised when the provided trial_type value does not meet the expected criteria
    for correctness according to BIDS (Brain Imaging Data Structure) specifications.
    """

    def __init__(
        self, trial_type: object, msg: str = "Property 'trial_type' MUST be a string"
    ) -> None:
        """Initialize the TrialTypeError instance.

        Parameters
        ----------
        trial_type : object
            The trial_type value that caused the error.
        msg : str, optional
            Explanation of the error.
        """
        self.trial_type = trial_type
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self) -> str:
        """Return a string representation of the error.

        Returns
        -------
        str
            A string containing the trial_type value and the error message.
        """
        return f"{self.trial_type} -> {self.msg}"


class SampleError(BIDSError):
    """Exception raised when sample value is incorrect.

    This exception is raised when the provided sample value does not meet the expected criteria
    for correctness according to BIDS (Brain Imaging Data Structure) specifications.
    """

    def __init__(
        self, sample: object, msg: str = "Property 'sample' MUST be an integer"
    ) -> None:
        """Initialize the SampleError instance.

        Parameters
        ----------
        sample : object
            The sample value that caused the error.
        msg : str, optional
            Explanation of the error.
        """
        self.sample = sample
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self) -> str:
        """Return a string representation of the error.

        Returns
        -------
        str
            A string containing the sample value and the error message.
        """
        return f"{self.sample} -> {self.msg}"


class ResponseTimeError(BIDSError):
    """Exception raised when response_time value is incorrect.

    This exception is raised when the provided response_time value does not meet the expected
    criteria for correctness according to BIDS (Brain Imaging Data Structure) specifications.
    """

    def __init__(
        self,
        response_time: object,
        msg: str = "Property 'response_time' MUST be a number (or n/a if unavailable)",
    ) -> None:
        """Initialize the ResponseTimeError instance.

        Parameters
        ----------
        response_time : object
            The response_time value that caused the error.
        msg : str, optional
            Explanation of the error.
        """
        self.response_time = response_time
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self) -> str:
        """Return a string representation of the error.

        Returns
        -------
        str
            A string containing the response_time value and the error message.
        """
        return f"{self.response_time} -> {self.msg}"


class HedError(BIDSError):
    """Exception raised when hed value is incorrect.

    This exception is raised when the provided hed value does not meet the expected criteria
    for correctness according to BIDS (Brain Imaging Data Structure) specifications.
    """

    def __init__(
        self, hed: object, msg: str = "Property 'hed' MUST be a string"
    ) -> None:
        """Initialize the HEDError instance.

        Parameters
        ----------
        hed : object
            The hed value that caused the error.
        msg : str, optional
            Explanation of the error.
        """
        self.hed = hed
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self) -> str:
        """Return a string representation of the error.

        Returns
        -------
        str
            A string containing the hed value and the error message.
        """
        return f"{self.hed} -> {self.msg}"


class StimFileError(BIDSError):
    """Exception raised when stim_file value is incorrect.

    This exception is raised when the provided stim_file value does not meet the expected criteria
    for correctness according to BIDS (Brain Imaging Data Structure) specifications.
    """

    def __init__(
        self, stim_file: object, msg: str = "Property 'stim_file' MUST be a string"
    ) -> None:
        """Initialize the StimFileError instance.

        Parameters
        ----------
        stim_file : object
            The stim_file value that caused the error.
        msg : str, optional
            Explanation of the error.
        """
        self.stim_file = stim_file
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self) -> str:
        """Return a string representation of the error.

        Returns
        -------
        str
            A string containing the stim_file value and the error message.
        """
        return f"{self.stim_file} -> {self.msg}"


class IdentifierError(BIDSError):
    """Exception raised when identifier value is incorrect.

    This exception is raised when the provided identifier value does not meet the expected criteria
    for correctness according to BIDS (Brain Imaging Data Structure) specifications.
    """

    def __init__(
        self, identifier: object, msg: str = "Property 'identifier' MUST be a string"
    ) -> None:
        """Initialize the IdentifierError instance.

        Parameters
        ----------
        identifier : object
            The identifier value that caused the error.
        msg : str, optional
            Explanation of the error.
        """
        self.identifier = identifier
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self) -> str:
        """Return a string representation of the error.

        Returns
        -------
        str
            A string containing the identifier value and the error message.
        """
        return f"{self.identifier} -> {self.msg}"


class DatabaseError(BIDSError):
    """Exception raised when database value is incorrect.

    This exception is raised when the provided database value does not meet the expected criteria
    for correctness according to BIDS (Brain Imaging Data Structure) specifications.
    """

    def __init__(
        self, database: object, msg: str = "Property 'database' MUST be a string"
    ) -> None:
        """Initialize the DatabaseError instance.

        Parameters
        ----------
        database : object
            The database value that caused the error.
        msg : str, optional
            Explanation of the error.
        """
        self.database = database
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self) -> str:
        """Return a string representation of the error.

        Returns
        -------
        str
            A string containing the database value and the error message.
        """
        return f"{self.database} -> {self.msg}"
