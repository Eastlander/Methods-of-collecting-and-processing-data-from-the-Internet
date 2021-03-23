'''
2) Написать программу, которая собирает «Хиты продаж» с сайта техники mvideo
и складывает данные в БД. Магазины можно выбрать свои.
Главный критерий выбора: динамически загружаемые товары
'''

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import datetime
import time
import json
from pymongo import MongoClient
import pymongo.errors

def _mvideo_parse():
    chrome_options = Options()
    chrome_options.add_argument('start-maximized')
    driver = webdriver.Chrome('./chromedriver.exe',
                              options=chrome_options)
    driver.get('https://www.mvideo.ru/')
    time.sleep(7)
    information = driver.find_elements_by_xpath(
        '//div[contains(@class, "gallery-layout_products")]')
    new_item = information[0].find_element_by_tag_name('ul')
    # информация о товаре в аттрибуте 'data-init-param' в виде json
    item_params = json.loads(new_item.get_attribute('data-init-param'))
    count_item = item_params['ajaxContentLoad']['total']  # количество товаров в динамическом списке
    items = new_item.find_elements_by_class_name('gallery-list-item')
    # пока не появятся все товары, будем нажимать кнопку для прокрутки списка
    while len(items) < count_item:
        btn = new_item.find_elements_by_xpath(
            '//a[contains(@class,"next-btn c-btn c-btn_scroll-horizontal c-btn_icon i-icon-fl-arrow-right")]')
        btn[0].click()
        time.sleep(3)
        items = new_item.find_elements_by_class_name('gallery-list-item')
    products = information[0].find_elements_by_tag_name('li')
    list = []
    for one in products:
        product = one.find_element_by_tag_name('a')
        data_prod = json.loads(product.get_attribute('data-product-info'))
        data_prod['link'] = product.get_property('href')
        data_prod['img_link'] = product.find_element_by_tag_name(
            'img').get_attribute('src')
        data_prod['productPriceLocal'] = float(data_prod['productPriceLocal'])
        data_prod['data'] = datetime.datetime.now()
        list.append(data_prod)
    return list


# Сохраняем в БД
client = MongoClient('localhost', 27017)
db = client['hits_of_m-video']
hits = db.today_hits
hits.create_index('productId', unique=True)
count = 0  # счетчик уникальных товаров
total_count = 0  # счетчик скачаных товаров
for _ in _mvideo_parse():
    # обрабатываем ошибку дублирования индекса
    try:
        hits.insert_one(_)
        count += 1
        total_count += 1
    except pymongo.errors.DuplicateKeyError:
        total_count += 1

