# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookparserItem(scrapy.Item):
    _id = scrapy.Field()
    book_link = scrapy.Field()
    book_name = scrapy.Field()
    book_authors = scrapy.Field()
    book_basic_price = scrapy.Field()
    book_sale_price = scrapy.Field()
    book_rating = scrapy.Field()
