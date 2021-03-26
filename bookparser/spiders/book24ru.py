import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem


class Book24ruSpider(scrapy.Spider):
    name = 'book24ru'
    allowed_domains = ['book24.ru']
    start_urls = ['https://book24.ru/search/?q=%D1%84%D0%B0%D0%BD%D1%82%D0%B0%D1%81%D1%82%D0%B8%D0%BA%D0%B0']

    def parse(self, response: HtmlResponse):
        books = response.xpath('//a[contains(@class, "book-preview__title-link")]/@href').extract()
        for book in books:
            yield response.follow(book, callback=self.book_parse)

        next_page = response.xpath('//a[contains(text(), "Далее")]/@href').extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def book_parse(self, response: HtmlResponse):
        book_link = response.url
        book_name = response.xpath("//h1/text()").extract_first()
        book_authors = response.xpath('//a[@itemprop="author"]/text()').extract_first()
        book_basic_price = response.xpath("//div[@class='item-actions__price-old']/text()").extract()
        book_sale_price = response.xpath("//div[@class='item-actions__price']/b/text()").extract()
        book_rating = response.xpath("//span[@class='rating__rate-value']/text()").extract()

        yield BookparserItem(book_link=book_link,
                             book_name=book_name,
                             book_authors=book_authors,
                             book_basic_price=book_basic_price,
                             book_sale_price=book_sale_price,
                             book_rating=book_rating)


