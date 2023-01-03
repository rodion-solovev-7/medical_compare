# flake8: noqa
import ast
import sys

from loguru import logger

from .base import *

try:
    from .local import *
except ImportError as e:
    print('Not found local.py')

# Override config variables from environment
for var in list(locals()):
    value = os.getenv(var)
    if value is None:
        continue
    try:
        locals()[var] = ast.literal_eval(value)
    except:
        locals()[var] = value


def setup_logger(log_format: str, level: str = 'DEBUG') -> None:
    """
    Настраивает логгирование с ротацией и автоматическим сжатием в zip.
    Returns:
        None
    """
    logger.remove()
    logger.add(sink=sys.stdout, format=log_format, level=level)


setup_logger(
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS UTCZ}</> | "
    "<level>{level: <8}</> | "
    "<cyan>{name}:{function}:{line}</> - <level>{message}</>"
)

# TODO: setup loggers from loguru
