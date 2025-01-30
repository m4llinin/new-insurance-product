from loguru import logger
from src.core.config.config import LoggingConfig
import sys


def setup_logging(config: LoggingConfig):
    logger.remove()

    logger.add(
        sys.stdout,
        level="DEBUG",
        format=config.FORMAT,
        backtrace=config.BACKTRACE,
    )

    logger.add(
        "logs/info.log",
        level="INFO",
        format=config.FORMAT,
        rotation=config.ROTATION,
        compression=config.COMPRESSION,
        backtrace=config.BACKTRACE,
        serialize=config.SERIALIZE,
    )

    logger.add(
        "logs/error.log",
        level="ERROR",
        format=config.FORMAT,
        rotation=config.ROTATION,
        compression=config.COMPRESSION,
        backtrace=config.BACKTRACE,
        serialize=config.SERIALIZE,
    )
