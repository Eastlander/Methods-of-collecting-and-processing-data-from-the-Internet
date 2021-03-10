'''
2. Изучить список открытых API (https://www.programmableweb.com/category/all/apis).
Найти среди них любое, требующее авторизацию (любого типа).
Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.

Если нет желания заморачиваться с поиском, возьмите API вконтакте (https://vk.com/dev/first_guide).
Сделайте запрос, чтобы получить список всех сообществ на которые вы подписаны.
'''

# Тут я решил пойти по более простому пути, т.к. был ограничен во времени + решил, что это в будущем может пригодиться

# access_token=2b1d954236b68015ec94a0be8265c67565316b6ec987b78a1d3292e65c02096b549821b5d5cea05b9b744
# https://api.vk.com/method/groups.get?user_id=57263194&access_token=2b1d954236b68015ec94a0be8265c67565316b6ec987b78a1d3292e65c02096b549821b5d5cea05b9b744&v=5.52

import requests
import json
from pprint import pprint

main_link = 'https://api.vk.com/method/groups.get'
params = {'user_id':'5126277',
          'access_token':'0d58da95e64953e92739620831be68b4c3a1945e832655eac70b57363667a6eda20ab7504e4817fe04cb3',
          'v':'5.52'}

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'}
response = requests.get(main_link, params=params, headers=headers)
j_body = response.json()

pprint(j_body)

with open('vk_groups_id.json', 'w') as f:
    json.dump(response.json(), f)