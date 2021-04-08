# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst
import re

def price_to_int(price):
    if price:
        return int(re.sub('\D', '', price))
    return price

def clear_spaces(features_value):
    if features_value:
        features_value = features_value.replace(' ', '').replace('\n', '')
    return features_value

class LeroyMerlinItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    article = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(price_to_int), output_processor=TakeFirst())
    photo = scrapy.Field()
    link = scrapy.Field(output_processor=TakeFirst())
    features_name = scrapy.Field()
    features_value = scrapy.Field(input_processor=MapCompose(clear_spaces), output_processor=TakeFirst())
    features = scrapy.Field()
