from typing import Iterable

import scrapy
from scrapy.http import Response, Request
from scrapy.selector import Selector, SelectorList

from scraper.items import InvitroAnalyzeItem, InvitroCityItem
from scraper.utils import urljoin, extract_all_inner_text, parse_price


class AbstractInvitroSpider(scrapy.Spider):
    name = None
    allowed_domains = ['www.invitro.ru']
    base_url = 'https://www.invitro.ru/'
    start_urls = ['https://www.invitro.ru/analizes/for-doctors/']

    city_whitelist = ['Москва', 'Екатеринбург', 'Краснодар', 'Тюмень', 'Казань']

    def extract_invitro_cities(self, response: Response) -> Iterable[InvitroCityItem]:
        self.logger.debug(f'Processing main page (scraping cities): "{response.url}"')

        city_elements: SelectorList | list[Selector]
        city_elements = response.css('.select-basket-city-column > a.select-basket-city-item')

        city_data = []
        for element in city_elements:
            href = element.attrib.get('href', None)
            if href is None:
                self.logger.debug(f'Skip cause no href: {element}')
                continue

            name = element.css('*::text').extract_first(default=None)
            if name not in self.city_whitelist:
                self.logger.debug(f'Skip city cause not in whitelist: {name}')
                continue

            self.logger.debug('Parsed city: %s', name)
            url = urljoin(self.base_url, href)
            city_data.append((href, url, name))
        city_data = sorted(set(city_data))

        for href, url, name in city_data:
            yield InvitroCityItem(href=href, url=url, name=name)

    def parse(self, response: Response, **kwargs):
        # Не используем стандартный обработчик, т.к. для каждого шага паука определили свои
        raise NotImplemented


class InvitroAnalysisSpider(AbstractInvitroSpider):
    name = 'invitro_analysis'

    def start_requests(self) -> Iterable[Request]:
        self.logger.debug(f'Sending start requests: {self.start_urls}')

        for url in self.start_urls:
            add_data = {'spider_name': self.name}
            yield Request(
                meta={'add_data': add_data},
                url=url,
                callback=self.parse_cities,
            )

    def parse_cities(self, response: Response) -> Iterable[Request]:
        for city in self.extract_invitro_cities(response):
            self.logger.debug(f'Goto url for city "{city.name}": "{city.url}"')

            add_data = {
                **response.meta.get('add_data', {}),
                'city_href': city.href,
                'city_url': city.url,
                'city_name': city.name,
            }
            yield Request(
                meta={  # передаём meta-данные дальше - к другим обработчикам
                    **response.meta,
                    'add_data': add_data,
                },
                url=city.url,
                callback=self.parse_analysis_list,
                dont_filter=True,
            )

    def parse_analysis_list(self, response: Response) -> Iterable[Request]:
        self.logger.debug(f'Processing analysis list page: "{response.url}"')

        visible_query = '.pagination-items > .show-block-wrap:not([data-section-id]) .result-item__title > a'
        hidden_query = '#simplified_content > .node:not([data-section-id]) > a'

        analysis_elements: SelectorList | list[Selector]
        analysis_elements = response.css(visible_query) + response.css(hidden_query)
        for element in analysis_elements:
            href = element.attrib.get('href', None)
            if href is None:
                self.logger.debug(f'Skip cause no href: {element}')
                continue

            url = urljoin(self.base_url, href)
            self.logger.debug(f'Goto url for analysis data: "{url}"')

            add_data = {
                **response.meta.get('add_data', {}),
                'analysis_url': url,
                'analysis_href': href,
            }

            yield Request(
                meta={  # передаём meta-данные дальше - к другим обработчикам
                    **response.meta,
                    'add_data': add_data,
                },
                url=url,
                callback=self.parse_analysis_info,
            )

    def parse_analysis_info(self, response: Response) -> Iterable[dict]:
        self.logger.debug(f'Processing analysis info page: "{response.url}"')

        name: str = response.css('.title-block.title-block--img.title-block--narrow > h1::text').extract_first()
        description: str = extract_all_inner_text(
            response.css(
                '.article__slider-content-box.article__slider-analysis__content-box > '
                '.article__slider-content:nth-child(1)'
            )[0]
        )
        preparation: str = extract_all_inner_text(
            response.css(
                '.article__slider-content-box.article__slider-analysis__content-box > '
                '.article__slider-content:nth-child(2)'
            )[0]
        )
        purpose: str = extract_all_inner_text(
            response.css(
                '.article__slider-content-box.article__slider-analysis__content-box > '
                '.article__slider-content:nth-child(3)'
            )[0]
        )
        interpretation: str = extract_all_inner_text(
            response.css(
                '.article__slider-content-box.article__slider-analysis__content-box > '
                '.article__slider-content:nth-child(4)'
            )[0]
        )
        article_number: str = response.css(
            '.info-block__section--article > .info-block__price::text'
        ).extract_first()
        total_price: str = response.css(
            '.info-block__section--total > '
            '.info-block__price-text > '
            '.info-block__price--total::text'
        ).extract_first()
        total_price = parse_price(total_price.replace('\xa0', '\n'))

        add_data = response.meta.get('add_data', {})
        yield InvitroAnalyzeItem(
            city_href=add_data.get('city_href'),
            city_url=add_data.get('city_url'),
            city_name=add_data.get('city_name'),
            analysis_href=add_data.get('analysis_href'),
            analysis_url=add_data.get('analysis_url'),
            analysis_name=name.strip(),
            description=description.strip(),
            preparation=preparation.strip(),
            purpose=purpose.strip(),
            interpretation=interpretation.strip(),
            article_number=article_number.strip(),
            total_price=total_price,
        )


class InvitroCitySpider(AbstractInvitroSpider):
    name = 'invitro_city'

    def start_requests(self) -> Iterable[Request]:
        self.logger.debug(f'Sending start requests: {self.start_urls}')

        for url in self.start_urls:
            add_data = {'spider_name': self.name}
            yield Request(
                meta={'add_data': add_data},
                url=url,
                callback=self.parse_cities,
            )

    def parse_cities(self, response: Response) -> Iterable[InvitroCityItem]:
        for city in self.extract_invitro_cities(response):
            yield city
