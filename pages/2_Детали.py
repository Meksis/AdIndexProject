import streamlit as st
import pandas as pd
import plotly.express as px

import datetime

from Utils.parser import *


def refresh_datas(date_from : datetime.date, date_to : datetime.date, csv_save_path : str):
    st.session_state['datas'] = parse_some_news(date_from, date_to, csv_save_path)

def refresh_metrics(csv_save_path):
    datas = st.session_state['datas']
    datas_metrics = pd.DataFrame()

    # if os.path.exists(csv_save_path):
    #     loaded_df = pd.read_csv(csv_save_path, index_col=0)
    #     differences = pd.merge(datas, loaded_df, 'left')
    #     st.write(differences)


    #     for link in differences.link:
    #         datas_metrics = pd.concat([datas_metrics, pd.DataFrame([get_data_from_url(link)[1]])])


    # else:
    #     for link in datas.link:
    #         datas_metrics = pd.concat([datas_metrics, pd.DataFrame([get_data_from_url(link)[1]])])
    
    for link in datas.link:
        datas_metrics = pd.concat([datas_metrics, pd.DataFrame([get_data_from_url(link)[1]])])

    
    datas.date = pd.to_datetime(datas.date)
    merged = pd.concat([datas.merge(datas_metrics, how='inner', on='link'), pd.DataFrame([{'Copyright' : None}])])
    

    st.session_state['datas_full'] = merged
    st.session_state['datas_full'].to_csv(csv_save_path)


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
        
        try:
            refresh_datas(selected_date[1], selected_date[0], f'./csvs/AdIndex news {selected_date[0]}__{selected_date[1]}.csv')
            refresh_metrics(f'./csvs/AdIndex news metrics {selected_date[0]}__{selected_date[1]}.csv')
        
        except:
            pass




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
                refresh_datas(selected_date[1], selected_date[0], f'./csvs/AdIndex news {selected_date[0]}__{selected_date[1]}.csv')
                refresh_metrics(f'./csvs/AdIndex news metrics {selected_date[0]}__{selected_date[1]}.csv')
        

if 'datas_full' in st.session_state:
    st.write(st.data_editor(st.session_state['datas_full'], disabled=st.session_state['datas_full'].columns[ : -1]))
    