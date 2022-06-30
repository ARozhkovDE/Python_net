#1. Посмотреть документацию к API GitHub, 
#разобраться как вывести список репозиториев для конкретного пользователя, 
#сохранить JSON-вывод в файле *.json.


import requests
import json

user = 'ARozhkovDE'
url = f'https://api.github.com/users/{user}/repos'

response = requests.get(url).json()
with open(f'{user}_repos.json', 'w') as outfile:
    for elem in range(len(response)):
        json.dump((response[elem]).get('name'), outfile)
        outfile.write('\n')

