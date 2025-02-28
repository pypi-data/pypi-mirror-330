from helpers import (
    ResultKeeper,
    XErrorHandler,
    reraise,
)
from observerutil import Observer, Observers


def test_ignore_reraised_errors():
    """
    Ignore reraised errors
    """
    result_keeper = ResultKeeper(100)
    def testing_func(message: int):
        result_keeper.result = result_keeper.result // message

    error_handler = XErrorHandler(handlers=[reraise])
    observer = Observer(func=testing_func, error_handler=error_handler)
    observers = Observers(
        observers=[observer],
        message_adapter=lambda message: int(message),
    )
    assert result_keeper.result == 100
    message = 0
    observers.send_message(message)
    assert len(error_handler.exceptions) == 1
    assert isinstance(error_handler.exceptions[0], ZeroDivisionError)
