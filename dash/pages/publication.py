from dash import Dash, dcc, html, Input, Output, callback
import dash
from dash.dash_table import DataTable
# import dash_core_components as dcc
# import dash_html_components as html
import plotly.express as px
import pandas as pd

from Utils.data_prepare import Publication

dash.register_page(__name__, path = '/news')

render_df = Publication()

# Создайте датафрейм Pandas
df = pd.read_csv('csvs\AdIndex main news METRICS 2023-12-14.csv', index_col=0, parse_dates=True)

cl_df = render_df.page_df(df=df)

# Создайте приложение Dash
# app = dash.Dash(__name__)

# Определите layout
layout = html.Div([
    
    html.H2('Рейтинг публикаций'),
    html.P('Временной промежуток'),
    
    dcc.RadioItems(
                ['3 Дня', '7 Дней', '30 Дней',],
                # 'Linear',
                value = '3 Дня',  
                id ='date-select',
                inline =True
            ),
    
    html.P('Топ'),
    
    dcc.RadioItems(
                [5, 10, 20,],
                # 'Linear',
                id='news-head',
                value = 5,  

                inline=True
            ),
    
    dcc.Graph(
        id='bar-top',
        # figure= px.bar(render_df.bar_data(df,5), x='post_id', y='Читатели', title='Рейтинг публикаций', 
        #     width=1400, height=800)

    ),
    


    # Таблица
    DataTable(
                id='main-table',
                data=cl_df.to_dict('records'),
                sort_action='native', 
                editable=True,
                # row_selectable="single",
                # filter_action='native',
                # row_deletable=True,
                page_size=10, 
    
            ),
])


@callback(
    Output('bar-top', 'figure'),
    Input('news-head','value'),
)
def update_figure(head):
    fig = px.bar(render_df.bar_data(df,head), x='post_tag', y='Читатели', title='Рейтинг публикаций', 
            width=1200, height=550)
    
    return fig