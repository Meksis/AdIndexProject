import streamlit as st
import pandas as pd
import plotly.express as px

import datetime

from Utils.parser import *


st.set_page_config(layout="wide", initial_sidebar_state='collapsed') # установка широкого расположения объектов
# st.write(st.session_state)
# st.write(__file__)
# st.write(st.session_state['datas'])


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






today = datetime.date.today()

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
        csv_save_path = f'./csvs/AdIndex news {st.session_state["picked_dates"][0]}__{st.session_state["picked_dates"][1]}.csv'

        csv_save_metrics_path = csv_save_path.split()
        csv_save_metrics_path = ' '.join(csv_save_metrics_path[ : 2]) + ' metrics ' + csv_save_metrics_path[-1]

        refresh_datas(st.session_state['picked_dates'][0], st.session_state['picked_dates'][1], csv_save_path)
        refresh_metrics(csv_save_metrics_path)

        # data = st.session_state['datas_full']





if 'datas_full' in st.session_state:
    data = st.session_state['datas_full']
    data = data[data['date'] <= pd.Timestamp(st.session_state['picked_dates'][1].strftime("%Y.%m.%d"))]
    data = data[data['date'] >= pd.Timestamp(st.session_state['picked_dates'][0].strftime("%Y.%m.%d"))]

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