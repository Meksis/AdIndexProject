from dash import Dash, dcc, html, Input,State, Output, callback
import dash
from dash.dash_table import DataTable
# import dash_core_components as dcc
# import dash_html_components as html
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from Utils.data_prepare import Publication

dash.register_page(__name__, path = '/news',external_stylesheets=[dbc.themes.BOOTSTRAP])

render_df = Publication()

# Создайте датафрейм Pandas
df = pd.read_csv('csvs\AdIndex_24_05-1_28_Metrics.csv', index_col=0, parse_dates=True)

cl_df = render_df.page_df(df=df)

# Создайте приложение Dash
# app = dash.Dash(__name__)

# Определите layout
layout = html.Div([
    
    html.H2('Рейтинг публикаций'),
    # html.P('Временной промежуток'),
    
    # dbc.RadioItems(
    #             ['3 Дня', '7 Дней', '30 Дней',],
    #             # 'Linear',
    #             value = '3 Дня',  
    #             id ='date-select',
    #             inline =True
    #         ),
    
    html.P('Топ'),
    
    dbc.RadioItems(
                [ 10, 30, 50],
                # 'Linear',
                id='news-head',
                value = 10,  

                inline=True
            ),
    
    dcc.Graph(
        id='bar-pub',
        # figure= px.bar(render_df.bar_data(df,5), x='post_id', y='Читатели', title='Рейтинг публикаций', 
        #     width=1400, height=800)

    ),
    
     dbc.Button(
            "?",
            id="collapse-button",
            className="mb-3",
            color="primary",
            n_clicks=0,
        ),

        dbc.Collapse(
            dbc.Card([
                html.H4('Описание столбцов таблицы'),
                dbc.CardBody('Тема - Название темы, по которой публикуются статьи'),
                dbc.CardBody('Читатели - Количество подписчиков на тему'),
                dbc.CardBody('Кол во статей - Количество статей, опубликованных по теме'),
                dbc.CardBody('Лучший автор - Автор, опубликовавший наибольшее количество статей по теме'),
                ]),
            id="collapse-pub",
            is_open=False,
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
                page_size=20, 
    
            ),
])


@callback(
    Output('bar-pub', 'figure'),
    Input('news-head','value'),
)
def update_figure(head):
    fig = px.bar(render_df.bar_data(df,head), x='Название', y='Читатели', title='Рейтинг публикаций', 
            width=2100, height=1100)
    
    return fig


@callback(
    Output('collapse-pub', "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State('collapse-pub', "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open