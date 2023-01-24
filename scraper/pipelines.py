# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from dependency_injector.wiring import inject, Provide
from itemadapter import ItemAdapter
from scrapy import Item, Spider

from common import di, db
from common.db import models
from scraper.items import InvitroAnalyzeItem, InvitroCityItem


class SaveDbPipeline:
    @inject
    def open_spider(self, _: Spider):
        # Init di container for @inject working
        di.Container()
        db.apply_migrations()

    @inject
    async def process_item(
        self,
        item: Item | InvitroAnalyzeItem | dict,
        spider: Spider,
        session: db.AsyncSession = Provide[di.Container.session],
    ) -> Item:
        spider.logger.debug('Start processing item %s: %s', type(item), item)
        record = None

        if isinstance(item, InvitroAnalyzeItem):
            spider.logger.debug('Identified InvitroAnalyze result')
            adapter = dict(**ItemAdapter(item))
            adapter['name'] = adapter.pop('analysis_name', None)
            record = models.Analysis(**adapter)
        elif isinstance(item, InvitroCityItem):
            spider.logger.debug('Identified InvitroCity result')
            adapter = dict(**ItemAdapter(item))
            record = models.City(**adapter)

        if record is not None:
            session.add(record)
            await session.commit()
        else:
            spider.logger.debug('NO_SAVE_DB: cannot identify item %s: %s', type(item), item)
        return item
