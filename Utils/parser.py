import selenium.webdriver as webdriver
from selenium.webdriver.common.by import By

import pandas as pd
import random
import datetime
import time


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
                'author' : random.choice(authors_names),
                'visitors' : random.randint(100, 20000),
                'post_tag' : tag,
                'post_id' : id,
                'link' : link
            })
            
            posts_datas[-1].update({'views' : random.randint(round(posts_datas[-1]['visitors']), round(posts_datas[-1]['visitors'] + posts_datas[-1]['visitors'] * .5))})

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
                'visitors' : random.randint(100, 20000),
                'post_tag' : tag,
                'post_id' : id,
                'link' : link
            })
            
            posts_datas[-1].update({'views' : random.randint(round(posts_datas[-1]['visitors']), round(posts_datas[-1]['visitors'] + posts_datas[-1]['visitors'] * .5))})
            
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


    posts_total_info.to_csv(f'AdIndex main news {datetime.datetime.today().strftime("%Y-%m-%d")} - {days4parse} days.csv')
    return(posts_total_info)