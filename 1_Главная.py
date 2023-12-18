import streamlit as st
import pandas as pd
import plotly.express as px

import datetime

from Utils.parser_old import *
st.set_page_config(layout="wide", initial_sidebar_state='collapsed') # установка широкого расположения объектов
st.code(st.session_state)

def refresh_datas(parse_days : int = 1):
    st.session_state['datas'] = parse_some_news(days4parse=parse_days)


def refresh_metrics():
    datas = st.session_state['datas']
    datas_metrics = pd.DataFrame()

    
    for link in datas.link:
        datas_metrics = pd.concat([datas_metrics, pd.DataFrame([get_data_from_url(link)[1]])])

    st.session_state['datas_full'] = datas.merge(datas_metrics, how='inner', on='link')
    st.session_state['datas_full'].to_csv(f'AdIndex main news METRICS {datetime.datetime.today().strftime("%Y-%m-%d")}.csv')






today = datetime.datetime.now()

if 'picked_dates' not in st.session_state:
    st.session_state['picked_dates'] = [datetime.date(today.year, today.month, today.day - 7 if today.day - 7 > 0 else 1), today]
    

try:
    selected_date = st.date_input(      # Создаем поле для ввода даты, задавая размеры от минимальной даты в датафрейме до текущей и выставляя значение от текущей недели до 7 дней назад
        "Выберете промежуток выборки",
        (
            st.session_state['picked_dates'][0],
            st.session_state['picked_dates'][1]
        ),
        st.session_state['picked_dates'][0],
        st.session_state['picked_dates'][1],

        format="YYYY.MM.DD",
        key='datepick_main_page'
        )


except Exception as e:
    print(e)



if st.button('Обновить данные'):
    with st.spinner('Обновляемся'):
        st.session_state['picked_dates'] = selected_date
        refresh_datas((st.session_state['picked_dates'][1] - st.session_state['picked_dates'][0]).days)
        refresh_metrics()

        data = st.session_state['datas_full']





if 'datas_full' in st.session_state:
    data = st.session_state['datas_full']
    date_list = sorted(data['date'].unique())
    filtered_data = data[data['date'] <= pd.Timestamp(st.session_state['picked_dates'][1].strftime("%Y.%m.%d"))][data['date'] >= pd.Timestamp(st.session_state['picked_dates'][0].strftime("%Y.%m.%d"))]   


    # Разделение экрана на три столбца
    col1, _, col3 = st.columns(3)



    # График во втором столбце

    with col1:
        with st.container(border=True):
            # Выпадающий список для выбора даты в первом столбце
            # selected_date_scatter = col1.selectbox('Выберите дату', [date.date() for date in date_list], key='scatter_selector')
                # Фильтрация данных по выбранной дате
                
            try:
                fig_line = px.bar(filtered_data, x='date', y='Посетители', title='Посещений за выбранный промежуток времени', hover_data=['author', 'post_tag', 'post_id'])
                st.plotly_chart(fig_line)
            
            except Exception as e:
                print(e)


        


        

    # Круговая диаграмма в третьем столбце
    with col3:
        selected_metric_diagram = col3.selectbox('Выберите метрику для сравнения', ['date', 'author', 'Посетители', 'Читатели'], key='metric_selector' )

        with st.container(border=True):
            # Сделать выбор промежутка по времени
            # selected_date_diagram = col3.selectbox('Выберите дату', date_list, key='diagram_selector')
            

            

            # fig_pie = px.pie(filtered_data_diagram, names='visitors', title='Круговая диаграмма')
            try:
                fig_pie = px.pie(filtered_data, names=selected_metric_diagram, title='Круговая диаграмма')
                st.plotly_chart(fig_pie)
            
            except Exception as e:
                print(e)