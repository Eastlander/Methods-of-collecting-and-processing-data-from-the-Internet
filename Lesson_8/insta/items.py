# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstaItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field() # поле для внутреннего индекса MongoDB
    main_acc_name = scrapy.Field() # ник таргет-пользователя
    status_name = scrapy.Field() # статус отношения к таргет-пользователю подписчик, или подписка
    user_id = scrapy.Field() # ID пользователя
    user_name = scrapy.Field() # ник пользователя
    user_full_name = scrapy.Field() # полное имя
    avatar = scrapy.Field() # аватар
    user_data = scrapy.Field() # информация о пользователе(json)
