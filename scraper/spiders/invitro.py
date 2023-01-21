import re
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


def extract_all_inner_text(selector: Selector) -> str:
    """Возвращает весь текст из селектора и его дочерних элементов.
    Предварительно очищает их от повторных пробелов, табуляций, переходов строк и пр. фигни.
    """
    all_text = '\n'.join(selector.css(' *::text').extract())
    all_text = '\n'.join(re.split(r'[\n\r]+', all_text))
    all_text = ' '.join(re.split(r'[\s\t]+', all_text))
    return all_text


class InvitroAnalysisSpider(scrapy.Spider):
    name = 'invitro_analysis'

    allowed_domains = ['www.invitro.ru']
    base_url = 'https://www.invitro.ru/'
    start_urls = ['https://www.invitro.ru/analizes/for-doctors/']

    def start_requests(self) -> Iterable[Request]:
        self.logger.debug(f'Sending start requests: {self.start_urls}')

        for url in self.start_urls:
            yield Request(
                meta={
                    'spider_name': self.name,
                },
                url=url,
                callback=self.parse_cities,
            )

    def parse_cities(self, response: Response) -> Iterable[Request]:
        self.logger.debug(f'Processing main page (scraping cities): "{response.url}"')

        city_elements: SelectorList | list[Selector]
        city_elements = response.css('.select-basket-city-column > a.select-basket-city-item')

        for element in city_elements:
            href = element.attrib.get('href', None)
            if href is None:
                self.logger.debug(f'Skip cause no href: {element}')
                continue

            # TODO
            if 'krasnodar' not in href:
                continue

            name = element.css('*::text').extract_first(default=None)
            self.logger.debug(f'HREF="{href}"')
            url = urljoin(self.base_url, href)
            self.logger.debug(f'Goto url for city "{name}": "{url}"')

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

        yield {
            'meta': response.meta,
            'analysis_name': name.strip(),
            'description': description.strip(),
            'preparation': preparation.strip(),
            'purpose': purpose.strip(),
            'interpretation': interpretation.strip(),
            'article_number': article_number.strip(),
            'total_price': total_price.strip(),
        }

    def parse(self, response: Response, **kwargs):
        # Не используем стандартный обработчик, т.к. для каждого шага паука определили свои
        raise NotImplemented
