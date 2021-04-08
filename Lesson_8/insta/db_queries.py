'''
3) Собранные данные необходимо сложить в базу данных. Структуру данных нужно заранее продумать, чтобы:
4) Написать запрос к базе, который вернет список подписчиков только указанного пользователя
5) Написать запрос к базе, который вернет список профилей, на кого подписан указанный пользователь

Название: "insta"
Коллекция: "instacom"
Поля документов:
  _id : уникальный индекс МонгоДБ,
  main_acc_name : никнейм пользователя для которого собирались подписки
  и подписчики(таргет-пользователь),
  status_name : статус взаимоотношений с таргет-пользователем(подписчик
  или подписка),
  user_id : id подписчика/подписки,
  user_name : никнейм подписчика/подписки,
  user_full_name : полное имя подписчика/подписки,
  avatar : ссылка на аватар подписчика/подписки,
  user_data : ссылка на аватар подписчика/подписки

'''

from pymongo import MongoClient
# from pprint import pprint

client = MongoClient('localhost', 27017)
db = client['insta']
users = db.instacom

# подписчики
def get_followers_list(username):
    result = users.find({'$and': [{'main_acc_name': username},
                                  {'status_name': 'follower'}]},
                        {'user_name': True, '_id': False})

    return [name['user_name'] for name in result]

# pprint(get_followers_list('_aleksandra_nikitina__'))

# подписки
def get_following_profile_list(username):
    result = users.find({'$and': [{'main_acc_name': username},
                                  {'status_name': 'following'}]},
                        {'user_data': {'id': True, 'username': True,
                                       'full_name': True, 'is_private': True},
                         '_id': False})

    return [name['user_data'] for name in result]

# pprint(get_following_profile_list('_aleksandra_nikitina__'))
