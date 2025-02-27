"""
Main entry point for reporting module.
"""

from pyutile.reporting.logged import logger
from pyutile.reporting.errors import PyUtilReportingError
class Reporter:  # TODO: expand from the generated base
    """
    A class used to report messages.

    Attributes
    ----------
    logger : logger
        The logger object used to log messages.
    """
    def __init__(self):
        self._logger = logger

    def report(self, message):
        """
        Log a message.

        Parameters
        ----------
        message : str
            The message to be logged.
        """
        self._logger.info(message)

    def get_reporter(self, reporter: str = 'logger'):
        """
        Get a reporter object.

        Parameters
        ----------
        reporter : str
            The name of the reporter object to get.

        Returns
        -------
        logger
            The logger object.
        """
        if reporter == 'logger':
            return self._logger
        else:
            raise PyUtilReportingError(f"Reporter '{reporter}' not found.")
