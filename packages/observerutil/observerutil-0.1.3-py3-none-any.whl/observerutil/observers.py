# coding=utf-8
"""
Observers
"""

from typing import Any, Callable, Optional, Iterable

from .interfaces import (
    IObserver,
    IMessageAdapter,
    IErrorHandler,
)


# pylint: disable=too-few-public-methods
class Observer(IObserver):
    """
    Observer that can get message and do some work and handle errors.
    """
    def __init__(
        self,
        func: Callable,
        error_handler: Optional[IErrorHandler] = None,
    ):
        self.func = func
        self.error_handler = error_handler

    def __call__(self, message: Any):
        """
        Listen message.
        Catch errors by error_handler (if provided)
        """
        try:
            self.func(message)
        except Exception as exc:  # pylint: disable=broad-exception-caught
            if callable(self.error_handler):
                self.error_handler(exc)


class Observers:
    """
    Registry of observers.
    It is not possible to subscribe each observer more than once.
    Provide message_adapter if you would like to adapt message for all registered observers.
    Any exceptions of observers will be excepted while sending message.
    """

    def __init__(
        self,
        observers: Optional[Iterable[IObserver | Callable]] = None,
        *,
        message_adapter: Optional[IMessageAdapter | Callable] = None,
    ):
        self.registry = {id(x): x for x in observers or []}
        self.message_adapter = message_adapter

    def __bool__(self):
        return bool(self.registry)

    def __iter__(self):
        return iter(self.registry.values())

    def __len__(self):
        return len(self.registry)

    def __call__(self, message: Any):
        self.send_message(message)

    def add(self, observer: Any):
        """
        Subscribe observer
        """
        self.registry[id(observer)] = observer

    def remove(self, observer: Any):
        """
        Unsubscribe observer
        """
        self.registry.pop(id(observer), None)

    def send_message(self, message: Any):
        """
        Send message to observers
        """
        if self.message_adapter:
            message = self.message_adapter(message)

        for observer in self:
            # protection from reraise of errors receivers
            try:
                observer(message)
            except Exception:  # pylint: disable=broad-exception-caught
                continue
