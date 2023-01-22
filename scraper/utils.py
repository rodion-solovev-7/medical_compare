import decimal
import re
from urllib import parse

from scrapy import Selector


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


def parse_price(text: str) -> decimal.Decimal:
    """Парсит цену из строк вида '1 000.00 руб.' в Decimal"""
    price: str = re.findall(r'\d+\s?\d+[.,]?\d+', text)[0]
    price = price.replace(' ', '').replace(',', '.')
    return decimal.Decimal(price)
