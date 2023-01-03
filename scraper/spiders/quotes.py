import scrapy
from scrapy.http import Response


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    # start_urls = ['https://example.com/']

    def start_requests(self):
        for page in range(1, 10 + 1):
            url = f'https://quotes.toscrape.com/page/{page}/'
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: Response, **kwargs):
        page = response.url.split("/")[-2]
        texts: list[str] = response.css('.quote > .text::text').extract()
        authors: list[str] = response.css('.quote .author::text').extract()
        author_urls: list[str] = response.xpath("//*[@class='quote']/span/a/@href").extract()
        self.log(f'Processed page {page}')
        for author, text, author_url in zip(authors, texts, author_urls):
            yield {
                'author': author,
                'text': text,
                'author_url': author_url,
            }
