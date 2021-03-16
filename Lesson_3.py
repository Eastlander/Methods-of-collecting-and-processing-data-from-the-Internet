'''
1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB
и реализовать функцию, записывающую собранные вакансии (из предыдущего задания) в созданную БД.
'''

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from pprint import pprint
from pymongo import MongoClient


def hh_parser(vac):
    main_link = 'https://hh.ru/search/vacancy'
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'
    }

    df = pd.DataFrame(columns=('Вакансия', 'Ссылка', 'Мин. з/п', 'Макс. з/п', 'Валюта', 'Источник'))

    for i in range(100):
        params = {
            'st': 'searchVacancy', \
            'text': vac, \
            'search_field': 'name', \
            'search_period': '7', \
            'items_on_page': '50', \
            'page': i
        }

        response = requests.get(main_link, params=params, headers=headers)

        if response.ok:
            soup = bs(response.text, 'html.parser')
            vacancy1 = soup.find('div', {'class': 'vacancy-serp-item'})
            div_on_page = len(soup.find('div', {'class': "vacancy-serp"}))
            vacancy_site_link = 'https://hh.ru/'

            for i in range(div_on_page):
                try:
                    # Название вакансии
                    vacancy_name = vacancy1.find('span', {'class': 'g-user-content'}).text

                    # Ссылка на вакансию
                    vacancy_link = vacancy1.find('span', {'class': 'g-user-content'})
                    vacancy_link = vacancy_link.next['href']

                    # З/п
                    vacancy_salary = vacancy1.find('div', {'class': 'vacancy-serp-item__sidebar'}).next.text
                    vacancy_salary = vacancy_salary.replace('\xa0', '')
                    vacancy_salary = vacancy_salary.replace(' ', '-')
                    vacancy_salary = vacancy_salary.split('-')
                    vacancy_salary_min = vacancy_salary[0]
                    vacancy_salary_max = vacancy_salary[1]
                    vacancy_salary_currency = vacancy_salary[2]

                    try:
                        vacancy_salary_min = int(vacancy_salary_min)
                    except:
                        vacancy_salary_min = float('NaN')

                    try:
                        vacancy_salary_max = int(vacancy_salary_max)
                    except:
                        vacancy_salary_max = float('NaN')

                    if vacancy_salary_currency == ('руб.'):
                        vacancy_salary_currency = 'RUB'
                    elif vacancy_salary_currency == ('EUR'):
                        vacancy_salary_currency = 'EUR'
                    elif vacancy_salary_currency == ('USD'):
                        vacancy_salary_currency = 'USD'
                    else:
                        vacancy_salary_currency = float('NaN')

                    df = df.append(
                        {
                            'Вакансия': vacancy_name,
                            'Ссылка': vacancy_link,
                            'Мин. з/п': vacancy_salary_min,
                            'Макс. з/п': vacancy_salary_max,
                            'Валюта': vacancy_salary_currency,
                            'Источник': vacancy_site_link,
                        },
                        ignore_index=True,
                    )
                    vacancy1 = vacancy1.next_sibling
                except:
                    vacancy1 = vacancy1.next_sibling
        if soup.find('a', {'class': 'HH-Pager-Controls-Next'}) == None:
            break
    return df

# df = pd.DataFrame(hh_parser('продавец'))
# pprint(df)
# df.to_csv('hh_parser_result.csv', sep='\t', encoding='utf-8')

pprint(hh_parser('продавец'))

client = MongoClient('localhost', 27017)
db = client['Vacancies']

df = hh_parser('продавец')
df.rename(columns={'Вакансия':'vacancy',
                   'Ссылка':'link',
                   'Мин. з/п':'minsalary',
                   'Макс. з/п':'maxsalary',
                   'Валюта':'currency_unit',
                   'Источник':'source'}, inplace=True)
print(df)

df_dict = df.to_dict('register')
db.vacancies.insert_many(df_dict)

'''
2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы.
'''

# ВЫСКАКИВАЕТ ОШИБКА. Разобраться!
# import warnings

a = 0
while a == 0:
    try:
        salary = float(input('Введите минимальную желаемую зарплату: '))
        a += 1
    except:
        print('Вы ввели некорректные символы! Попробуйте ещё раз.')

gt_salary = db.vacancies.find({'maxsalary': {'$gt': salary} })
for i in gt_salary:
    pprint(i)

'''
3. Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта.
'''

objects = db.vacancies.find({}).limit(1)
for obj in objects:
    pprint(obj)

df = hh_parser('продавец')
df.rename(columns={'Вакансия':'vacancy',
                   'Ссылка':'link',
                   'Мин. з/п':'minsalary',
                   'Макс. з/п':'maxsalary',
                   'Валюта':'currency_unit',
                   'Источник':'source'}, inplace=True)

print(df)

df_dict_for_updates = df.to_dict('register')

for i in df_dict_for_updates:
    db.vacancies.update_one({'link': i['link']},
                                 {'$set': {'vacancy': i['vacancy'],
                                            'link': i['link'],
                                            'minsalary': i['minsalary'],
                                            'maxsalary': i['maxsalary'],
                                            'currency_unit': i['currency_unit'],
                                            'source': i['source']},},
                            upsert=True)

objects = db.vacancies.find({}).limit(3)
for obj in objects:
    pprint(obj)