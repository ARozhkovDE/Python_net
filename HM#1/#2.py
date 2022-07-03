#2. Изучить список открытых API (https://www.programmableweb.com/category/all/apis). 
#Найти среди них любое, требующее авторизацию (любого типа). 
#Выполнить запросы к нему, пройдя авторизацию. 
#Ответ сервера записать в файл.

import requests
from token_github import token

url = 'https://api.github.com/user/repos'
headers = {'Authorization': f'token {token}',
           'Accept': 'application/vnd.github.v3+json'
           }

data = '{"name": "API_test"}'

response = requests.post(url, headers=headers, data=data)
with open('Github_resp.txt', 'w') as outfile:
    outfile.write(str(response.status_code))
