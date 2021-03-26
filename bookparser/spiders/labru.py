import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem


class LabruSpider(scrapy.Spider):
    name = 'labru'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/%D0%9A%D1%83%D0%BB%D0%B8%D0%BD%D0%B0%D1%80%D0%B8%D1%8F/?stype=0']

    def parse(self, response: HtmlResponse):
        books = response.xpath('//a[@class="product-title-link"]/@href').extract()
        for book in books:
            yield response.follow(book, callback=self.book_parse)

        next_page = response.xpath("//a[@class='pagination-next__text']/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)


    def book_parse(self, response: HtmlResponse):
        book_link = response.url
        book_name = response.xpath("//h1/text()").extract_first()
        book_authors = response.xpath("//a[@data-event-label='author']/text()").extract_first()
        book_basic_price = response.xpath("//span[@class='buying-priceold-val-number']/text()").extract()
        book_sale_price = response.xpath("//span[@class='buying-pricenew-val-number']/text()").extract()
        book_rating = response.xpath("//div[@id='rate']/text()").extract_first()

        yield BookparserItem(book_link=book_link,
                             book_name=book_name,
                             book_authors=book_authors,
                             book_basic_price=book_basic_price,
                             book_sale_price=book_sale_price,
                             book_rating=book_rating)
