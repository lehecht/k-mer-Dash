import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
from src.dashView import initializeData

process = None


def startDash(slc, k_len, p, t):
    if slc is not None:
        global process
        process = initializeData.initData(slc, slc, k_len, p, t)
        app.run_server(debug=True)


def markSliderRange(min, max):
    mark = {}
    for i in range(min, max + 1):
        mark[i] = str(i)
    return mark


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.title = "k-Mer Dash"

app.layout = dbc.Container([
    dbc.Card([
        dbc.Row([
            dbc.Col(
                dbc.CardBody([
                    html.H3("Menu"),
                    html.Br(),
                    html.Br(),
                    # ------------------------- Choose Fasta-Files -----------------------------------------------------
                    dbc.Button("Choose Files", color="primary", className="mr-1"),
                    html.Br(),
                    html.Br(),
                    # ------------------------------------- Select File1 And File 2 ------------------------------------
                    html.H6("Selected Files:"),
                    dbc.Select(
                        id="file1",
                        options=[
                            {"label": "File 1", "value": "1"},
                            {"label": "File 2", "value": "2"},
                        ],
                        # value="1"
                    ),
                    dbc.Select(
                        id="file2",
                        options=[
                            {"label": "File 1", "value": "1"},
                            {"label": "File 2", "value": "2"},
                        ],
                        # value="2"
                    ),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    # ------------------------------------------- K ----------------------------------------------------
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

            # --------------------------------------- ScatterPlot ------------------------------------------------------
            dbc.Col(dbc.Card([
                dbc.Spinner(children=[
                    dcc.Graph(figure={}, id="scatter", style={'height': '50vh'})], color="primary",
                    spinner_style={'position': 'absolute',
                                   'top': '50%',
                                   'left': '50%'
                                   })

            ], style={
                'background': '#f2f2f2', 'height': '50vh'}, outline=True),
                width=5,
                style={"padding-right": '5px',
                       "padding-left": '10px'}),

            # ------------------------------------------------- PCAs ---------------------------------------------------
            dbc.Col(dbc.Card([
                dbc.Spinner(children=[dcc.Tabs(id='tabs-example', value='Tab1', children=[
                    dcc.Tab(label="", value='Tab1', id="Tab1", children=[
                        dcc.Graph(figure={}, id="PCA1",
                                  style={'height': '42vh'}
                                  )
                    ]),
                    dcc.Tab(label="", value='Tab2', id="Tab2", children=[
                        dcc.Graph(figure={}, id="PCA2",
                                  style={'height': '42vh'}
                                  )
                    ]),
                ],
                                               )], color="primary", spinner_style={'position': 'absolute',
                                                                                   'top': '50%',
                                                                                   'left': '50%'
                                                                                   }),

            ], style={
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
                    # ---------------------------------------- Top -----------------------------------------------------
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
                    # ----------------------------------------- Peak ---------------------------------------------------
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
                    # -------------------------------- Highlighted Feature ---------------------------------------------
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
            # -------------------------------------------- TopK --------------------------------------------------------
            dbc.Col(
                dbc.Spinner(children=[dbc.Card(id="topK", children=[], style={
                    'background': '#f2f2f2', 'height': '49vh', 'overflow-y': 'scroll'}, outline=True)],
                            color="primary", spinner_style={'position': 'absolute',
                                                            'top': '50%',
                                                            'left': '50%'
                                                            }),
                width=5,
                style={"padding-right": '5px',
                       "padding-top": '5px',
                       "padding-left": '10px'}),

            # ------------------------------------------- MSA ----------------------------------------------------------
            dbc.Col(
                dbc.Spinner(children=[dbc.Card(id="msa", children=[], style={
                    'background': '#f2f2f2', 'height': '49vh', 'overflow-y': 'scroll'}, outline=True)],
                            color="primary", spinner_style={'position': 'absolute',
                                                            'top': '50%',
                                                            'left': '50%'
                                                            }),
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


@app.callback(
    [dash.dependencies.Output('scatter', 'figure'), ],
    [
        dash.dependencies.Input('file1', 'value'),
        dash.dependencies.Input('file2', 'value'),
        dash.dependencies.Input('k', 'value'),
        dash.dependencies.Input('top', 'value'),
        dash.dependencies.Input('peak', 'value'),
    ]

)
def updateScatterPlot(file1, file2, k_d, top_d, peak_d):
    scatter = None
    if file1 is None and file2 is None:
        scatter = initializeData.getScatterPlot(process)
    return [scatter]


@app.callback(
    [dash.dependencies.Output('PCA1', 'figure'),
     dash.dependencies.Output('PCA2', 'figure'),
     dash.dependencies.Output('Tab1', 'label'),
     dash.dependencies.Output('Tab2', 'label')
     ],
    [
        dash.dependencies.Input('file1', 'value'),
        dash.dependencies.Input('file2', 'value'),
        dash.dependencies.Input('k', 'value'),
        dash.dependencies.Input('top', 'value'),
        dash.dependencies.Input('peak', 'value'),
    ]

)
def updatePCA(file1, file2, k_d, top_d, peak_d):
    pca1 = None
    pca2 = None
    file1 = None
    file2 = None
    if file1 is None and file2 is None:
        pcas, file1, file2 = initializeData.getPCA(process)
        pca1 = pcas[0]
        pca2 = pcas[1]
    return [pca1, pca2, file1, file2]


@app.callback(
    [dash.dependencies.Output('topK', 'children')],
    [
        dash.dependencies.Input('file1', 'value'),
        dash.dependencies.Input('file2', 'value'),
        dash.dependencies.Input('k', 'value'),
        dash.dependencies.Input('top', 'value'),
        dash.dependencies.Input('peak', 'value'),
    ]

)
def updateTopTable(file1, file2, k_d, top_d, peak_d):
    topK = None
    if file1 is None and file2 is None:
        topK = process.getTopKmer().copy()
        kmer = topK.index
        topK["K-Mer"] = kmer
        topK = topK[["K-Mer", "Frequency", "File"]]
        topK = topK.sort_values(by="Frequency", ascending=False)
    return [dbc.Table.from_dataframe(topK, striped=True, bordered=True, hover=True, size='sm',
                                     style={'text-align': 'center'}, loading_state={'is_loading': True})]


@app.callback(
    [dash.dependencies.Output('msa', 'children')],
    [
        dash.dependencies.Input('file1', 'value'),
        dash.dependencies.Input('file2', 'value'),
        dash.dependencies.Input('k', 'value'),
        dash.dependencies.Input('top', 'value'),
        dash.dependencies.Input('peak', 'value'),
    ]

)
def updateMSA(file1, file2, k_d, top_d, peak_d):
    algn = None
    peak = process.getSettings().getPeak()
    if file1 is None and file2 is None:
        algn = initializeData.getAlignmentData(process)
        if peak is not None:
            algn = pd.DataFrame(algn)
            algn.columns = ["Alignment at peak position"]
        else:
            algn = [str(entry.seq) for entry in algn]
            algn = pd.DataFrame(algn)
            algn.columns = ["Alignment with ClustalW"]

    return [dbc.Table.from_dataframe(algn, borderless=True, hover=True, size='sm', style={'text-align': 'center'})]
