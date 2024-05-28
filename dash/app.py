from dash import Dash, dcc, html, Input, Output, callback_context
import dash
from dash.dash_table import DataTable
import dash_bootstrap_components as dbc

import pandas as pd
import plotly.express as px


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], use_pages=True, pages_folder='pages')
nav_style = {
    'display': 'flex',
    'justifyContent': 'space-around',
    'alignItems': 'center',
    'padding': '10px 0',
    'backgroundColor': '#007bff',
    'color': '#ffffff',
    'position': 'fixed',
    'top': '0',
    'width': '100%',
    'zIndex': '1000'
}

# Определяем стиль для каждой ссылки
link_style = {
    'padding': '10px 15px',
    'color': '#ffffff',
    'fontSize': '18px',
    'textDecoration': 'none',
    'borderRadius': '5px',
    'transition': 'background-color 0.3s'
}

link_hover_style = {
    'backgroundColor': '#0056b3'
}

# Определяем стиль для контейнера контента
content_style = {
    'marginTop': '60px',  # Добавляем отступ сверху, чтобы не налипали на навигационную панель
    'padding': '20px'
}

# Определяем layout для приложения
app.layout = html.Div([
    html.Div([
        dcc.Link(page['name'], href=page["relative_path"], style=link_style, className='nav-link')
        for page in dash.page_registry.values()
    ], style=nav_style, className='nav-bar'),
    html.Div(dash.page_container, style=content_style)
])

# Добавляем CSS для ссылок при наведении
app.index_string = '''
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


if __name__ == '__main__':
    app.run(debug=True)
