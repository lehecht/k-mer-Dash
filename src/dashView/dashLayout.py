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
        dbc.CardBody([
            html.H3('Menü')
        ], style={"width": "20rem",
                                     'height': '100vh',
                                     'left': '0px',
                                     'background': 'lightgrey'}),

        # dbc.CardBody(["BBB"], style={"width": "20rem",
        #                              'position': 'relative',
        #                              'margin-top': '50px',
        #                              'left': '0px',
        #                              'background': 'grey'})

    ],

        className="mw-100 mh-100"),
], className="mw-100 mh-100", style={'left': '0px', 'margin-left': '0px', 'padding': '0px'})


def startDash():
    app.run_server(debug=True)

# , style={'height': '100vh','width':'5000px'}
