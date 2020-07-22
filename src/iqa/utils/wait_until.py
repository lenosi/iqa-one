import time
import timeit


def wait_until(check, timeout, pause, clock=timeit.default_timer):
    """Wait until..."""

    ref = clock()
    now = ref
    while (now - ref) < timeout:
        if check():
            return
        time.sleep(pause)
        now = clock()

    raise Exception("Timeout reached while waiting on!")
