from dash import Dash, dcc, html, Input, Output, callback
from dash.dash_table import DataTable


import pandas as pd
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

reload_btn = html.Button(
        'reload',
        '1',
        0,
        draggable = 'false'

    )


plot = dcc.Graph(
    'graph'
)

data_table = DataTable(
    page_size=10,
    style_data_conditional=[{
        'if': {'column_editable': False},
        'backgroundColor': 'rgb(30, 30, 30)',
        'color': 'white'
    }],
    style_header_conditional=[{
        'if': {'column_editable': False},
        'backgroundColor': 'rgb(30, 30, 30)',
        'color': 'white'
    }]
)


app.layout = html.Div(
    style = {
        'bgcolor': 'rgb(0, 0, 0)'
    },
    id = 'div1',
    children = [
    reload_btn,
    data_table,
    plot
]
    
)





@callback(
    Output(plot, 'figure'),
    Output(data_table, 'data'),
    Input(reload_btn, 'n_clicks')
)
def on_reload_click(n_clicks):
    df = pd.read_csv('./csvs/AdIndex main news METRICS 2023-12-14.csv', index_col=0, parse_dates=True)
    df['date'] = df['date'].apply(lambda x: pd.to_datetime(x))

    return (px.line(df['post_id']), df.to_dict('records'))


@callback(
    Output(plot, 'figure'),
    Input(data_table, 'data'),
    Input(reload_btn, 'n_clicks')
)
def on_reload_click(n_clicks):
    df = pd.read_csv('./csvs/AdIndex main news METRICS 2023-12-14.csv', index_col=0, parse_dates=True)
    df['date'] = df['date'].apply(lambda x: pd.to_datetime(x))

    return (px.line(df['post_id']), df.to_dict('records'))



@callback(
    Output(plot, 'figure'),
    Input(data_table, 'data'),
    Input(data_table, 'columns')
)
def callback_table(rows, columns):
    df = pd.DataFrame(rows, columns=[c['name'] for c in columns])






if __name__ == '__main__':
    app.run(debug=True)
