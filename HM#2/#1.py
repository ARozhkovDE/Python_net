# Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы получаем должность) с сайтов HH(обязательно) и/или Superjob(по желанию).
# Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы). Получившийся список должен содержать в себе минимум:
# Наименование вакансии.
# Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта. цифры преобразуем к цифрам).
# Ссылку на саму вакансию.
# Сайт, откуда собрана вакансия. (можно прописать статично hh.ru или superjob.ru)
# По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение).
# Структура должна быть одинаковая для вакансий с обоих сайтов.
# Общий результат можно вывести с помощью dataFrame через pandas. Сохраните в json либо csv.


import requests
from bs4 import BeautifulSoup
import pandas
from pprint import pprint


vacancy = 'Data engineer'
url = f'https://dolgoprudny.hh.ru/search/vacancy'
params = {'page': '2', 'text': f'{vacancy}', 'area': '1', 'items_on_page': 20}
headers = {'User-agent': 'Mozilla/5.0'}
session = requests.Session()

page = int(params['page'])

vacancy_list = []
while True:
    print(f'scrapping page {params["page"]}')
    response = session.get(url, params=params, headers=headers)
    dom = BeautifulSoup(response.text, 'html.parser')

    span = dom.find_all('a', {'class': 'bloko-button'})
    span_set = set()
    for span_elem in span:
        span_set.add(span_elem.text)

    vacancy_all = dom.find_all('div', {'class': 'vacancy-serp-item-body'})
    for vacancy_single in vacancy_all:

        vacancy_data = {}
        name = vacancy_single.find('a', {'data-qa': 'vacancy-serp__vacancy-title'}).text

        salary_text = vacancy_single.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
        salary_start = None
        salary_end = None
        salary_currency = None

        if not salary_text is None:
            salary_text = salary_text.text.replace('\u202f', '')
            salary_currency = salary_text[salary_text.rfind(' '): len(salary_text)]
            if salary_text[0:2] == 'от':
                salary_start = int(salary_text[3: salary_text.find(' ', salary_text.find(' ') + 1)])
            elif salary_text[0].isdigit():
                salary_start = int(salary_text[0: salary_text.find(' ')])
            elif salary_text[0:2] == 'до':
                salary_start = None
                salary_end = int(salary_text[3: salary_text.find(' ', salary_text.find(' ') + 1)])
            else:
                salary_start = None

            if salary_text.find('–') > 0:
                salary_end = int(salary_text.replace(salary_currency, '').replace(' ', '')[salary_text.find('–'): 1000])

        link = vacancy_single.find('a', {'data-qa': 'vacancy-serp__vacancy-title'}).get('href')
        href = link[:link.find('?')]
        company = vacancy_single.find('a', {'data-qa': 'vacancy-serp__vacancy-employer'}).text
        location = vacancy_single.find('div', {'data-qa': 'vacancy-serp__vacancy-address'}).text

        vacancy_data['name'] = name
        vacancy_data['salary_start'] = salary_start
        vacancy_data['salary_end'] = salary_end
        vacancy_data['salary_currency'] = salary_currency
        vacancy_data['href'] = href.replace('dolgoprudny.', '')
        vacancy_data['company'] = company
        vacancy_data['location'] = location
        vacancy_data['source'] = 'hh.ru'

        vacancy_list.append(vacancy_data)

    params['page'] = page + 1
    page = params['page']



    if 'дальше' not in span_set:
        break

pandas.set_option('display.max_columns', None)
pandas.set_option('display.expand_frame_repr', False)
df = pandas.DataFrame.from_dict(vacancy_list, orient='columns')
print(df)
with open(f'{vacancy}.csv', 'w') as outfile:
    outfile.write(str(df))


