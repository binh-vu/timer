# timer ![PyPI](https://img.shields.io/pypi/v/timer4) ![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)

`timer` is a library to time your Python code.

## Installation

```bash
pip install timer4  # not timer
```

## Usage

- `timer` uses `with` statement to watch how long your code running:

```python
import time
from timer import Timer


with Timer().watch_and_report(msg='test'):
    # running code that do lots of computation
    time.sleep(1.0)

# when the code reach this part, it will output the message and the time it tooks.
# for example:
#     test: 10.291 seconds
```

- If you don't want to report the result immediately, use the `watch` method instead. Whenever you've done, call `report`.

```python
import time
from timer import Timer

# you can either create a timer variable first, or use Timer.get_instance()
# that will return a singleton variable.

total = 0
for item in range(7):
    # only measure the part that we want
    with Timer.get_instance().watch("sum of square"):
        total += item ** 2
        time.sleep(0.2)

    # doing other things that we don't want to measure
    time.sleep(0.8)

Timer.get_instance().report()
```

- You can also use different way to print the message, such as using logging by passing a printing function to the report method: `report(print_fn=logger.info)`

- You can also choose to append the result to a file `report(append_to_file='/tmp/runtime.csv')`. This is useful if you want to measure runtime of your method and put it to a file to plot it later.
