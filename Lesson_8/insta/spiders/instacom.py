'''
1)Написать приложение, которое будет проходиться по указанному списку двух и/или более пользователей
    и собирать данные об их подписчиках и подписках.
2) По каждому пользователю, который является подписчиком или на которого подписан исследуемый объект
    нужно извлечь имя, id, фото (остальные данные по желанию). Фото можно дополнительно скачать.

P.S.  Продолжение задания в db_quiries.py
'''




import scrapy
from scrapy.http import HtmlResponse
from insta.items import InstaItem
import re
import json
from urllib.parse import urlencode
from copy import deepcopy


class InstacomSpider(scrapy.Spider):
    name = 'instacom'
    allowed_domains = ['instagram.com']
    start_urls = ['http://instagram.com/']
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    inst_login = '+79776924830'
    inst_pass = '#PWD_INSTAGRAM_BROWSER:9:1617815606:AVdQABoL/cOaaLHlO91op+CK4sY0HLkg0bif1iMAnBo5FqQIqJpa9NGRUcet2yiV1L/eiCrlxQae5hy6UEWOwPV1iZsA3LKA4/iX+C3X1I6fqHho61+PtL026t+gH3QXqO985iLByIg0PQWo'
    parse_user = ['_aleksandra_nikitina__', 'qpaya__']  # список юзеров, чьих подписчиков и подписки необходимо собрать
    status_list = ['following', 'follower']  # список информации о таргет-пользователе, которую необходимо собрать
    # хэш-коды информации (о таргет-пользователе), которую собираем
    status_hash = ['3dec7e2c57367ef3da3d987d89f9dbc8',
                   '5aefa9893005572d237da5068082d8d5']
    graphql_url = 'https://www.instagram.com/graphql/query/'


    def parse(self, response: HtmlResponse):
        csrf_token = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(self.inst_login_link,
                                 method='POST',
                                 callback=self.user_login,
                                 formdata={'username': self.inst_login,
                                           'enc_password': self.inst_pass,
                                           'queryParams': {},
                                           'optIntoOneTap': 'false'},
                                 headers={'X-CSRFToken': csrf_token})

    def user_login(self, response: HtmlResponse):
        j_body = response.json()
        if j_body.get('authenticated'):
            for name in self.parse_user:
                yield response.follow(
                    f'/{name}/',
                    callback=self.user_data_parse,
                    cb_kwargs={'username': deepcopy(name)}
                )

    '''
    для каждого таргет-пользователя будем разделять
    запросы на сбор данных по подпискам и подписчикам
    '''
    def user_data_parse(self, response: HtmlResponse, username):
        person_id = self.fetch_person_id(response.text, username)
        variables = {'id': person_id,
                     "include_reel": 'true',
                     "fetch_mutual": 'false',
                     'first': 24}
        for status_name, target_hash, method in zip(self.status_list,
                                                    self.status_hash,
                                                    [self.following_parse,
                                                     self.follower_parse]):
            url_post = f'{self.graphql_url}?query_hash={target_hash}&{urlencode(variables)}'

            yield response.follow(url_post,
                                  callback=method,
                                  cb_kwargs={'variables': deepcopy(variables),
                                             'username': username,
                                             'status_name': status_name,
                                             'target_hash': target_hash})

    # подписки
    def following_parse(self, response: HtmlResponse, variables, username,
                        status_name, target_hash):
        j_son = json.loads(response.text)
        page_info = j_son.get('data').get('user').get(
            'edge_follow').get('page_info')
        if page_info.get('has_next_page'):
            variables.update({'after': page_info.get('end_cursor')})
            url_post = f'{self.graphql_url}?query_hash={target_hash}&{urlencode(variables)}'
            yield response.follow(url_post,
                                  callback=self.following_parse,
                                  cb_kwargs={'variables': variables,
                                             'username': username,
                                             'status_name':
                                                 status_name,
                                             'target_hash':
                                                 target_hash})
        followings = j_son.get('data').get('user').get('edge_follow').get(
            'edges')
        for following in followings:
            yield InstaItem(
                status_name=status_name,
                main_acc_name=username,
                user_id=following.get('node').get('id'),
                user_name=following.get('node').get('username'),
                user_full_name=following.get('node').get('full_name'),
                avatar=following.get('node').get('profile_pic_url'),
                user_data=following.get('node')
            )

    # подписчики
    def follower_parse(self, response: HtmlResponse, variables, username,
                       status_name, target_hash):
        j_son = json.loads(response.text)
        page_info = j_son.get('data').get('user').get(
            'edge_followed_by').get('page_info')
        if page_info.get('has_next_page'):
            variables.update({'after': page_info.get('end_cursor')})
            url_post = f'{self.graphql_url}?query_hash={target_hash}&{urlencode(variables)}'
            yield response.follow(url_post,
                                  callback=self.follower_parse,
                                  cb_kwargs={'variables': variables,
                                             'username': username,
                                             'status_name': status_name,
                                             'target_hash': target_hash})
        followers = j_son.get('data').get('user').get(
            'edge_followed_by').get('edges')
        for follower in followers:
            yield InstaItem(
                status_name=status_name,
                main_acc_name=username,
                user_id=follower.get('node').get('id'),
                user_name=follower.get('node').get('username'),
                user_full_name=follower.get('node').get('full_name'),
                avatar=follower.get('node').get('profile_pic_url'),
                user_data=follower.get('node')
            )

    # получение токена для авторизации
    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    # Получение id желаемого пользователя
    def fetch_person_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')