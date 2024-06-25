from dash import Dash, dcc, html, Input, State, Output, callback
import dash
from dash.dash_table import DataTable
# import dash_core_components as dcc
# import dash_html_components as html
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from Utils.data_prepare import Theme

dash.register_page(__name__, path = '/theme',external_stylesheets=[dbc.themes.BOOTSTRAP])

render_df = Theme()

# Создайте датафрейм Pandas
df = pd.read_csv('./csvs/AdIndex_24_05-1_28_Metrics.csv', index_col=0, parse_dates=True)

df = render_df.page_df(df=df)



# Создайте приложение Dash
# app = dash.Dash(__name__)

# Определите layout
layout = html.Div([
    
    html.H2('Рейтинг тематик'),
    html.P('Временной промежуток'),
    
    dbc.RadioItems(
                ['3 Дня', '7 Дней', '30 Дней',],
                # 'Linear',
                value = '3 Дня',  
                id ='date-select',
                inline =True
            ),
    
    html.P('Топ'),
    
    dbc.RadioItems(
                [5, 10, 20,],
                # 'Linear',
                id='theme-head',
                value = 5,  

                inline=True
            ),
     

    dcc.Graph(
        id='bar-theme-viewers',
        # figure= px.bar(render_df.bar_data(df,5), x='post_id', y='Читатели', title='Рейтинг публикаций', 
        #     width=1400, height=800)

    ),
    
    dcc.Graph(
        id='bar-theme',
        figure= px.bar(render_df.bar_data(df,5), x='Тема', y='Читатели', title='Рейтинг публикаций', 
            width=1400, height=800)

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
                dbc.CardBody('Тема	Название темы, по которой публикуются статьи'),
                dbc.CardBody('Читатели	Количество подписчиков на тему'),
                dbc.CardBody('Кол во статей	Количество статей, опубликованных по теме'),
                dbc.CardBody('Лучший автор	Автор, опубликовавший наибольшее количество статей по теме'),
                ]),
            id='collapse-theme',
            is_open=False,
        ),


    # Таблица
    DataTable(
                id='main-table',
                data=df.to_dict('records'),
                sort_action='native', 
                editable=True,
                # row_selectable="single",
                # filter_action='native',
                # row_deletable=True,
                # page_size=10, 
    
            ),
])


@callback(
    Output('bar-theme-viewers', 'figure'),
    Input('theme-head','value'),
)
def update_themes_chart(head):
    fig = px.bar(render_df.bar_data(df,head), x='Тема', y='Читатели', title='Рейтинг тематики', 
            width=1200, height=550)
    
    return fig



@callback(
    Output('bar-theme', 'figure'),
    Input('theme-head','value'),
)
def update_themes_best_authors(head):

    sum_read = df.groupby('лучший_автор')['Читатели'].sum().reset_index()
    sum_read=sum_read.sort_values(by='Читатели', ascending=False,).head(head)

    best_topic_author = px.bar(sum_read, x='лучший_автор', y='Читатели', title='Топ авторов во всех темах', 
                width=1400, height=800)
                # width=1400, height=800, hover_data=['Тема', 'лучший_автор', "Читатели"])


    # best_topic_author.show()

    # fig = px.bar(render_df.bar_data(df,head), x='Тема', y='Читатели', title='Рейтинг публикаций', 
    #         width=1200, height=550)
    
    return best_topic_author


@callback(
    Output('collapse-theme', "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State('collapse-theme', "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open