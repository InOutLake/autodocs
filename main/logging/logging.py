import logging


def setup_logging(verbose_level: int = 0) -> None:
    datefmt = "%H:%M:%S"
    format = "%(levelname)s: %(message)s"
    if verbose_level == 0:
        level = logging.WARNING
    elif verbose_level == 1:
        level = logging.INFO
    else:
        level = logging.DEBUG
        format = "[%(ascitime)s | %(levelname)s]  %(message)s"

    logging.basicConfig(level=level, format=format, datefmt=datefmt)
