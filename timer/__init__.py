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
        self.end = time.time()
        self.timer.categories[self.name] += self.end - self.start
        return self.timer


class Timer:
    instance = None

    def __init__(self):
        self.categories: dict[str, float] = {}

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
        preprint: bool = False,
        precision: int = 3,
        append_to_file: Union[None, str, Path] = None,
        disable: bool = False,
    ):
        """Watch and report the timer results to stdout and optionally to a file

        Args:
            msg: message to print before the report
            print_fn: function to print the results (default is print to stdout)
            preprint: whether to print the message before the timer starts
            precision: number of decimal places to round to
            append_to_file: file to append the results to if it's not None
            disable: whether to disable the timer
        """
        if disable:
            yield None
            return
        
        print_fn = print_fn or print
        counter = self.start(msg)

        if preprint:
            print_fn(msg + ": ...")

        try:
            yield None
        finally:
            counter.stop()
            print_fn(msg + f": {format(counter.end - counter.start, f'.{precision}f')} seconds")

        if append_to_file is not None:
            Path(append_to_file).parent.mkdir(parents=True, exist_ok=True)
            rows = []
            if not Path(append_to_file).exists():
                rows.append(["name", "time"])
            rows.append([msg, counter.end - counter.start])
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

    def merge(self, timer: "Timer"):
        """Merge the results of another timer into this one. This is useful when we have multiple tasks running
        in parallel so we can run multiple timer instance and merge the results at the end.

        Note: this function mutate the timer!
        """
        for k, v in timer.categories.items():
            if k not in self.categories:
                self.categories[k] = v
            else:
                self.categories[k] += v
        return self


@contextmanager
def watch_and_report(
    msg: str,
    print_fn=None,
    preprint: bool = False,
    precision: int = 3,
    append_to_file: Union[None, str, Path] = None,
    disable: bool = False,
):
    """Watch and report the timer results to stdout and optionally to a file

    Args:
        msg: message to print before the report
        print_fn: function to print the results (default is print to stdout)
        preprint: whether to print the message before the timer starts
        precision: number of decimal places to round to
        append_to_file: file to append the results to if it's not None
        disable: whether to disable the timer
    """
    if disable:
        yield None
        return
    print_fn = print_fn or print
    start = time.time()

    if preprint:
        print_fn(msg + ": ...")

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