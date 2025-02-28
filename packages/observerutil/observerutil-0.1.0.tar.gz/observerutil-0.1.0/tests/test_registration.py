from observerutil import Observer, Observers


def test_subscribe_observer():
    observer = Observer(
        func=lambda message: print(message),
    )
    observers = Observers()
    assert len(observers) == 0
    observers.add(observer)
    assert len(observers) == 1


def test_unsubscribe_observer():
    observer = Observer(
        func=lambda message: print(message),
    )
    observers = Observers()
    assert len(observers) == 0
    observers.add(observer)
    assert len(observers) == 1
    observers.remove(observer)
    assert len(observers) == 0


def test_twice_registration():
    """
    Ignore reraised errors
    """
    observer = Observer(
        func=lambda message: print(message),
    )
    observers = Observers()
    assert len(observers) == 0
    observers.add(observer)
    assert len(observers) == 1
    observers.add(observer)
    assert len(observers) == 1
