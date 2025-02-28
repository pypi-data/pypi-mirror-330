**observerutil** is simple and powerful observer pattern tool.

## How to install
You could install from PyPi:
```bash
$ python3 -m pip install observerutil
```

Any callable can become observer

```python
from typing import Any
from observerutil import Observers

def func_a(message: Any):
    ...

def func_b(message: Any):
    ...

observers = Observers([func_a])
observers.add(func_b)
my_message = 'some message here'
# or
my_message = {1: 2}

# distribute message to func_a and func_b
observers.send_message(my_message)
```

But in this case any exception will be ignored. 
If you would like to catch exceptions then use Observer with error handler.

```python
from typing import Any
from observerutil import Observer, Observers, ErrorHandler


def func_a(message: int):
    print(100 / message)


def write_exception_to_logs(exc: Exception):
    ...


observer = Observer(func_a, error_handler=write_exception_to_logs)
observers = Observers()
observers.add(func_a)

my_message = 0
observers.send_message(my_message)
```

If you would like to adapt message for observers in the collection then add message adapter
```python
from typing import Any
from observerutil import Observers


def func_a(message: int):
    print(100 / message)

def convert_to_int(message: str):
    return int(message)

observers = Observers(message_adapter=convert_to_int)
observers.add(func_a)

my_message = '2'
# any exceptions of observers (funcs or Observer instances) will be excepted while sending
observers.send_message(my_message)
```
