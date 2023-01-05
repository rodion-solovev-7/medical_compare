import logging
from typing import Iterable
from urllib import parse

import scrapy
from scrapy.http import Response, Request
from scrapy.selector import Selector, SelectorList


def urljoin(base: str, url: str, allow_fragments: bool = True) -> str:
    """Версия urljoin, которая не ломает мозг"""
    if base.endswith('/'):
        base = base[:-1]
    base = f'{base}/'
    if url.startswith('/'):
        url = url[1:]
    return parse.urljoin(base=base, url=url, allow_fragments=allow_fragments)


class InvitroAnalysisSpider(scrapy.Spider):
    name = 'invitro_analysis'

    allowed_domains = ['www.invitro.ru']
    base_url = 'https://www.invitro.ru/'
    start_urls = ['https://www.invitro.ru/analizes/for-doctors/']

    def start_requests(self) -> Iterable[Request]:
        self.log(f'Sending start requests: {self.start_urls}', level=logging.DEBUG)

        for url in self.start_urls:
            yield Request(
                meta={
                    'spider_name': self.name,
                },
                url=url,
                callback=self.parse_cities,
            )

    def parse_cities(self, response: Response) -> Iterable[Request]:
        self.log(f'Processing main page (scraping cities): "{response.url}"', level=logging.DEBUG)

        city_elements: SelectorList | list
        city_elements = response.css('.select-basket-city-column > a.select-basket-city-item')

        for element in city_elements:
            href = element.attrib.get('href', None)
            if href is None:
                self.log(f'Skip cause no href: {element}', level=logging.DEBUG)
                continue

            # TODO
            if 'krasnodar' not in href:
                continue

            name = element.css('*::text').extract_first(default=None)
            self.log(f'HREF="{href}"', level=logging.DEBUG)
            url = urljoin(self.base_url, href)
            self.log(f'Goto url for city "{name}": "{url}"', level=logging.DEBUG)

            yield Request(
                meta={  # передаём meta-данные дальше - к другим обработчикам
                    **response.meta,
                    'city_href': href,
                    'city_url': url,
                    'city_name': name,
                },
                url=url,
                callback=self.parse_analysis_list,
            )

    def parse_analysis_list(self, response: Response) -> Iterable[Request]:
        self.log(f'Processing analysis list page: "{response.url}"', level=logging.DEBUG)

        visible_query = '.pagination-items > .show-block-wrap:not([data-section-id]) .result-item__title > a'
        hidden_query = '#simplified_content > .node:not([data-section-id]) > a'

        analysis_elements: SelectorList | list[Selector]
        analysis_elements = response.css(visible_query) + response.css(hidden_query)
        for element in analysis_elements:
            href = element.attrib.get('href', None)
            if href is None:
                self.log(f'Skip cause no href: {element}', level=logging.DEBUG)
                continue

            url = urljoin(self.base_url, href)
            self.log(f'Goto url for analysis data: "{url}"', level=logging.DEBUG)

            yield Request(
                meta={  # передаём meta-данные дальше - к другим обработчикам
                    **response.meta,
                    'analysis_url': url,
                    'analysis_href': href,
                },
                url=url,
                callback=self.parse_analysis_info,
            )

    def parse_analysis_info(self, response: Response) -> Iterable[dict]:
        self.log(f'Processing analysis info page: "{response.url}"', level=logging.DEBUG)

        name: str = response.css('.title-block.title-block--img.title-block--narrow > h1::text').extract_first()

        # TODO: здесь нужно спарсить всё, что не приколочено гвоздями
        yield {
            'meta': response.meta,
            'analysis_name': name,
        }

    def parse(self, response: Response, **kwargs):
        # Не используем стандартный обработчик, т.к. для каждого шага паука определили свои
        raise NotImplemented
