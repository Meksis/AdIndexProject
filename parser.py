import selenium.webdriver as webdriver
from selenium.webdriver.common.by import By

import pandas as pd
import random


main_url = 'https://adindex.ru/news/all.phtml'
authors_names = [
    'Иванов Иван Иванович',
    'Петрова Мария Сергеевна',
    'Сидоров Антон Владимирович',
    'Андреева Анастасия Андреевна',
    'Борисова Ольга Борисовна',
    'Васильева Екатерина Васильевна',
    'Григорьева Людмила Григорьевна',
    'Данилова Светлана Викторовна',
    'Егорова Надежда Андреевна',
    'Жукова Ирина Ильинична'
]


def parse_some_news(driver : webdriver.Firefox = None) -> pd.DataFrame: # type: ignore
    if not driver:
        driver = webdriver.Firefox()


    driver.get(main_url)
    posts_cards = driver.find_elements(By.CLASS_NAME, 'newsfeed__list-item ')

    posts_links = [element.find_element(By.CLASS_NAME, 'newsfeed__list-item-title').find_element(By.TAG_NAME, 'a').get_attribute('href') for element in posts_cards]
    posts_tags = [element.find_element(By.CLASS_NAME, 'newsfeed__list-footer').find_element(By.TAG_NAME, 'a').text for element in posts_cards]
    posts_dates = [element.find_element(By.CLASS_NAME, 'newsfeed__list-footer').find_element(By.TAG_NAME, 'span').text.split(' | ')[0] for element in posts_cards]

    posts_datas = []

    for element in posts_cards:
        link = element.find_element(By.CLASS_NAME, 'newsfeed__list-item-title').find_element(By.TAG_NAME, 'a').get_attribute('href')
        
        footer_object = element.find_element(By.CLASS_NAME, 'newsfeed__list-footer')
        tag = footer_object.find_element(By.TAG_NAME, 'a').text
        date = footer_object.find_element(By.TAG_NAME, 'span').text.split(' | ')[0]

        id = link[link.index('.phtml') - 6 : link.index('.phtml')]


        posts_datas.append({
            'date' : date,
            'author' : random.choice(authors_names),
            'visitors' : random.randint(100, 20000),
            'post_tag' : tag,
            'post_id' : id,
            'link' : link
        })
    
    return(pd.DataFrame(posts_datas))