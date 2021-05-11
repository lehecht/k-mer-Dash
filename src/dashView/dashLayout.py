import dash
import dash_core_components as dcc
import dash_table
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
from dash.exceptions import PreventUpdate

from src.processing import Processing
from src.dashView import initializeData

# selected files, which are processed
# read-only
selected = None
file_list = None


# starts dash
# slc: input data
# port: port
def startDash(files, slc, port):
    global file_list
    global selected
    selected = slc
    file_list = files
    app.run_server(debug=False, host='0.0.0.0', port=port)


# calculates slider ranges
# peak-boolean sets first value to 'none' (for peak-slider)
def markSliderRange(min_val, max_val, peak):
    mark = {}
    if peak:
        min_val += 1
        mark[0] = 'none'
    for i in range(min_val, max_val + 1):
        mark[i] = str(i)
    return mark


# calculation of slider ranges in steps [50, 100, 500, 1000,...,all]
def specialSliderRange(min_val, max_val):
    j = min_val
    mark = {}
    i = 0
    while i < 9:
        if "5" in str(j):
            j = j * 2
        else:
            j = j * 5

        if j <= max_val:
            mark[i] = str(j)
        else:
            break
        i += 1
    mark[i] = 'all'
    return mark


# ------------------------------------------- Dash-Layout --------------------------------------------------------------

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.title = "k-Mer Dash"

app.layout = dbc.Container([
    # ---------------------------------------------- Info-Alert --------------------------------------------------------
    dbc.Alert(
        "Top-Slider changed. "
        "Please note, that current top-value is last 'all'-value. "
        "It does not need to be exact the present value on the current top-slider. "
        "To use values of current top-slider, just select any other value.",
        id="all",
        is_open=False,
        duration=30000,
        color="info"
    ),
    # ------------------------------------------ Store -----------------------------------------------------------------
    dbc.Spinner(children=[dcc.Store(id='memory', storage_type='memory')],
                color="primary", fullscreen=True),

    # -------------------------------------------------------------------------------------------------------------------
    dbc.Card([
        dbc.Row([
            dbc.Col(
                dbc.CardBody([
                    html.H3("Menu"),
                    html.Br(),
                    html.Br(),
                    # ------------------------------------- Select File1 And File 2 ------------------------------------
                    html.H6("Selected Files:"),
                    dbc.Select(
                        id="file1",
                        options=[]),
                    dbc.Select(
                        id="file2",
                        options=[]),
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
                        value=3,
                        marks=markSliderRange(0, 10, False)
                    ),
                    html.Br(),
                    # ------------------------------------------ top ---------------------------------------------------
                    html.H6("Top-values:"),
                    dcc.Slider(
                        id='top',
                        min=0,
                        max=10,
                        step=1,
                        value=0,
                        marks=markSliderRange(0, 10, False)
                    ),
                    html.Br(),
                    # ----------------------------------------- Peak ---------------------------------------------------
                    html.H6("Peak-position:"),
                    dcc.Slider(
                        id='peak',
                        min=1,
                        max=10,
                        step=1,
                        value=0,
                        marks=markSliderRange(0, 10, True)
                    ),
                    html.Br(),
                    # -------------------------------- Highlighted Feature ---------------------------------------------
                    html.H6("Highlighted Feature:"),
                    dbc.Select(
                        id="Feature",
                        options=[
                            {"label": "Frequency", "value": "1"},
                            {"label": "T Occurrences", "value": "2"},
                        ],
                        value="1"
                    ),
                    html.Br(),
                    html.Br(),
                    html.Br(),

                ], style={
                    'height': '100vh',
                    'left': '0px',
                    'background': 'lightgrey'}),
                width=2,
                style={"padding-right": '0px',
                       "padding-left": '0px',
                       'margin-right': '0px'}),

            # --------------------------------------- ScatterPlot ------------------------------------------------------
            dbc.Col([
                dbc.Card([
                    dbc.Spinner(children=[dcc.Graph(figure={}, id="scatter", style={'height': '50vh'})],
                                color="primary", spinner_style={'position': 'absolute',
                                                                'top': '50%',
                                                                'left': '50%'
                                                                }),

                ], style={
                    'background': '#f2f2f2', 'height': '50vh'}, outline=True),

                # -------------------------------------------- TopK ----------------------------------------------------
                dbc.Spinner(children=[dbc.Card(id="topK", children=[], style={
                    'background': '#f2f2f2', 'height': '49vh', 'overflow-y': 'scroll'}, outline=True)],
                            color="primary", spinner_style={'position': 'absolute',
                                                            'top': '50%',
                                                            'left': '50%'
                                                            }),
            ],
                width=5,
                style={"padding-right": '5px',
                       "padding-left": '10px'}),

            # ------------------------------------------------- PCAs ---------------------------------------------------
            dbc.Col(
                [dbc.Card([
                    dbc.Spinner(children=[
                        dcc.Tabs(id='tabs-example', value='Tab1', children=[
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
                                 )], color="primary",
                        spinner_style={'position': 'absolute',
                                       'top': '50%',
                                       'left': '50%'
                                       }),

                ], style={
                    'background': '#f2f2f2', 'height': '50vh'}, outline=True),

                    # ------------------------------------------- MSA --------------------------------------------------
                    dbc.Spinner(children=[dbc.Card(id="msa", children=[], style={
                        'background': '#f2f2f2', 'height': '49vh', 'overflow-y': 'scroll'}, outline=True)],
                                color="primary", spinner_style={'position': 'absolute',
                                                                'top': '50%',
                                                                'left': '50%'
                                                                }),
                ],
                width=5,
                style={"padding-right": '0px',
                       "padding-left": '0px'}
            )

        ], style={'padding-top': '0px', 'padding-bottom': '0px', 'margin-top': '0px', 'margin-bottom': '0px',
                  'margin-left': '0px', 'padding-left': '0px'},
            className="mw-100 mh-100"
        ),

    ],
        className="mw-100 mh-100"),
], className="mw-100 mh-100", style={'left': '0px', 'margin-left': '0px', 'padding': '0px'})


