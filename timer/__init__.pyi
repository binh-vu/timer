from typing import Union
from pathlib import Path

class TimerCount:
    def __init__(self, name: str, timer: Timer): ...
    
    def stop(self) -> Timer: ...

class Timer:
    def __init__(self): ...

    @staticmethod
    def get_instance() -> Timer: ...

    def watch(self, name: str = "default"): ...

    def watch_and_report(
        self,
        msg: str,
        print_fn=None,
        precision: int = 3,
        append_to_file: Union[None, str, Path] = None,
    ): ...

    def start(self, name: str = "default") -> TimerCount: ...

    def report(
        self,
        print_fn=None,
        precision: int = 3,
        append_to_file: Union[None, str, Path] = None,
    ): ...

    def get_time(self, name: str = "default") -> float: ...

    def merge(self, timer: Timer): ...

    