from dash import Dash, dcc, html, Input, Output, callback
import dash
from dash.dash_table import DataTable
# import dash_core_components as dcc
# import dash_html_components as html
import pandas as pd

dash.register_page(__name__, path = '/main')

# Создайте датафрейм Pandas
df = pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data', names=['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species'])

# Создайте приложение Dash
# app = dash.Dash(__name__)

# Определите layout
layout = html.Div([
    html.H1('Главная страница'),
    
    # Таблица
    DataTable(data=df.to_dict('records'), page_size=10, editable=True),
    
    # График 1 - гистограмма площади лепестков
    dcc.Graph(
        id='petal-area-histogram',
        figure={
            'data': [
                {'x': df['petal_length'] * df['petal_width'], 'type': 'histogram'}
            ],
            'layout': {
                'title': 'Гистограмма площади лепестков'
            }
        }
    ),
    
    # График 2 - рассеянный диаграмм Sepal Length vs Sepal Width
    dcc.Graph(
        id='sepal-scatter',
        figure={
            'data': [
                {'x': df['sepal_length'], 'y': df['sepal_width'], 'mode': 'markers', 'name': 'Sepal Length vs Sepal Width'}
            ],
            'layout': {
                'title': 'Sepal Length vs Sepal Width (рассеянный диаграмм)'
            }
        }
    )
])


