import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#
# app.layout = html.Div(children=[
#     html.H1(id='header', children='Hello Dash'),
#
#     html.Div(children='''
#         Dash: A web application framework for Python!!!!
#     '''),
#
#     dcc.Graph(
#         id='example-graph',
#         figure={
#             'data': [
#                 {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
#                 {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
#             ],
#             'layout': {
#                 'title': 'Dash Data Visualization'
#             }
#         }
#     )
# ])


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Card([
        dbc.Row([
            dbc.Col(
                dbc.CardBody([
                    html.H3('Menü')
                ], style={
                    'height': '50vh',
                    'left': '0px',
                    'background': 'lightgrey'}),
                width=2,
                style={"padding-right": '0px',
                       "padding-left": '0px',
                       'margin-right': '0px'}),

            dbc.Col(dbc.Card(["TEST1"], style={
                'background': '#f2f2f2', 'height': '50vh'}, outline=True),
                    width=5,
                    style={"padding-right": '5px',
                           "padding-left": '10px'}),

            dbc.Col(dbc.Card(["TEST2"], style={
                'background': '#f2f2f2', 'height': '50vh'}, outline=True),
                    width=5,
                    style={"padding-right": '0px',
                           "padding-left": '0px'}
                    )
        ], style={'padding-top': '0px', 'padding-bottom': '0px', 'margin-top': '0px', 'margin-bottom': '0px',
                  'margin-left': '0px', 'padding-left': '0px'},
            className="mw-100 mh-100"
        ),

        dbc.Row([
            dbc.Col(
                dbc.CardBody([
                    html.H3()
                ], style={
                    'height': '50vh',
                    'left': '0px',
                    'background': 'lightgrey'}),
                width=2,
                style={"padding-right": '0px',
                       "padding-left": '0px',
                       'margin-right': '0px'}),
            dbc.Col(dbc.Card(["TEST3"], style={
                'background': '#f2f2f2', 'height': '49vh'}, outline=True),
                    width=5,
                    style={"padding-right": '5px',
                           "padding-top": '5px',
                           "padding-left": '10px'}),

            dbc.Col(dbc.Card(["TEST4"], style={
                'background': '#f2f2f2', 'height': '49vh'}, outline=True),
                    width=5,
                    style={"padding-right": '0px',
                           "padding-top": '5px',
                           "padding-left": '0px'}
                    )
        ], style={'padding-top': '0px', 'padding-bottom': '0px', 'margin-top': '0px', 'margin-bottom': '0px',
                  'margin-left': '0px', 'padding-left': '0px'},
            className="mw-100 mh-100"
        )

    ],
        className="mw-100 mh-100"),
], className="mw-100 mh-100", style={'left': '0px', 'margin-left': '0px', 'padding': '0px'})


def startDash():
    app.run_server(debug=True)
