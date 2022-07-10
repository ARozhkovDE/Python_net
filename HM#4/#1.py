# Написать приложение, которое собирает основные новости с сайта на выбор news.mail.ru, lenta.ru, yandex-новости.
# Для парсинга использовать XPath. Структура данных должна содержать:
# название источника;
# наименование новости;
# ссылку на новость;
# дата публикации.
# Сложить собранные новости в БД

import pymongo
from pymongo import MongoClient
import requests
from lxml import html
from pymongo import errors
from pprint import pprint

client = MongoClient('127.0.0.1', 27017)
db = client['News_db']
news_db = db.news_db
news_db.delete_many({})
url = 'https://news.mail.ru/'
params = {}
headers = {'User-agent': 'Mozilla/5.0'}
session = requests.Session()

response = session.get(url, params=params, headers=headers)
dom = html.fromstring(response.text)
items = dom.xpath(
    ".//ul[@class='list list_type_square list_half js-module']//li[@class='list__item hidden_medium hidden_large'] "
    "|"
    " .//ul[@class='list list_type_square list_half js-module']//li[@class='list__item']")


def get_datetime_from_href(href):
    response_inside = session.get(href, params=params, headers=headers)
    dom_inside = html.fromstring(response_inside.text)
    return dom_inside.xpath(".//span[@class='note__text breadcrumbs__text js-ago']//@datetime")


for item in items:
    news_dict = {}
    news = item.xpath(".//a[@class='list__text']//text()")[0]
    href = item.xpath(".//a[@class='list__text']//@href")[0]

    if len(href) > 0:
        publication_time = get_datetime_from_href(href)
        news_dict['news'] = news
        news_dict['href'] = href
        news_dict['publication_time'] = publication_time[0]
        news_dict['source'] = 'mail.news'
        news_db.insert_one(news_dict)


main_news = dom.xpath(".//td[@class='daynews__main']//span//text()")[0]
main_href = dom.xpath(".//td[@class='daynews__main']//@href")[0]
main_time = get_datetime_from_href(main_href)[0]
news_db.insert_one({'news': main_news, 'href': main_href, 'publication_time': main_time, 'source': 'mail.news'})


second_main_news = dom.xpath(".//td[@class='daynews__items']//div[@class='daynews__item']")
for item in second_main_news:
    news_dict = {}
    news = item.xpath(".//span//text()")[0]
    href = item.xpath(".//a//@href")[0]
    second_main_news = get_datetime_from_href(main_href)[0]
    news_db.insert_one({'news': news, 'href': href, 'publication_time': second_main_news, 'source': 'mail.news'})