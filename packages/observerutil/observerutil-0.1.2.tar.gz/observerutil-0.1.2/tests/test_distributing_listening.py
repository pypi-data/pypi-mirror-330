from helpers import ResultKeeper, XErrorHandler
from observerutil import Observer, Observers


def test_distributing_listening():
    """
    Test adapt message and update instance variable
    """
    result_keeper = ResultKeeper(100)
    def testing_func(message: int):
        result_keeper.result = result_keeper.result // message

    error_handler = XErrorHandler()
    observer = Observer(func=testing_func, error_handler=error_handler)
    observers = Observers(
        observers=[observer],
        message_adapter=lambda message: int(message),
    )
    assert result_keeper.result == 100
    message = '2'
    observers.send_message(message)
    assert result_keeper.result == 50
    assert len(error_handler.exceptions) == 0
