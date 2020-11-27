import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


def markSliderRange(min, max):
    mark = {}
    for i in range(min, max + 1):
        mark[i] = str(i)
    return mark


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Card([
        dbc.Row([
            dbc.Col(
                dbc.CardBody([
                    html.H3("Menu"),
                    html.Br(),
                    html.Br(),
                    dbc.Button("Choose Files", color="primary", className="mr-1"),
                    html.Br(),
                    html.Br(),
                    html.H6("Selected Files:"),
                    dbc.Select(
                        id="Selected File 1",
                        options=[
                            {"label": "File 1", "value": "1"},
                            {"label": "File 2", "value": "2"},
                        ],
                        value="1"
                    ),
                    dbc.Select(
                        id="Selected File 2",
                        options=[
                            {"label": "File 1", "value": "1"},
                            {"label": "File 2", "value": "2"},
                        ],
                        value="2"
                    ),
                    html.Br(),
                    html.Br(),
                    html.H6("K-mer length:"),
                    dcc.Slider(
                        id='k',
                        min=1,
                        max=10,
                        step=1,
                        value=1,
                        marks=markSliderRange(0, 10)
                    ),

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
                    html.H6("Top-values:"),
                    dcc.Slider(
                        id='top',
                        min=1,
                        max=10,
                        step=1,
                        value=1,
                        marks=markSliderRange(0, 10)
                    ),
                    html.Br(),
                    html.H6("Peak-position:"),
                    dcc.Slider(
                        id='peak',
                        min=1,
                        max=10,
                        step=1,
                        value=1,
                        marks=markSliderRange(0, 10)
                    ),
                    html.Br(),
                    html.H6("Number of highlights:"),
                    dcc.Slider(
                        id='highlight',
                        min=1,
                        max=10,
                        step=1,
                        value=1,
                        marks=markSliderRange(0, 10),
                    ),
                    html.Br(),
                    html.H6("Highlighted Feature:"),
                    dbc.Select(
                        id="Feature",
                        options=[
                            {"label": "Frequency", "value": "1"},
                            {"label": "T Occurences", "value": "2"},
                        ],
                        value="1"
                    ),

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
