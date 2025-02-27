"""Skaha Logging Utility."""

import logging
from typing import Optional


def get_logger(
    name: str = __name__, level: int = logging.INFO, filename: Optional[str] = None
) -> logging.Logger:
    """Logging utility.

    Args:
        name (str): Name of the logger. Defaults to __name__.
        level (int): Logging Level. Defaults to logging.INFO.
        filename (Optional[str], optional): Log file name. Defaults to None.

    Returns:
        logging.Logger: Logger object.

    """
    # create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # create console handler and set level to debug
    streamer = logging.StreamHandler()
    streamer.setLevel(level)

    # create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # add formatter to ch
    streamer.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(streamer)

    # create file handler
    if filename:
        filer = logging.FileHandler(filename)
        filer.setLevel(level)

        # add formatter to filer
        filer.setFormatter(formatter)

        # add filer to logger
        logger.addHandler(filer)

    logger.propagate = False

    return logger
