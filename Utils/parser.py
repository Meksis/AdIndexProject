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
        
        posts_datas[-1].update({'views' : random.randint(round(posts_datas[-1]['visitors']), round(posts_datas[-1]['visitors'] + posts_datas[-1]['visitors'] * .5))})
    
    driver.close()

    posts_datas = pd.DataFrame(posts_datas)
    posts_datas['date'] = pd.to_datetime(posts_datas['date'], format='mixed')

    posts_datas.to_csv(f'AdIndex main news {date}')
    return(posts_datas)

import requests


def get_data_from_url(url: str ):
    params = {
        'ids': '22386646',
        # 'metrics': 'ym:s:visits,ym:s:pageviews,ym:s:users,ym:s:bounceRate,ym:s:pageDepth,ym:s:avgVisitDurationSeconds',
        'metrics': 'ym:s:pageviews',  # Метрика для просмотров страниц
        'dimensions': 'ym:s:referer',  # Размерность для получения ссылок
        'date1': 'today',  # 7daysAgo за неделю, 30daysAgo за месяц, 365daysAgo за год
        'date2': 'today',
        'filters': f"ym:pv:URL=='{url}'"
    }

    url = 'https://api-metrika.yandex.net/stat/v1/data'


    headers = {
        'Authorization': 'OAuth y0_AgAAAABxT5u9AArjtwAAAADzHTIKv-VGe5uzTHqKqd3WWTTeIiZQ2WU',
    }

    response = requests.get(url, headers=headers, params=params )
    return response.json()