# ------------------------------------ Store Callback ------------------------------------------------------------------

@app.callback(
    dash.dependencies.Output('memory', 'data'),
    dash.dependencies.Input('k', 'value'),
    dash.dependencies.Input('peak', 'value'),
    dash.dependencies.Input('top', 'value'),
    dash.dependencies.Input('Feature', 'value'),
    dash.dependencies.State('memory', 'data'),
)
# calculates new data for tables/diagrams
# k: kmer length
# peak: peak: peak-position, where sequences should be aligned
# top: number of best values
# pca_feature: number of T or kmer-Frequency for pcas
# data: storage to share data between callbacks
def updateData(k, peak, top, pca_feature, data):
    # initial values
    t_slider_min = 5
    if data is None:
        t_slider_max = 50
    else:
        t_slider_max = data['big_profile_size']

    # translate top_val from slider to real top value
    top_range = specialSliderRange(t_slider_min, t_slider_max)
    # if last top-slider was bigger than current one, adapt all value
    if top >= len(top_range):
        top = len(top_range) - 1
    if top in list(top_range.keys()):
        top = top_range[top]
        if top is 'all':
            top = t_slider_max
        else:
            top = int(top)

    if peak is 0:
        peak = None

    new_process = initializeData.initData(selected, selected, k, peak, top, pca_feature)

    # calculate top-table
    top_k = Processing.getTopKmer(new_process).copy()
    kmer = top_k.index
    top_k["K-Mer"] = kmer
    top_k[""] = ["" for i in range(0, len(top_k))]
    top_k = top_k[["", "K-Mer", "Frequency", "File"]]
    top_k = top_k.sort_values(by="Frequency", ascending=False)
    top_k_table = [
        dash_table.DataTable(columns=[{"name": i, "id": i} for i in top_k.columns], data=top_k.to_dict('records'),
                             style_table={'overflow-x': 'hidden'},
                             style_cell={'textAlign': 'center'},
                             export_format="csv",
                             sort_action='native')]

    # calculate MSA
    try:
        algn1, algn2, f1_name, f2_name = initializeData.getAlignmentData(new_process)
    except ValueError:  # is thrown is there are too many entries
        algn1 = ['Alignment could not be calculated']
        algn2 = ['Alignment could not be calculated']
        f1_name = top_k['File'].drop_duplicates().values.tolist()[1]
        f2_name = top_k['File'].drop_duplicates().values.tolist()[0]

    # if cols differ in their length, need to do some adaptions

    if (len(algn1) > 0) and (len(algn2) > 0):
        algn1_df = pd.DataFrame(columns=[f1_name], data=algn1)
        algn2_df = pd.DataFrame(columns=[f2_name], data=algn2)
        algn1_df = pd.concat([algn1_df, algn2_df], ignore_index=False, axis=1)
        msas = [
            dash_table.DataTable(columns=[{"name": i, "id": i} for i in algn1_df.columns],
                                 data=algn1_df.to_dict('records'),
                                 style_table={'overflow-x': 'hidden'},
                                 style_cell={'textAlign': 'center'},
                                 export_format="csv")]
    elif len(algn1) == 0 and len(algn2) == 0:
        algn1_df = pd.DataFrame(data=[])
        algn1_df[f1_name] = ''
        algn1_df[f2_name] = ''
        msas = [dash_table.DataTable(columns=[{"name": i, "id": i} for i in algn1_df.columns],
                                     data=algn1_df.to_dict('records'),
                                     style_table={'overflow-x': 'hidden'},
                                     style_cell={'textAlign': 'center'},
                                     export_format="csv")]

    else:
        if len(algn1) == 0:
            algn1_df = pd.DataFrame(algn2)
            algn1_df.columns = [f2_name]
            algn1_df[f1_name] = ''
        else:
            algn1_df = pd.DataFrame(algn1)
            algn1_df.columns = [f1_name]
            algn1_df[f2_name] = ''

        msas = [dash_table.DataTable(columns=[{"name": i, "id": i} for i in algn1_df.columns],
                                     data=algn1_df.to_dict('records'),
                                     style_table={'overflow-x': 'hidden'},
                                     style_cell={'textAlign': 'center'},
                                     export_format="csv")]

    # calculate scatterplot

    scatter = initializeData.getScatterPlot(new_process)

    # calculate PCAs

    pca_12, file1, file2 = initializeData.getPCA(new_process)
    pcas = [pca_12, file1, file2]

    # maximal slider value before value 'all'
    # depends on smallest profile because otherwise all entries would be displayed

    big_profile_size = max(
        [len(new_process.getProfilObj1().getProfile()), len(new_process.getProfilObj2().getProfile())])

    seq_len = new_process.getSeqLen()

    data = {'topK': top_k_table, 'msas': msas, 'scatter': scatter, 'pcas': pcas, 'big_profile_size': big_profile_size,
            'seqLen': seq_len}

    return data


