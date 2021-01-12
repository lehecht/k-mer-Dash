import dash
import dash_core_components as dcc
import dash_table
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
from dash.exceptions import PreventUpdate

from src.processing import Processing
from src.dashView import initializeData

process = None
k_p_slider_max = None
k_p_slider_min = 2

t_slider_max = None
t_slider_min = 5


def startDash(slc, k_len, p, t):
    if slc is not None:
        global process
        global k_p_slider_max
        global t_slider_max
        process = initializeData.initData(slc, slc, k_len, p, t)
        k_p_slider_max = Processing.getSeqLen(process)
        # t_slider_max: size of both sets added
        t_slider_max = len(Processing.getProfilObj1(process).getProfile()) + \
                       len(Processing.getProfilObj2(process).getProfile())
    app.run_server(debug=False)


def markSliderRange(min, max):
    mark = {}
    for i in range(min, max + 1):
        mark[i] = str(i)
    return mark


def specialSliderRange(max):
    j = t_slider_min
    mark = {}
    i = 0
    while i < 9:
        if "5" in str(j):
            j = j * 2
        else:
            j = j * 5

        if j <= max:
            mark[i] = str(j)
        else:
            break
        i += 1
    mark[i] = 'all'
    return mark


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.title = "k-Mer Dash"

app.layout = dbc.Container([
    # ------------------------------------------ Store -----------------------------------------------------------------
    dcc.Store(id='memory', storage_type='memory'),

    # -------------------------------------------------------------------------------------------------------------------
    dbc.Card([
        dbc.Row([
            dbc.Col(
                dbc.CardBody([
                    html.H3("Menu"),
                    html.Br(),
                    html.Br(),
                    # ------------------------- Choose Fasta-Files -----------------------------------------------------
                    dbc.Button("Choose Files", color="primary", className="mr-1", disabled=True),
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
                        disabled=True),
                    dbc.Select(
                        id="file2",
                        options=[
                            {"label": "File 1", "value": "1"},
                            {"label": "File 2", "value": "2"},
                        ],
                        # value="2"
                        disabled=True),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    # ------------------------------------------- K ----------------------------------------------------
                    html.H6("K-mer length:"),
                    dcc.Slider(
                        id='k',
                        min=0,
                        max=10,
                        step=1,
                        value=5,
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
                        min=0,
                        max=10,
                        step=1,
                        value=10,
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
                    html.Br(),
                    html.Br(),
                    html.Br(),

                    # ---------------------------------------- Copy Table ------------------------------------------
                    dbc.Button("Copy K-Mer Table", color="primary", className="mr-1", id="copy"),
                    html.Div(id="output")

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
                dbc.Spinner(children=[

                    dbc.Card(id="msa", children=[], style={
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
    [
        dash.dependencies.Output("k", "min"),
        dash.dependencies.Output("k", "max"),
        dash.dependencies.Output("k", "marks"),
        dash.dependencies.Output("k", "value"),
        dash.dependencies.Output("peak", "min"),
        dash.dependencies.Output("peak", "max"),
        dash.dependencies.Output("peak", "marks"),
        dash.dependencies.Output("peak", "value"),
        dash.dependencies.Output("top", "min"),
        dash.dependencies.Output("top", "max"),
        dash.dependencies.Output("top", "marks"),
        dash.dependencies.Output("top", "value"),
    ],
    [dash.dependencies.Input("file1", "value"),
     dash.dependencies.Input("file2", "value"),
     ],
)
def updateSliderRange(file1, file2):
    k_val = Processing.getSettings(process).getK()
    p_val = Processing.getSettings(process).getPeak()
    t_val = Processing.getSettings(process).getTop()
    k_slider_max = k_p_slider_max - 1
    peak_min = 1
    k_range = markSliderRange(k_p_slider_min, k_slider_max)
    peak_range = markSliderRange(peak_min, k_p_slider_max)
    top_range = specialSliderRange(t_slider_max)

    t_max = len(top_range) - 1
    t_min = 0

    return k_p_slider_min, k_slider_max, k_range, k_val, \
           peak_min, k_p_slider_max, peak_range, p_val, \
           t_min, t_max, top_range, t_val


# ------------------------------------ Store Callback ------------------------------------------------------------------

@app.callback(dash.dependencies.Output('memory', 'data'),
              dash.dependencies.Input('k', 'value'),
              dash.dependencies.Input('peak', 'value'),
              dash.dependencies.Input('top', 'value'),
              dash.dependencies.State('memory', 'data'),
              prevent_inital_call=True)
def updateData(k, peak, top, data):

    # translate top_val from slider to real top value
    top_range = specialSliderRange(t_slider_max)
    if top in list(top_range.keys()):
        top = top_range[top]

        if top is 'all':
            top = t_slider_max
        else:
            top = int(top)

    selected = Processing.getSettings(process).getSelected()
    newProcess = initializeData.initData(selected, selected, k, peak, top)

    topK = Processing.getTopKmer(newProcess).copy()
    kmer = topK.index
    topK["K-Mer"] = kmer
    topK[""] = ["" for i in range(0, len(topK))]
    topK = topK[["", "K-Mer", "Frequency", "File"]]
    topK = topK.sort_values(by="Frequency", ascending=False)
    topK_table = [
        dash_table.DataTable(columns=[{"name": i, "id": i} for i in topK.columns], data=topK.to_dict('records'),
                             style_table={'overflow-x': 'hidden'},
                             style_cell={'textAlign': 'center'},
                             sort_action='native')]

    algn1, algn2, f1_name, f2_name = initializeData.getAlignmentData(newProcess)
    algn1 = pd.DataFrame(algn1)
    algn2 = pd.DataFrame(algn2)
    if not (len(algn1) is 0) and not (len(algn2) is 0):
        algn1.columns = [f1_name]
        algn1[f2_name] = algn2
        msas = [
            dash_table.DataTable(columns=[{"name": i, "id": i} for i in algn1.columns], data=algn1.to_dict('records'),
                                 style_table={'overflow-x': 'hidden'},
                                 style_cell={'textAlign': 'center'})]
    else:
        msas = [dash_table.DataTable(columns=["", ""], data=[],
                                     style_table={'overflow-x': 'hidden'},
                                     style_cell={'textAlign': 'center'})]

    scatter = initializeData.getScatterPlot(newProcess)

    pca_12, file1, file2 = initializeData.getPCA(newProcess)
    pcas = [pca_12, file1, file2]

    data = {'topK': topK_table, 'msas': msas, 'scatter': scatter, 'pcas': pcas}


    return data


@app.callback(dash.dependencies.Output('scatter', 'figure'),
              dash.dependencies.Input('memory', 'modified_timestamp'),
              dash.dependencies.State('memory', 'data'))
def updateScatter(ts, data):
    if ts is None:
        raise PreventUpdate
    return data.get('scatter', 0)


@app.callback([dash.dependencies.Output('PCA1', 'figure'),
               dash.dependencies.Output('PCA2', 'figure'),
               dash.dependencies.Output('Tab1', 'label'),
               dash.dependencies.Output('Tab2', 'label')],
              dash.dependencies.Input('memory', 'modified_timestamp'),
              dash.dependencies.State('memory', 'data'))
def updateScatter(ts, data):
    if ts is None:
        raise PreventUpdate
    pca_data = data.get('pcas', 0)
    pca1 = pca_data[0][0]
    pca2 = pca_data[0][1]
    file1 = pca_data[1]
    file2 = pca_data[2]
    return [pca1, pca2, file1, file2]


@app.callback(dash.dependencies.Output('topK', 'children'),
              dash.dependencies.Input('memory', 'modified_timestamp'),
              dash.dependencies.State('memory', 'data'))
def updateTopK(ts, data):
    if ts is None:
        raise PreventUpdate
    return data.get('topK', 0)


@app.callback(dash.dependencies.Output('msa', 'children'),
              dash.dependencies.Input('memory', 'modified_timestamp'),
              dash.dependencies.State('memory', 'data'))
def updateMSA(ts, data):
    if ts is None:
        raise PreventUpdate
    return data.get('msas', 0)
