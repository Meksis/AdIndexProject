from dash import Dash, dcc, html, Input, Output, callback
import dash
import dash_bootstrap_components as dbc
from dash import html
import plotly.express as px
import pandas as pd

from Utils.data_prepare import Publication


dash.register_page(__name__, path='/' ,external_stylesheets=[dbc.themes.BOOTSTRAP], )

render_df = Publication()

# Создайте датафрейм Pandas
ddf = pd.read_csv('csvs\AdIndex_24_05-1_28_Metrics.csv', index_col=0, parse_dates=True)

df = render_df.page_df(df=ddf)

cdf= render_df.bar_data(df,5)
# cdf.sort_values(by='Читатели', ascending=False)




visit = {
    "title": "Посещаемость",
    "value": ddf.Посетители.sum(),
}
uniuser = {
    "title": "Уникальных пользователей",
    "value": ddf['Уникальные пользователи'].sum(),
}
uniuser = {
    "title": "Ср. глубина просмотра",
    "value": round(ddf['Глубина просмотра'].mean(),3),
}

# Определяем стиль для карточки
card_style = {
    'padding': '20px',
    'margin': '20px',
    'boxShadow': '2px 2px 10px rgba(0, 0, 0, 0.1)',
    'borderRadius': '10px',
    'backgroundColor': '#ffffff',
    'flex': '1',
    'minWidth': '200px'
}

# Определяем стиль для заголовка
title_style = {
    'fontSize': '24px',
    'fontWeight': 'bold',
    'marginBottom': '10px'
}

# Определяем стиль для значения
value_style = {
    'fontSize': '32px',
    'color': '#17BECF',
    'marginBottom': '10px'
}

# Определяем стиль для контейнера контента
content_style = {
    'marginTop': '80px',  # Добавляем отступ сверху, чтобы не налипали на навигационную панель
    'padding': '20px'
}

# Определяем стиль для контейнера карточек
cards_container_style = {
    'display': 'flex',
    'justifyContent': 'space-around',
    'flexWrap': 'wrap',
    'marginBottom': '40px'  # Добавляем отступ снизу, чтобы карточки не налипали на график
}

# Определяем layout для приложения
layout = html.Div([

    
    html.Div([
        html.Div([
            html.Div(visit['title'], style=title_style),
            html.Div(visit['value'], style=value_style)
        ], style=card_style),
        
        html.Div([
            html.Div(uniuser['title'], style=title_style),
            html.Div(uniuser['value'], style=value_style)
        ], style=card_style),
    ], style=cards_container_style),
    
    html.Div([
        dcc.Graph(
            figure=px.bar(cdf, x=cdf.Автор, y='Читатели', title='Рейтинг публикаций', width=1000, height=650)
        )
    ], style=content_style)
])

# Добавляем CSS для ссылок при наведении
index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            .nav-link:hover {
                background-color: #0056b3;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''