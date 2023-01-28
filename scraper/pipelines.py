# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import sqlalchemy as sa
from dependency_injector.wiring import inject, Provide
from itemadapter import ItemAdapter
from scrapy import Item, Spider

from common import di, db
from common.db import models
from scraper.items import AnalyzeItem, CityItem


class SaveDbPipeline:
    @inject
    def open_spider(self, _: Spider):
        # Init di container for @inject working
        di.Container()
        db.apply_migrations()

    @inject
    async def process_item(
        self,
        item: Item | AnalyzeItem | dict,
        spider: Spider,
        session: db.AsyncSession = Provide[di.Container.session],
    ) -> Item:
        spider.logger.debug('Start processing item %s: %s', type(item), item)

        if isinstance(item, AnalyzeItem):
            spider.logger.debug('Identified AnalyzeItem result')
            await self.add_analysis(
                ItemAdapter(item),
                session=session,
            )
        elif isinstance(item, CityItem):
            spider.logger.debug('Identified CityItem result')
            await self.add_city(
                ItemAdapter(item),
                session=session,
            )
        else:
            spider.logger.debug('NO_SAVE_DB: cannot identify item %s: %s', type(item), item)

        return item

    async def add_analysis(
        self,
        adapter: ItemAdapter,
        *,
        session: db.AsyncSession,
    ) -> None:
        item = dict(**adapter)
        item['name'] = item.pop('analysis_name', None)

        q = sa.select(models.City).where(
            models.City.name == item['city_name'],
            models.City.organisation == item['organisation'],
        )
        result = await session.execute(q)
        city: db.City = result.one()[0]

        analysis = models.Analysis(**item, city_id=city.id)
        session.add(analysis)
        await session.commit()

    async def add_city(
        self,
        adapter: ItemAdapter,
        *,
        session: db.AsyncSession,
    ) -> None:
        item = dict(**adapter)
        q = sa.select(models.City).where(
            models.City.name == item['city_name'],
            models.City.organisation == item['organisation'],
        )
        result = await session.execute(q)
        if result.rowcount > 0:
            # upsert
            return

        city = models.City(**adapter)
        session.add(city)
        await session.commit()
