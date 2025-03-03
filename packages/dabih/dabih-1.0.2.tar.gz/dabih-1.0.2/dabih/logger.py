import logging
import sys
from typing import NoReturn
from pathlib import Path

GREY = "\x1b[38;20m"
YELLOW = "\x1b[33;20m"
RED = "\x1b[31;20m"
BOLD_RED = "\x1b[31;1m"
CYAN = "\x1b[36;20m"
RESET = "\x1b[0m"


class CustomFormatter(logging.Formatter):
    def format(self, record):
        log_fmt = "%(message)s"
        log_fmt_name = "%(levelname)s: %(message)s"
        formats = {
            logging.DEBUG: f"{GREY}{log_fmt}{RESET}",
            logging.INFO: f"{GREY}{log_fmt}{RESET}",
            logging.WARNING: f"{YELLOW}{log_fmt_name}{RESET}",
            logging.ERROR: f"{RED}{log_fmt_name}{RESET}",
            logging.CRITICAL: f"{BOLD_RED}{log_fmt_name}{RESET}",
        }
        log_fmt = formats.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


def setup_logger(verbose: bool = False) -> None:
    """
    Sets up a logger with a custom handler and formatter.

    Parameters:
        use_file: If True, a file handler is added to the logger.
        verbose: If True, the logger's level is set to DEBUG. Otherwise, to INFO.

    Returns:
        None
    """
    logger = logging.getLogger(__name__)
    if verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(CustomFormatter())
    logger.addHandler(stdout_handler)


def dbg(msg):
    logger = logging.getLogger(__name__)
    logger.debug(msg)


def log(msg):
    logger = logging.getLogger(__name__)
    logger.info(msg)


def warn(msg):
    logger = logging.getLogger(__name__)
    logger.warning(msg)


def error(msg):
    logger = logging.getLogger(__name__)
    logger.error(msg)


def critical(msg) -> NoReturn:
    logger = logging.getLogger(__name__)
    logger.critical(msg)
    raise Exception(msg)
