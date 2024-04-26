from dash import Dash, dcc, html, Input, Output, callback
import dash
from dash.dash_table import DataTable
# import dash_core_components as dcc
# import dash_html_components as html
import plotly.express as px
import pandas as pd

dash.register_page(__name__, path = '/main')

# Создайте датафрейм Pandas
df = pd.read_csv('csvs\AdIndex main news METRICS 2023-12-14.csv', index_col=0, parse_dates=True)

# Создайте приложение Dash
# app = dash.Dash(__name__)

# Определите layout
layout = html.Div([
    html.H1('Главная страница'),
    
    # Таблица
    DataTable(data=df.to_dict('records'), page_size=10, editable=True),
    




    
    # График 1 - гистограмма площади лепестков
    dcc.Graph(
        id='tree',
        figure= px.treemap(df, path=['post_tag','author'], title='Посещений за выбранный промежуток времени', )

    ),
    
    # # График 2 - рассеянный диаграмм Sepal Length vs Sepal Width
    # dcc.Graph(
    #     id='sepal-scatter',
    #     figure={
    #         'data': [
    #             {'x': df['sepal_length'], 'y': df['sepal_width'], 'mode': 'markers', 'name': 'Sepal Length vs Sepal Width'}
    #         ],
    #         'layout': {
    #             'title': 'Sepal Length vs Sepal Width (рассеянный диаграмм)'
    #         }
    #     }
    # )
])