# --------------------------------------- File Dropdown Updater --------------------------------------------------------
@app.callback([
    dash.dependencies.Output("file1", "value"),
    dash.dependencies.Output("file2", "value"),
    dash.dependencies.Input('memory', 'modified_timestamp'),
])
def initialSelect(ts):
    if ts is None:
        f1 = "0"
        f2 = "1"
    else:
        raise PreventUpdate

    return f1,f2

@app.callback([
    dash.dependencies.Output("file1", "options"),
    dash.dependencies.Input("file2", "value"),
])
def updateFile1Dropdown(f2):
    return updateFileList(f2)


@app.callback([
    dash.dependencies.Output("file2", "options"),
    dash.dependencies.Input("file1", "value"),
])
def updateFile2Dropdown(f1):
    return updateFileList(f1)


def updateFileList(val):
    option = [
        {'label': file_list[i], 'value': str(i)} if not (str(i) == val)
        else {'label': file_list[i], 'value': str(i), 'disabled': True}
        for i in range(0, len(file_list))]

    return [option]


# --------------------------------------- Slider Values Updater --------------------------------------------------------


@app.callback(
    [
        dash.dependencies.Output("k", "min"),
        dash.dependencies.Output("k", "max"),
        dash.dependencies.Output("k", "marks"),
        dash.dependencies.Output("peak", "min"),
        dash.dependencies.Output("peak", "max"),
        dash.dependencies.Output("peak", "marks"),
        dash.dependencies.Output("top", "min"),
        dash.dependencies.Output("top", "max"),
        dash.dependencies.Output("top", "marks"),
        dash.dependencies.Output("all", "is_open"),
    ],
    [
        dash.dependencies.Input("file1", "value"),
        dash.dependencies.Input("file2", "value"),
        dash.dependencies.Input('memory', 'modified_timestamp'),
        dash.dependencies.State('memory', 'data'),
        dash.dependencies.State('top', 'marks'),
        dash.dependencies.State('all', 'is_open'),
        dash.dependencies.State('top', 'value')
    ],
)
# calculates slider ranges (marks)
# fil1/file2: input file
# ts: timestamp when data was modified
# data: storage to share data between callbacks
# old_marks: last old top-slider dictionary
# is_open: bool, which shows alert status (hidden/open)
# top_val: current top-value
def updateSliderRange(file1, file2, ts, data, old_marks, is_open, top_val):
    if ts is None:
        raise PreventUpdate
    k_p_slider_max = data['seqLen']
    k_p_slider_min = 2
    t_slider_max = data['big_profile_size']
    t_slider_min = 5

    k_slider_max = k_p_slider_max - 1
    peak_min = 0

    # calculation of new slider ranges, if files were changed or if dataframe-size was changed (for top-slider)

    k_range = markSliderRange(k_p_slider_min, k_slider_max, False)
    peak_range = markSliderRange(peak_min, k_p_slider_max, True)
    top_range = specialSliderRange(t_slider_min, t_slider_max)

    # if last top-value was 'all' and new top-slider is bigger than last, an alert is triggered
    while (len(old_marks) - 1) < top_val:
        top_val = top_val - 1

    if (len(old_marks) < len(top_range)) and (old_marks[str(top_val)] == 'all'):
        is_open = True

    t_max = len(top_range) - 1
    t_min = 0

    return k_p_slider_min, k_slider_max, k_range, peak_min, k_p_slider_max, peak_range, t_min, t_max, top_range, is_open


# --------------------------------------------- Diagram/Table Updater --------------------------------------------------

# Tables/Diagrams only get updated figures/datatables here


@app.callback(dash.dependencies.Output('scatter', 'figure'),
              dash.dependencies.Input('memory', 'modified_timestamp'),
              dash.dependencies.State('memory', 'data'))
# ts: timestamp when data was modified
# data: storage to share data between callbacks
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
# ts: timestamp when data was modified
# data: storage to share data between callbacks
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
# ts: timestamp when data was modified
# data: storage to share data between callbacks
def updateTopK(ts, data):
    if ts is None:
        raise PreventUpdate
    return data.get('topK', 0)


@app.callback(dash.dependencies.Output('msa', 'children'),
              dash.dependencies.Input('memory', 'modified_timestamp'),
              dash.dependencies.State('memory', 'data'))
# ts: timestamp when data was modified
# data: storage to share data between callbacks
def updateMSA(ts, data):
    if ts is None:
        raise PreventUpdate
    return data.get('msas', 0)
