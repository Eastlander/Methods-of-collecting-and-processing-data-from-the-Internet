'''
Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы) с сайтов Superjob и HH.
Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы).
Получившийся список должен содержать в себе минимум:
* Наименование вакансии.
* Предлагаемую зарплату (отдельно минимальную, максимальную и валюту).
* Ссылку на саму вакансию.
* Сайт, откуда собрана вакансия.

По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение).
Структура должна быть одинаковая для вакансий с обоих сайтов. Общий результат можно вывести с помощью dataFrame через pandas.
'''

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from pprint import pprint


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

#pprint(hh_parser('продавец'))

df = pd.DataFrame(hh_parser('продавец'))
pprint(df)
df.to_csv('hh_parser_result.csv', sep='\t', encoding='utf-8')
