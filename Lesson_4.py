'''
1. Написать приложение, которое собирает основные новости с сайтов news.mail.ru, lenta.ru, yandex-новости.
Для парсинга использовать XPath. Структура данных должна содержать:
- название источника;
- наименование новости;
- ссылку на новость;
- дата публикации.
'''

import requests
from lxml import html
from pprint import pprint
from datetime import datetime as dt
from pymongo import MongoClient

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}

news = []

# lenta.ru

main_link = 'https://lenta.ru/'
response = requests.get(main_link, headers=header)

dom = html.fromstring(response.text)

items = dom.xpath('//div[@class="span4"]/div[@class="item"]')

for item in items:
    news_item = {}
    name = item.xpath('.//a/text()')[0].replace('\xa0', ' ')
    link = item.xpath('.//a/@href')[0]
    date = item.xpath('.//time/@datetime')
    news_item['name'] = name
    news_item['link'] = main_link + link
    news_item['date'] = date
    news_item['source'] = 'lenta.ru'
    news.append(news_item)

# yandex.news

main_link = 'https://yandex.ru/'
response = requests.get(main_link, headers=header)

dom = html.fromstring(response.text)
items = dom.xpath('//ol/li')
date = dt.today().strftime("%d-%m-%Y")

for item in items:
    news_item = {}
    source = item.xpath('.//object/@title')[0]
    name = item.xpath('.//span[contains(@class ,"news__item-content")]/text()')[0].replace('\xa0', ' ')
    link = item.xpath('.//a/@href')[0]
    news_item['source'] = source
    news_item['link'] = link
    news_item['name'] = name
    news_item['date'] = date
    news.append(news_item)

# news.mail.ru

def get_source(link):

    response = requests.get(link, headers=header)
    dom = html.fromstring(response.text)
    items = dom.xpath('//div[contains(@class,"article js-article")]')

    for item in items:
        source = item.xpath('.//span[@ class ="link__text"]/text()')[0]
    return source

main_link = 'https://news.mail.ru'
response = requests.get(main_link, headers=header)
dom = html.fromstring(response.text)
items = dom.xpath('//a[contains(@class,"photo photo_full photo_scale")] | //a[contains(@class,"photo photo_small photo_scale photo_full js-topnews__item")]')
date = dt.today().strftime("%d-%m-%Y")

# перебор ссылок для добавления источника
i = 0
for item in items:
    news_item = {}
    name = item.xpath('.//span[@class="photo__title photo__title_new photo__title_new_hidden js-topnews__notification"]/text()')[0].replace('\xa0', ' ')
    link = item.xpath('//a[contains(@class, "js-topnews__item")]/@href')[i]

    news_item['name'] = name
    news_item['link'] = link

    source = get_source(link)
    news_item['source'] = source
    news_item['date'] = date

    news.append(news_item)
    i += 1

pprint(news)

'''
2. Сложить собранные данные в БД
'''

client = MongoClient('localhost', 27017)
db = client['news']

db.news.insert_many(news)

