# coding=utf-8
"""
Interfaces
"""

from abc import abstractmethod
from typing import Any


# pylint: disable=too-few-public-methods
class IObserver:
    """
    Observer interface.
    Get message and do some work with it.
    """
    @abstractmethod
    def __call__(self, message: Any):
        """
        Listen message
        """
        raise NotImplementedError()


class ISubject:
    """
    Subject iterface.
    Send message.
    """


# pylint: disable=too-few-public-methods
class IMessageAdapter:
    """
    Message adapter interface.
    Get message and return adapted message.
    """
    @abstractmethod
    def __call__(self, message: Any) -> Any:
        raise NotImplementedError()


# pylint: disable=too-few-public-methods
class IErrorHandler:
    """
    Error handler interface.
    Get exception and do some work with it.
    """

    @abstractmethod
    def __call__(self, exc: Exception):
        """
        Handle exception
        """
        raise NotImplementedError()
