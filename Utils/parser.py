import selenium.webdriver as webdriver
from selenium.webdriver.common.by import By

import pandas as pd
import random
import datetime

from dateutil.parser import parse as parser

import time
import requests
from statistics import median


# pd.set_option('display.max_rows', None)

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


def get_post_data(post_card_object):
    link = post_card_object.find_element(By.CLASS_NAME, 'newsfeed__list-item-title').find_element(By.TAG_NAME, 'a').get_attribute('href')

    footer_object = post_card_object.find_element(By.CLASS_NAME, 'newsfeed__list-footer')
    tag = footer_object.find_element(By.TAG_NAME, 'a').text
    publication_datas = footer_object.find_element(By.TAG_NAME, 'span').text.split(' | ')
    date = publication_datas[0] if len(publication_datas[0]) > len(publication_datas[1]) else publication_datas[1]
    time = publication_datas[1] if len(publication_datas[0]) > len(publication_datas[1]) else publication_datas[0]

    publicated_at = parser(f'{date} {time}', dayfirst=True)

    del time, publication_datas, footer_object

    id = link[link.index('.phtml') - 6 : link.index('.phtml')]


    return(pd.DataFrame(
            [
                {
                'date' : publicated_at,
                'author' : random.choice(authors_names),        # Заглушка
                'post_tag' : tag,
                'post_id' : id,
                'link' : link
                }
            ]
        ),
        publicated_at
    )


def parse_some_news(date_from : datetime.date, date_to : datetime.date, driver : webdriver.Firefox = None) -> pd.DataFrame:
    if not driver:
        driver = webdriver.Firefox()

    driver.get(main_url)

    parsed_datas = pd.DataFrame()

    posts_cards = driver.find_elements(By.CLASS_NAME, 'newsfeed__list-item')
    continue_search = True
    checked_rounds = 0

    while continue_search:
        for post_card in posts_cards:
            parsed_data, post_date = get_post_data(post_card)
            date = datetime.date(post_date.year, post_date.month, post_date.day)

            if date <= date_to and date >= date_from:
                parsed_datas = pd.concat([parsed_datas, parsed_data], ignore_index = True)

            else:
                continue_search = False
                break
            

        checked_rounds += 1

        next_button = driver.find_element(By.CLASS_NAME, 'mb-xl-0')
        next_button.click()

        time.sleep(0.25)


        posts_cards = driver.find_elements(By.CLASS_NAME, 'newsfeed__list-item')

        posts_cards = posts_cards[16 * checked_rounds: ]

    driver.close()


    
    return(parsed_datas)





def get_data_from_url(url: str, days_from : str = "yesterday", days_to : str = "today"):
    params = {
        'ids': '22386646',
        # 'metrics': 'ym:s:visits,ym:s:pageviews,ym:s:users,ym:s:bounceRate,ym:s:pageDepth,ym:s:avgVisitDurationSeconds',
        # 'metrics': 'ym:s:pageviews',  # Метрика для просмотров страниц
        'metrics': 'ym:s:visits,ym:s:pageviews,ym:s:users,ym:s:bounceRate,ym:s:pageDepth,ym:s:avgVisitDurationSeconds',
        'dimensions': 'ym:s:refererDomain',  # Размерность для получения ссылок
        'date1': days_from,  # 7daysAgo за неделю, 30daysAgo за месяц, 365daysAgo за год
        'date2': days_to,
        'filters': f"ym:pv:URL=='{url}'"
    }

    api_url = 'https://api-metrika.yandex.net/stat/v1/data'


    headers = {
        'Authorization': 'OAuth y0_AgAAAABxT5u9AArjtwAAAADzHTIKv-VGe5uzTHqKqd3WWTTeIiZQ2WU',
    }

    response = requests.get(api_url, headers=headers, params=params ).json()

    if not response['data']:
        return response, url


    page_metrics = []
    response_data = response['data']
    names = ['Посетители', "Читатели", "Уникальные пользователи", "% недочитываемости", "Глубина просмотра", "Ср. время на сайте (сек)"]


    for data in response_data:
        page_metrics.append(
            {
                'Сайт' : data['dimensions'][0]['name']
            }
        )

        for counter, metric_name in enumerate(names):
            page_metrics[-1].update(
                {
                    metric_name : data['metrics'][counter]
                }
            )
    out = [{}, {}, {'% недочитываемости' : [], 'Глубина просмотра' : [], "Ср. время на сайте (сек)"  : []}]

    restrict_keys = ['Сайт', '% недочитываемости', 'Глубина просмотра', "Ср. время на сайте (сек)"]


    for data in page_metrics:
        if 'telegram' not in data['Сайт']:
            if out[0]:
                out[0].update(
                    {
                        key : out[0][key] + data[key] for key in list(data.keys())[ : -3][1 :]
                    } 
                )
            
            else:
                for key in data:
                    if key != 'Сайт':
                        out[0][key] = data[key]


            for key in restrict_keys[1 :]:
                out[2][key].append(data[key])

        else:
            for key in data:
                if key != 'Сайт':
                    out[1][key] = round(data[key], 2)

    for key in out[2]:
        out[0][key] = median(out[2][key])

    del out[2]


    out[0] = {
        'Поисковые системы' : out[0]
    }

    out[1] = {
        'Telegram' : out[1]
    }

    totals = {}

    print(out, '\n')

    if out[1]['Telegram']:
        totals.update(
            {
                key : out[0]['Поисковые системы'][key] + out[1]['Telegram'][key]
                for key in list(out[0]['Поисковые системы'].keys())[ : 3]
            }
        )

        totals.update(
            {
                key : median([out[0]['Поисковые системы'][key], out[1]['Telegram'][key]])
                for key in list(out[0]['Поисковые системы'].keys())[3 :]
            }
        )

    else:
        totals.update(
            out[0]['Поисковые системы']
        )

    totals.update({'link' : url})
    # return response.json()
    return out, totals

