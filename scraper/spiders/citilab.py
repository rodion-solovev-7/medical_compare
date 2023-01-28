from typing import Iterable

import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Response, Request
from scrapy.selector import Selector, SelectorList

from scraper.items import AnalyzeItem, CityItem
from scraper.utils import urljoin, parse_price


class AbstractCitilabSpider(scrapy.Spider):
    name = None
    organisation = 'citilab'
    allowed_domains = ['citilab.ru']
    base_url = 'https://citilab.ru/'
    start_urls = [
        'https://citilab.ru/local/components/reaspekt/reaspekt.geoip/templates/my01/ajax_popup_city.php',
    ]

    city_whitelist = ['Москва', 'Екатеринбург', 'Краснодар', 'Тюмень', 'Казань']

    def extract_citilab_cities(self, response: Response) -> Iterable[CityItem]:
        self.logger.debug(f'Processing main page (scraping cities): "{response.url}"')

        city_elements: SelectorList | list[Selector]
        city_elements = response.css('.reaspekt_row > .reaspektGeobaseAct > a')

        city_data = []
        for element in city_elements:
            city_code = element.attrib.get('data-code', None)
            if city_code is None:
                self.logger.debug(f'Skip cause no href: {element}')
                continue

            href = urljoin(self.base_url, f'/{city_code}/catalog')

            name = element.css('*::text').extract_first(default=None)
            name = name.strip()

            if name not in self.city_whitelist:
                continue

            self.logger.debug(f'HREF="{href}"')
            url = urljoin(self.base_url, href)
            self.logger.debug(f'Goto url for city "{name}": "{url}"')
            city_data.append((href, url, name))
        city_data = sorted(set(city_data))

        for href, url, name in city_data:
            yield CityItem(
                organisation=self.organisation,
                href=href,
                url=url,
                name=name,
            )

    def parse(self, response: Response, **kwargs):
        # Не используем стандартный обработчик, т.к. для каждого шага паука определили свои
        raise NotImplemented


class CitilabAnalysisSpider(AbstractCitilabSpider):
    name = 'citilab_analysis'

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
        for city in self.extract_citilab_cities(response):
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
                callback=self.parse_categories,
                dont_filter=True,
            )

    def parse_categories(self, response: Response) -> Iterable[Request]:
        self.logger.debug(f'Processing analysis list page: "{response.url}"')

        for request in self.parse_analyses_on_category_page(response):
            yield request

        category_elements: SelectorList | list[Selector]
        category_elements = response.css('.sidebar-list > .ln > .active > ul > li > a')
        for element in category_elements:
            href = element.attrib.get('href', None)
            if href is None:
                self.logger.debug(f'Skip cause no href: {element}')
                continue

            url = urljoin(self.base_url, href)
            self.logger.debug(f'Goto url for analysis data: "{url}"')

            add_data = {
                **response.meta.get('add_data', {}),
                'category_url': url,
                'category_href': href,
            }
            yield Request(
                meta={  # передаём meta-данные дальше - к другим обработчикам
                    **response.meta,
                    'add_data': add_data,
                },
                url=url,
                callback=self.parse_analyses_on_category_page,
            )

    def parse_analyses_on_category_page(self, response: Response) -> Iterable[Request]:
        analysis_elements: SelectorList | list[Selector]
        analysis_elements = response.css('.search-item > .row > .col-lg-12.col-md-10 > a')
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

    def parse_analysis_info(self, response: Response) -> Iterable[AnalyzeItem]:
        self.logger.debug(f'Processing analysis info page: "{response.url}"')
        name: str = response.css('.header-second > .container-fluid > h1::text').extract_first()

        detail: SelectorList = response.css('.inner-content > .detail')
        info = self.extract_info_from_detail(detail.extract_first())
        description = info.get('Описание', None)
        purpose = info.get('Показания к назначению', None)
        preparation = info.get('Подготовка к исследованию', None)

        price = response.css('.price-block-detail > .new-price::text').extract_first()
        if price is None:
            self.logger.info(f'Skip cause no price for analysis: {response.url}')
            return
        price = parse_price(price)

        add_data = response.meta.get('add_data', {})
        yield AnalyzeItem(
            organisation=self.organisation,
            url=response.url,
            city_href=add_data.get('city_href'),
            city_url=add_data.get('city_url'),
            city_name=add_data.get('city_name'),
            analysis_href=add_data.get('analysis_href'),
            analysis_url=add_data.get('analysis_url'),
            analysis_name=name.strip(),
            description=description.strip(),
            preparation=preparation.strip(),
            purpose=purpose.strip(),
            interpretation=None,
            article_number=None,
            total_price=price,
        )

    def extract_info_from_detail(self, detail_html: str) -> dict[str, str]:
        soup = BeautifulSoup(detail_html, 'html.parser')
        tags = list(next(soup.children).children)
        data = {}
        current_head = None
        current_content = []
        for tag in tags:
            if tag.name == 'h2':
                data[current_head] = ' '.join(current_content)
                current_content.clear()
                current_head = tag.text
            elif current_head is not None:
                # игнорируем все теги, помимо h3 и текста (у текста без тегов name == None)
                if tag.name is None:
                    current_content.append(tag.text)
        data[current_head] = ' '.join(current_content)
        return data


class InvitroCitySpider(AbstractCitilabSpider):
    name = 'citilab_city'

    def start_requests(self) -> Iterable[Request]:
        self.logger.debug(f'Sending start requests: {self.start_urls}')
        for url in self.start_urls:
            add_data = {'spider_name': self.name}
            yield Request(
                meta={'add_data': add_data},
                url=url,
                callback=self.parse_cities,
            )

    def parse_cities(self, response: Response) -> Iterable[CityItem]:
        for city in self.extract_citilab_cities(response):
            yield city

