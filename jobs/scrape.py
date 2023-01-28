import subprocess

from loguru import logger

import config
from ._base import repeat_every


@repeat_every(seconds=config.AUTO_SCRAPING_DELAY, wait_first=False, logger=logger)
async def scrape():
    spiders = [
        'invitro_city',
        'citilab_city',
        'invitro_analysis',
        'citilab_analysis',
    ]
    for spider in spiders:
        run_line = f'scrapy crawl {spider}'
        process = subprocess.Popen(run_line.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
