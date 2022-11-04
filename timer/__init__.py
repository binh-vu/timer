import csv
from pathlib import Path
import time
from contextlib import contextmanager
from typing import Union


class TimerCount:
    def __init__(self, name: str, timer: "Timer"):
        self.name = name
        self.timer = timer
        self.start = time.time()

    def stop(self):
        self.timer.categories[self.name] += time.time() - self.start
        return self.timer


class Timer:
    instance = None

    def __init__(self):
        self.categories = {}

    @staticmethod
    def get_instance():
        if Timer.instance is None:
            Timer.instance = Timer()
        return Timer.instance

    @contextmanager
    def watch(self, name: str = "default"):
        try:
            count = self.start(name)
            yield None
        finally:
            count.stop()

    @contextmanager
    def watch_and_report(
        self,
        msg: str,
        print_fn=None,
        precision: int = 3,
        append_to_file: Union[None, str, Path] = None,
    ):
        """Watch and report the timer results to stdout and optionally to a file

        Args:
            msg: message to print before the report
            print_fn: function to print the results (default is print to stdout)
            precision: number of decimal places to round to
            append_to_file: file to append the results to if it's not None
        """
        print_fn = print_fn or print
        start = time.time()

        try:
            yield None
        finally:
            end = time.time()
            print_fn(msg + f": {format(end - start, f'.{precision}f')} seconds")

        if append_to_file is not None:
            Path(append_to_file).parent.mkdir(parents=True, exist_ok=True)
            rows = []
            if not Path(append_to_file).exists():
                rows.append(["name", "time"])
            rows.append([msg, end - start])
            with open(append_to_file, "a") as f:
                writer = csv.writer(
                    f, delimiter=",", quoting=csv.QUOTE_MINIMAL, lineterminator="\n"
                )
                writer.writerows(rows)

    def start(self, name: str = "default"):
        if name not in self.categories:
            self.categories[name] = 0.0
        return TimerCount(name, self)

    def report(
        self,
        print_fn=None,
        precision: int = 3,
        append_to_file: Union[None, str, Path] = None,
    ):
        """Report the timer results to stdout and optionally to a file

        Args:
            print_fn: function to print the results
            precision: number of decimal places to round to
            append_to_file: file to append the results to if it's not None
        """
        print_fn = print_fn or print
        if len(self.categories) == 0:
            print_fn("--- Nothing to report ---")
            return

        print_fn("Runtime report:")
        for k, v in self.categories.items():
            print_fn(f"\t{k}: {format(v, f'.{precision}f')} seconds")

        if append_to_file is not None:
            rows = []
            if not Path(append_to_file).exists():
                rows.append(["name", "time"])
            for k, v in self.categories.items():
                rows.append([k, v])

            with open(append_to_file, "a") as f:
                writer = csv.writer(
                    f, delimiter=",", quoting=csv.QUOTE_MINIMAL, lineterminator="\n"
                )
                writer.writerows(rows)

    def get_time(self, name: str = "default"):
        return self.categories[name]
