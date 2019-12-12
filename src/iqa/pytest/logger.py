"""Provide a common interface to the `logging` module."""

from logging import getLogger, Logger

try:
    from logging import NullHandler
except ImportError:
    from logging import Handler

    class NullHandler(Handler):

        """Python-2.6 friendly NullHandler."""

        def emit(self, record) -> None:
            """Fake `emit` method."""
            pass


def get_logger(name: str) -> Logger:
    """Return an initialized logger."""
    log: Logger = getLogger(name)
    log.addHandler(NullHandler())
    return log
