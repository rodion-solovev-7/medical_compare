from loguru import logger

from ._base import repeat_every


@repeat_every(seconds=1, wait_first=True, logger=logger)
async def app_alive():
    logger.info('I am alive')
