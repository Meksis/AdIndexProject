from dash import Dash, dcc, html, Input, Output, callback
import dash
from dash.dash_table import DataTable
# import dash_core_components as dcc
# import dash_html_components as html
import plotly.express as px
import pandas as pd

from Utils.data_prepare import Theme

dash.register_page(__name__, path = '/theme')

render_df = Theme()

# Создайте датафрейм Pandas
df = pd.read_csv('csvs\AdIndex main news METRICS 2023-12-14.csv', index_col=0, parse_dates=True)

df = render_df.page_df(df=df)











# Создайте приложение Dash
# app = dash.Dash(__name__)

# Определите layout
layout = html.Div([
    
    html.H2('Рейтинг тематик'),
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
    sum_read.sort_values(by='Читатели', ascending=False, inplace=True)
    best_topic_author = px.bar(sum_read, x='лучший_автор', y='Читатели', title='Топ авторов во всех темах', 
                width=1400, height=800)
                # width=1400, height=800, hover_data=['Тема', 'лучший_автор', "Читатели"])


    # best_topic_author.show()

    # fig = px.bar(render_df.bar_data(df,head), x='Тема', y='Читатели', title='Рейтинг публикаций', 
    #         width=1200, height=550)
    
    return best_topic_author