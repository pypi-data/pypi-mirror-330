"""
TODO: Module docstring for errors.py
"""

from enum import Enum


class ErrorCategories(Enum):
    pass


class PyForgeException(Exception):
    pass


class PyUtilException(PyForgeException):
    pass


class PyUtilConfError(PyUtilException):
    pass


class PyUtilReportingError(PyUtilException):
    pass


class ExceptionHandler:
    """
    A class used to handle exceptions.
    """

    pass
