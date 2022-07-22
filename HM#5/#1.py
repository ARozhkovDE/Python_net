# Написать программу, которая собирает входящие письма из своего или
# тестового почтового ящика и сложить данные о письмах в базу данных
# (от кого, дата отправки, тема письма, текст письма полный)
# Логин тестового ящика: study.ai_172@mail.ru
# Пароль тестового ящика: NextPassword172#


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import time
import pymongo
from pymongo import MongoClient
import requests
from lxml import html
from pymongo import errors
from pprint import pprint
from selenium. webdriver. chrome. options import Options

client = MongoClient('127.0.0.1', 27017)
db = client['Mail']
Mail_db = db.Mail_db
Mail_db.delete_many({})

s = Service('./chromedriver')
driver = webdriver.Chrome(service=s)
driver.maximize_window()

driver.get('https://account.mail.ru/login')

login = driver.find_element(By.XPATH, '//html//input[@name="username"]')
login.send_keys("study.ai_172@mail.ru")

submit = driver.find_element(By.XPATH, '//button[@type="submit"]')
submit.click()

passwd = driver.find_element(By.XPATH, '//input[@name="password"]')
time.sleep(2)
passwd.send_keys("NextPassword172#")

submit = driver.find_element(By.XPATH, '//button[@type="submit"]')
submit.click()
time.sleep(2)

href_check = set()

time.sleep(2)
mail_count = int(driver.find_element(By.XPATH, '//a[@class = "nav__item js-shortcut nav__item_active nav__item_shortcut nav__item_child-level_0"]').get_attribute('title').split()[1])


for i in range(mail_count//10):
    articles = driver.find_elements(By.XPATH, '//a[@tabindex]')
    for article in articles:
        href_check.add(article.get_attribute('href').split('?')[0])
    actions = ActionChains(driver)
    actions.move_to_element(articles[-1])
    actions.perform()

news = []
for href in href_check:
    all_news = {}
    driver.get(href)
    time.sleep(1)
    all_news['date'] = driver.find_element(By.XPATH, '//div[@class = "letter__date"]').text
    all_news['title'] = driver.find_element(By.XPATH, '//h2[@class = "thread-subject"]').text
    all_news['letter_autor'] = driver.find_element(By.XPATH, '//div[@class = "letter__author"]//span[@class = "letter-contact"]').text
    all_news['body'] = driver.find_element(By.XPATH, '//div[@class = "letter__body"]').text
    Mail_db.insert_one({'date': all_news['date'], 'title': all_news['title'], 'letter_autor': all_news['letter_autor'], 'body': all_news['body']})







