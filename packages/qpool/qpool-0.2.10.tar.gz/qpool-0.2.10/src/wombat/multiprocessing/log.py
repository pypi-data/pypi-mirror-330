import logging

from wombat.utils.errors.decorators import enforce_type_hints_contracts
from typing import Dict, Any, cast
from logging import Logger


@enforce_type_hints_contracts
def setup_logging(
    name: str = "QPoolLogger",
    level: int = logging.ERROR,
    log_file: str = "logfile.log",
):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Setup file logging
    file_handler = logging.FileHandler(log_file, mode="a")
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    return logger


def log(worker, message: str, level: int, props: Dict[str, Any]):
    logger: Logger = cast(Logger, props["logger"].instance)
    logger.log(level=level, msg=message)
