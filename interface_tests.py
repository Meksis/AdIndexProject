import streamlit as st
import pandas as pd
import plotly.express as px


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
a = [
    {
        'date' : '1',
        'author' : 'f',
        'visitors' : 1,
        'post_tag' : '',
        'post_id' : '',
        'link' : ''
    }
]

data = pd.DataFrame([
    {
        'date' : '1',
        'visitors' : 1
    },
    {
        'date' : '2',
        'visitors' : 10
    },
    {
        'date' : '3',
        'visitors' : 100
    },
    {
        'date' : '4',
        'visitors' : 500
    },
    {
        'date' : '5',
        'visitors' : 2000
    },
    {
        'date': '6', 
        'visitors': 10000
    }, 
    {
        'date': '7', 
        'visitors': 20000
    },
    {
        'date': '8', 
        'visitors': 30000
    }, 
    {
        'date': '9', 
        'visitors': 40000
        },
    {
        'date': '10', 
        'visitors': 50000
        }
])

# Создание списка уникальных дат для выбора периода
date_list = sorted(data['date'].unique())

# Заголовок
st.title('Графики и диаграммы с выбором периода')

# Разделение экрана на три столбца
col1, col2, col3 = st.columns(3)



# График во втором столбце
with col1:
    # Выпадающий список для выбора даты в первом столбце
    selected_date_scatter = col1.selectbox('Выберите дату', date_list, key='scatter_selector')

    # Фильтрация данных по выбранной дате
    filtered_data_scatter = data[data['date'] == selected_date_scatter]
    fig_line = px.scatter(filtered_data_scatter, x='date', y='visitors', title='График')
    st.plotly_chart(fig_line)

# Круговая диаграмма в третьем столбце
with col3:
    # Выпадающий список для выбора даты в первом столбце
    selected_date_diagram = col3.selectbox('Выберите дату', date_list, key='diagram_selector')

    # Фильтрация данных по выбранной дате
    filtered_data_diagram = data[data['date'] == selected_date_diagram]
    fig_pie = px.pie(filtered_data_diagram, names='visitors', title='Круговая диаграмма')
    st.plotly_chart(fig_pie)


