import time
from timer import Timer

def test_watch_and_report():
    out = []
    with Timer().watch_and_report("test", print_fn=out.append):
        time.sleep(0.1)
    assert out[0].startswith("test: 0.")
    assert out[0].endswith(" seconds")
