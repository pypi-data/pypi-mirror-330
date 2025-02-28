from helpers import XErrorHandler
from observerutil import Observer, Observers


def test_listening():
    """
    Ignore reraised errors
    """
    error_handler = XErrorHandler()
    messages = []
    observer = Observer(
        func=lambda message: messages.append(message),
        error_handler=error_handler
    )
    observers = Observers([observer])
    assert len(messages) == 0
    message = 1
    observers.send_message(message)
    assert len(messages) == 1
    assert len(error_handler.exceptions) == 0
