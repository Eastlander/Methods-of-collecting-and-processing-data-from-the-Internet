'''
1. Посмотреть документацию к API GitHub,
разобраться как вывести список репозиториев для конкретного пользователя,
сохранить JSON-вывод в файле *.json.
'''

import requests
from json import dump

while True:
    user_input = input('Are you looking for repository of user or organization? (u/o)\n').lower()
    if user_input == 'u':
        id = input('Enter GitHub`s name: ')
        url = f"https://api.github.com/users/{id}/repos"
        break
    if user_input == 'o':
        id = input('Enter GitHub`s name: ')
        url = f"https://api.github.com/orgs/{id}/repos"
        break
    else:
        print("Access denied! Try again.")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
    "Accept": "application/json"
}

repo = requests.get(url, headers=headers)

if repo.ok:
    path = f"looking.{id}_repos.json"
    with open(path, "w") as f:
        dump(repo.json(), f)

for i in repo.json():
    print(i['name'])