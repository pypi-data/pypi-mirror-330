import logging


def start_logging(log_level: str = "WARN") -> None:
    """
    Add handlers to the logger if not exist

    :param log_level: Log level
    """
    if logging.getLogger("lineup_lang").hasHandlers():
        return
    logger = logging.getLogger("lineup_lang")
    logger.setLevel(log_level)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
