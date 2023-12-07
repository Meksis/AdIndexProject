import streamlit as st
import pandas as pd
import plotly.express as px

import datetime

import parser


st.set_page_config(layout="wide", initial_sidebar_state='collapsed') # установка широкого расположения объектов

# Загрузка данных (замените 'your_data.csv' на путь к вашему файлу данных)
# data = pd.read_csv('your_data.csv')

#CREATE TABLE DATA 
    # Date date,
    # author TEXT,
    # visitors INTEGER,
    # post_tag TEXT,
    # link TEXT,
    # post_id TEXT

if 'datas' not in st.session_state:
    st.session_state['datas'] = parser.parse_some_news()
    data = st.session_state['datas']

else:
    data = st.session_state['datas']

# st.write(data)
# Создание списка уникальных дат для выбора периода
date_list = sorted(data['date'].unique())

# Заголовок
st.title('Графики и диаграммы с выбором периода')


if st.button('Обновить данные'):
    with st.spinner('Обновляемся'):
        st.session_state['datas'] = parser.parse_some_news()
        data = st.session_state['datas']


# Разделение экрана на три столбца
col1, _, col3 = st.columns(3)




# График во втором столбце
with col1:
    # Выпадающий список для выбора даты в первом столбце
    # selected_date_scatter = col1.selectbox('Выберите дату', [date.date() for date in date_list], key='scatter_selector')

    today = datetime.datetime.now()

    try:
        selected_date_scatter = st.date_input(      # Создаем поле для ввода даты, задавая размеры от минимальной даты в датафрейме до текущей и выставляя значение от текущей недели до 7 дней назад
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


        filtered_data_scatter = data[data['date'] <= pd.Timestamp(selected_date_scatter[1].strftime("%Y.%d.%m"))][data['date'] >= pd.Timestamp(selected_date_scatter[0].strftime("%Y.%d.%m"))]   


        # st.write(pd.DataFrame({'Средняя глубина просмотра' : filtered_data_scatter['visitors'].sum() / filtered_data_scatter['views'].sum() }, index=['Средняя глубина просмотра'], columns = ['Средняя глубина просмотра'] ))
        # st.write(pd.DataFrame.from_records([{'Средняя глубина просмотра' : filtered_data_scatter['visitors'].sum() / filtered_data_scatter['views'].sum() }]))

        # print(pd.DataFrame.from_records([{'Средняя глубина просмотра' : filtered_data_scatter['visitors'].sum() / filtered_data_scatter['views'].sum() }]))

        st.table({'Средняя глубина просмотра' : filtered_data_scatter['visitors'].sum() / filtered_data_scatter['views'].sum() })


        # Фильтрация данных по выбранной дате
        fig_line = px.scatter(filtered_data_scatter, x='date', y='visitors', title='График')
        st.plotly_chart(fig_line)


    except Exception as e:
        pass


    

# Круговая диаграмма в третьем столбце
with col3:
    # Сделать выбор промежутка по времени
    # selected_date_diagram = col3.selectbox('Выберите дату', date_list, key='diagram_selector')
    

    today = datetime.datetime.now()

    try:
        selected_date_diagram = st.date_input(      # Создаем поле для ввода даты, задавая размеры от минимальной даты в датафрейме до текущей и выставляя значение от текущей недели до 7 дней назад
            "Выберете промежуток выборки",
            (
                datetime.date(today.year, today.month, today.day - 7 if today.day - 7 > 0 else 1),
                today
            ),
            datetime.date(data.date.iloc[0].year, data.date.iloc[0].month, data.date.iloc[0].day - 7),
            # data.date.iloc[-1],
            today,
            format="YYYY.MM.DD",
            key='diagram_datepick'
        )


        # new_datas = data.query(f'date <= {pd.to_datetime(selected_date_diagram[1], format="mixed")} & date >= {pd.to_datetime(selected_date_diagram[0], format="mixed")}')

        selected_metric_diagram = col3.selectbox('Выберите метрику для сравнения', ['date', 'author', 'visitors', 'views'], key='metric_selector' )

        # Фильтрация данных по выбранной дате
        filtered_data_diagram = data[data['date'] <= pd.Timestamp(selected_date_diagram[1])][data['date'] >= pd.Timestamp(selected_date_diagram[0])]        # Строки с датами между двух выбранных
        # fig_pie = px.pie(filtered_data_diagram, names='visitors', title='Круговая диаграмма')
        fig_pie = px.pie(filtered_data_diagram, names=selected_metric_diagram, title='Круговая диаграмма')
        st.plotly_chart(fig_pie)
    
    except Exception as e:
        raise e
        # print(str(e))


