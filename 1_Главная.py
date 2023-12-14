import streamlit as st
import pandas as pd
import plotly.express as px

import datetime

from Utils.parser import *
st.set_page_config(layout="wide", initial_sidebar_state='collapsed') # установка широкого расположения объектов


def refresh_datas(parse_days : int = 1):
    st.session_state['datas'] = parse_some_news(days4parse=parse_days)


def refresh_metrics():
    datas = st.session_state['datas']
    datas_metrics = pd.DataFrame()

    
    for link in datas.link:
        datas_metrics = pd.concat([datas_metrics, pd.DataFrame([get_data_from_url(link)[1]])])

    st.session_state['datas_full'] = datas.merge(datas_metrics, how='inner', on='link')
    st.session_state['datas_full'].to_csv(f'AdIndex main news METRICS {datetime.datetime.today().strftime("%Y-%m-%d")}.csv')



# Загрузка данных (замените 'your_data.csv' на путь к вашему файлу данных)
# data = pd.read_csv('your_data.csv')


if 'datas_full' not in st.session_state:
    refresh_datas()
    refresh_metrics()

else:
    data = st.session_state['datas_full']

# st.write(data)
# Создание списка уникальных дат для выбора периода
date_list = sorted(data['date'].unique())

# Заголовок
# st.title('Графики и диаграммы с выбором периода')


if st.button('Обновить данные'):
    with st.spinner('Обновляемся'):
        st.session_state['datas'] = parse_some_news(days4parse=(st.session_state['picked_dates'][1] - st.session_state['picked_dates'][0]).days)
        data = st.session_state['datas']



today = datetime.datetime.now()

try:
    selected_date = st.date_input(      # Создаем поле для ввода даты, задавая размеры от минимальной даты в датафрейме до текущей и выставляя значение от текущей недели до 7 дней назад
        "Выберете промежуток выборки",
        (
            datetime.date(today.year, today.month, today.day - 7 if today.day - 7 > 0 else 1),
            today
        ),
        datetime.date(data.date.iloc[0].year, data.date.iloc[0].month, data.date.iloc[0].day - 7),
        # data.date.iloc[-1],
        today,
        format="YYYY.MM.DD",
        key='scatter_datepick'
    )

    st.session_state['picked_dates'] = selected_date


    filtered_data = data[data['date'] <= pd.Timestamp(selected_date[1].strftime("%Y.%m.%d"))][data['date'] >= pd.Timestamp(selected_date[0].strftime("%Y.%m.%d"))]   


    # st.write(pd.DataFrame({'Средняя глубина просмотра' : filtered_data['visitors'].sum() / filtered_data['views'].sum() }, index=['Средняя глубина просмотра'], columns = ['Средняя глубина просмотра'] ))
    # st.write(pd.DataFrame.from_records([{'Средняя глубина просмотра' : filtered_data['visitors'].sum() / filtered_data['views'].sum() }]))

    # print(pd.DataFrame.from_records([{'Средняя глубина просмотра' : filtered_data['visitors'].sum() / filtered_data['views'].sum() }]))

    # st.table({'Средняя глубина просмотра' : filtered_data['visitors'].sum() / filtered_data['views'].sum() })


except Exception as e:
    pass


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