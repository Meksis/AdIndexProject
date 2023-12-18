import streamlit as st
import pandas as pd
import plotly.express as px

import datetime

from Utils.parser_old import *


def refresh_datas(parse_days : int = 1):
    datas = parse_some_news(days4parse=parse_days)
    st.session_state['datas'] = datas


def refresh_metrics():
    datas = st.session_state['datas']
    datas_metrics = pd.DataFrame()

    
    for link in datas.link:
        datas_metrics = pd.concat([datas_metrics, pd.DataFrame([get_data_from_url(link)[1]])])

    st.session_state['datas_full'] = datas.merge(datas_metrics, how='inner', on='link')
    st.session_state['datas_full'].to_csv(f'AdIndex main news METRICS {datetime.datetime.today().strftime("%Y-%m-%d")}.csv')


if 'datas_full' not in st.session_state:
    if 'picked_dates' in st.session_state:
        selected_date = st.date_input(      # Создаем поле для ввода даты, задавая размеры от минимальной даты в датафрейме до текущей и выставляя значение от текущей недели до 7 дней назад
            "Выберете промежуток выборки",
            (
                st.session_state['picked_dates'][0],
                st.session_state['picked_dates'][1]
            ),
            st.session_state['picked_dates'][0],
            st.session_state['picked_dates'][1],

            format="YYYY.MM.DD",
            key='datepick_details_page'
        )

        refresh_datas((selected_date[1] - selected_date[0]).days)
        refresh_metrics()




    else:
        today = datetime.datetime.now()
        selected_date = st.date_input(      # Создаем поле для ввода даты, задавая размеры от минимальной даты в датафрейме до текущей и выставляя значение от текущей недели до 7 дней назад
            "Выберете промежуток выборки",
            (
                datetime.date(today.year, today.month, today.day - 7 if today.day - 7 > 0 else 1),
                today
            ),
            datetime.date(today.year, today.month, today.day - 7 if today.day - 7 > 0 else 1),
            # data.date.iloc[-1],
            today,
            format="YYYY.MM.DD",
            key='scatter_datepick'
        )

        if st.button('Ок'):
            st.session_state['picked_dates'] = selected_date

            with st.spinner('Получаем данные'):
                refresh_datas((selected_date[1] - selected_date[0]).days)
                refresh_metrics()
        
            st.write(st.session_state['datas_full'])
        # refresh_datas((st.session_state['picked_dates'][1] - st.session_state['picked_dates'][0]).days)

else:
    st.write(st.session_state['datas_full'])
    