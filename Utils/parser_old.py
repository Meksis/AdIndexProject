import selenium.webdriver as webdriver
from selenium.webdriver.common.by import By

import pandas as pd
import random
import datetime
import time
import requests
from statistics import median

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





def parse_some_news(driver : webdriver.Firefox = None, days4parse : int = 1) -> pd.DataFrame: # type: ignore
    if not driver:
        driver = webdriver.Firefox()

    days_iterated = 0
    button_clicked = 0
    posts_total_info = []
    date_prev = ''
    posts_datas = []

    driver.get(main_url)

    while days_iterated != days4parse:
        print(days_iterated, '\n', posts_datas)

        if isinstance(posts_datas, list):
            posts_cards = driver.find_elements(By.CLASS_NAME, 'newsfeed__list-item ')
        
        else:
            posts_cards = driver.find_elements(By.CLASS_NAME, 'newsfeed__list-item ')[posts_datas.post_id.size * button_clicked : ]


        posts_datas = []

        for element in posts_cards:
            link = element.find_element(By.CLASS_NAME, 'newsfeed__list-item-title').find_element(By.TAG_NAME, 'a').get_attribute('href')
            
            footer_object = element.find_element(By.CLASS_NAME, 'newsfeed__list-footer')
            tag = footer_object.find_element(By.TAG_NAME, 'a').text
            date = footer_object.find_element(By.TAG_NAME, 'span').text.split(' | ')
            date = date[0] if len(date[0]) > len(date[1]) else date[1]
            date = '.'.join(date.split('.')[ : -1]) + '.20' + date.split('.')[-1]


            id = link[link.index('.phtml') - 6 : link.index('.phtml')]



            posts_datas.append({
                'date' : date,
                'author' : random.choice(authors_names),            # Позже заменить
                # 'visitors' : random.randint(100, 20000),          # Тестовый вариант
                # 'visitors' : 0,                                     # Заглушка
                'post_tag' : tag,
                'post_id' : id,
                'link' : link
            })
            
            # posts_datas[-1].update({'views' : random.randint(round(posts_datas[-1]['visitors']), round(posts_datas[-1]['visitors'] + posts_datas[-1]['visitors'] * .5))})

            if not date_prev:
                date_prev = str(date)
            
            else:
                if date != date_prev:
                    date_prev = str(date)
                    days_iterated += 1


        posts_datas = pd.DataFrame.from_dict(posts_datas)

        if isinstance(posts_total_info, list):
            posts_total_info = posts_datas.copy()

        else:
            posts_total_info = pd.concat([posts_total_info, posts_datas], ignore_index = True)


        show_more_button = driver.find_element(By.CLASS_NAME, 'js-load-news')
        show_more_button.click()
        button_clicked += 1

        time.sleep(1)

    
    date_changed = False

    while not date_changed:
        posts_cards = driver.find_elements(By.CLASS_NAME, 'newsfeed__list-item ')[posts_datas.post_id.size * button_clicked : ]


        posts_datas = []

        for element in posts_cards:
            link = element.find_element(By.CLASS_NAME, 'newsfeed__list-item-title').find_element(By.TAG_NAME, 'a').get_attribute('href')
            
            footer_object = element.find_element(By.CLASS_NAME, 'newsfeed__list-footer')
            tag = footer_object.find_element(By.TAG_NAME, 'a').text
            date = footer_object.find_element(By.TAG_NAME, 'span').text.split(' | ')
            date = date[0] if len(date[0]) > len(date[1]) else date[1]
            date = '.'.join(date.split('.')[ : -1]) + '.20' + date.split('.')[-1]

            

            id = link[link.index('.phtml') - 6 : link.index('.phtml')]

            # print(date, id)
            

            posts_datas.append({
                'date' : date,
                'author' : random.choice(authors_names),
                # 'visitors' : random.randint(100, 20000),
                'post_tag' : tag,
                'post_id' : id,
                'link' : link
            })
            
            # posts_datas[-1].update({'views' : random.randint(round(posts_datas[-1]['visitors']), round(posts_datas[-1]['visitors'] + posts_datas[-1]['visitors'] * .5))})
            
            if date != date_prev:
                date_prev = str(date)
                date_changed = True


        posts_datas = pd.DataFrame.from_dict(posts_datas)
        # posts_datas.date = pd.to_datetime(posts_datas.date, format='%d.%m.%y')

        posts_datas = posts_datas[posts_datas.date != date]

        if isinstance(posts_total_info, list):
            posts_total_info = posts_datas.copy()

        else:
            posts_total_info = pd.concat([posts_total_info, posts_datas], ignore_index = True)


        show_more_button = driver.find_element(By.CLASS_NAME, 'js-load-news')
        show_more_button.click()
        button_clicked += 1

        time.sleep(1)
        
    
    driver.close()
    
    posts_total_info.date = pd.to_datetime(posts_total_info.date, dayfirst=True, format='%d.%m.%Y')


    posts_total_info.to_csv(f'csvs/AdIndex main news {datetime.datetime.today().strftime("%Y-%m-%d")} - {days4parse} days.csv')
    return(posts_total_info)




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
