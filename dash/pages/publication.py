from dash import Dash, dcc, html, Input, Output, callback
import dash
from dash.dash_table import DataTable
# import dash_core_components as dcc
# import dash_html_components as html
import plotly.express as px
import pandas as pd

import Utils.data_prepare as clean_df

dash.register_page(__name__, path = '/news')

# Создайте датафрейм Pandas
df = pd.read_csv('csvs\AdIndex main news METRICS 2023-12-14.csv', index_col=0, parse_dates=True)

cl_df = clean_df.publication(df)

# Создайте приложение Dash
# app = dash.Dash(__name__)

# Определите layout
layout = html.Div([
    html.H1('Рейтинг публикаций'),
    dcc.RadioItems(
                ['3 Дня', '7 Дней', '30 Дней',],
                # 'Linear',
                id='date-select',
                inline=True
            ),
    # Таблица
    DataTable(
                id='main-table',
                data=cl_df.to_dict('records'),
                sort_action='native', 
                editable=True,
                # row_selectable="single",
                # filter_action='native',
                row_deletable=True,
                page_size=10, 
    
            ),
])


# @callback(
#     Input('date-select','value'),
# )