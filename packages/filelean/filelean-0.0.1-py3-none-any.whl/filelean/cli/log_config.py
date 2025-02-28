from loguru import logger
import click
import sys

LOGGING_LEVELS = {
    0: "CRITICAL",
    1: "ERROR", 
    2: "WARNING",
    3: "INFO",
    4: "DEBUG"
}  #: a mapping of `verbose` option counts to logging levels

class Info(object):
    """An information object to pass data between CLI functions."""
    def __init__(self):  # Note: This object must have an empty constructor.
        """Create a new instance."""
        self.verbose: int = 0

# pass_info is a decorator for functions that pass 'Info' objects.
#: pylint: disable=invalid-name
pass_info = click.make_pass_decorator(Info, ensure=True)

def setup_logging(verbose: int) -> str:
    """Setup logging configuration"""
    if verbose > 0:
        logger.remove()  # Remove default handler
        level = LOGGING_LEVELS[verbose] if verbose in LOGGING_LEVELS else "DEBUG"
        logger.add(sys.stderr, level=level)
        return level
    return "CRITICAL"
