from dash import Dash, dcc, html, Input, State, Output, callback
import dash
from dash.dash_table import DataTable
# import dash_core_components as dcc
# import dash_html_components as html
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from Utils.data_prepare import Author

dash.register_page(__name__, path = '/author')

render_df = Author()

# Создайте датафрейм Pandas
df = pd.read_csv('csvs\AdIndex_24_05-1_28_Metrics.csv', index_col=0, parse_dates=True)

cl_df = render_df.top_authors_df(df=df)

# Создайте приложение Dash
# app = dash.Dash(__name__)

# Определите layout
layout = html.Div([
    
    html.H2('Рейтинг Авторов'),
    # html.P('Временной промежуток'),
    
    # dbc.RadioItems(
    #             ['3 Дня', '7 Дней', '30 Дней',],
    #             # 'Linear',
    #             value = '3 Дня',  
    #             id ='date-select',
    #             inline =True
    #         ),
    
    
    # dbc.RadioItems(
    #             [5, 10, 20,],
    #             # 'Linear',
    #             id='author-head',
    #             value = 5,  

    #             inline=True
    #         ),
    
    dcc.Graph(
        id='bar-author',
        figure= px.bar(cl_df, x='Автор', y='Количество просмотров', title='Рейтинг авторов', 
            width=1500, height=600)

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
                dbc.CardBody('Автор - ФИО автора'),
                dbc.CardBody('количество просмотров - сумарное количество просмотров публикаций'),
                dbc.CardBody('Количество статей - Количество статей, опубликованных автором'),
                dbc.CardBody('Глубина - Среднее количество страниц(на сайте adindex) посейщеных после перехода на страницу статьи'),
                dbc.CardBody('Лучший автор - Автор, опубликовавший наибольшее количество статей по теме'),
                ]),
            id="collapse-author",
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
                page_size=10, 
    
            ),
])


# @callback(
#     Output('bar-author', 'figure'),
#     Input('author-head','value'),
# )
# def update_figure(head):
#     fig = px.bar(render_df.bar_data(df,head), x='Автор', y='Читатели', title='Рейтинг авторов', 
#             width=1500, height=600)
    
#     return fig

@callback(
    Output('collapse-author', "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State('collapse-author', "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open