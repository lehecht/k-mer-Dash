import dash
import dash_core_components as dcc
import dash_table
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import os
from dash.exceptions import PreventUpdate
import dash_bio as dashbio

from src.processing import Processing
from src.dashView import initializeData

# files, which are processed
# read-only
file_list = None
struct_data = None


# starts dash
# file_list: input data
# sec_struct_data: input structural data
# port: port
def startDash(files, port, sec_struct_data):
    global file_list
    global struct_data
    file_list = files
    struct_data = sec_struct_data
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


# range() function for floats
# start: start-value which is head of list
# step: steps between two values
# run: number of loop runs
def float_range(start, step, run):
    for_list = [start]
    for i in range(1, run):
        next_step = start + step * i
        for_list.append(next_step)
    return for_list


# checks if custom normalization rates sum up to one
# parameters (e.g. ee,ss,etc. ..): rate for 2-mer
def check_sum(ee, ss, ii, mm, bb, si, i_s, sm, ms, es, se, hh, hs, sh, sb, bs):
    custom_rates = [ee, ss, ii, mm, bb, si, i_s, sm, ms, es, se, hh, hs, sh, sb, bs]
    k_mer_sum = round(sum(custom_rates), 1)
    check_passed = bool(k_mer_sum == 1)

    return check_passed


# ------------------------------------------- Dash-Layout --------------------------------------------------------------

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.title = "k-Mer Dash"

app.layout = dbc.Container([
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
                    # ------------------------------------- Select File1 And File 2 ------------------------------------
                    html.H6("Selected Files:", id="sel_files_header"),
                    dbc.Select(
                        id="file1",
                        options=[]),
                    dbc.Select(
                        id="file2",
                        options=[]),
                    dbc.Tooltip(
                        "Files containing DNA nucleotide-sequences used for k-mer visualization",
                        target="sel_files_header"
                    ),
                    html.Br(),
                    html.Br(),
                    # ------------------------------------- Select Structure Files -------------------------------------
                    html.H6("Selected Structure Files:", id="struc_files_header"),
                    dbc.Select(
                        id="file3",
                        options=[{"label": "-", "value": "0"}],
                        value="0"),
                    dbc.Select(
                        id="file4",
                        options=[{"label": "-", "value": "0"}],
                        value="0"),
                    dbc.Tooltip(
                        "Files containing element-strings used for RNA structure heatmaps(s)",
                        target="struc_files_header"
                    ),
                    html.Br(),
                    html.Br(),
                    # ------------------------------------------- K ----------------------------------------------------
                    html.H6("K-mer length:", id="k_header"),
                    dcc.Slider(
                        id='k',
                        min=0,
                        max=10,
                        step=1,
                        value=3,
                        marks=markSliderRange(0, 10, False)
                    ),
                    dbc.Tooltip(
                        "Length of visualized substrings (k-mer)",
                        target="k_header"
                    ),
                    html.Br(),
                    # ----------------------------------------- Peak ---------------------------------------------------
                    html.H6("Peak-position:", id="peak_header"),
                    dcc.Slider(
                        id='peak',
                        min=1,
                        max=10,
                        step=1,
                        value=0,
                        marks=markSliderRange(0, 10, True)
                    ),
                    dbc.Tooltip(
                        "Highlighted position in sequence (e.g. assumed binding position "
                        "of protein in given sequences)",
                        target="peak_header"
                    ),
                    html.Br(),
                    # ------------------------------------------ top ---------------------------------------------------
                    html.H6("Top-values:", id="top_header"),
                    dbc.Select(
                        id='top',
                        options=[
                            {'label': '10', 'value': '0'},
                            {'label': '20', 'value': '1'},
                            {'label': '50', 'value': '2'},
                            {'label': '100', 'value': '3'}
                        ],
                        value="0"
                    ),
                    dbc.Tooltip(
                        "Number of <top> highest k-mer occurrences",
                        target="top_header"
                    ),
                    html.Br(),
                    html.Br(),
                    # -------------------------------- Highlighted Feature ---------------------------------------------
                    html.H6("Highlighted feature:", id="feature_header"),
                    dbc.Select(
                        id="Feature",
                        options=[
                            {"label": "Frequency", "value": "1"},
                            {"label": "T Occurrences", "value": "2"},
                            {"label": "A Occurrences", "value": "3"},
                            {"label": "C Occurrences", "value": "4"},
                            {"label": "G Occurrences", "value": "5"},
                        ],
                        value="1"
                    ),
                    dbc.Tooltip(
                        "Highlighted/Colored property of PCAs",
                        target="feature_header"
                    ),
                    html.Br(),
                    html.Br(),
                    # ------------------------------- Options structural data ------------------------------------------
                    dbc.ButtonGroup(
                        [dbc.Button("Extended options", id="opt_btn_open"),
                         # dbc.Button("Export PDF", id="ex_btn",disabled=True)
                         ],
                        size="md",
                        className="mr-1",
                    ),
                    dbc.Tooltip(
                        "Options for structural data visualization",
                        target="opt_btn_open"
                    ),
                    dbc.Modal(
                        [
                            dbc.ModalHeader("Options for structural data visualization"),
                            dbc.ModalBody(children=[
                                dcc.Checklist(
                                    id="sec_peak",
                                    options=[{'label': 'show only peak positions', 'value': 'peaking'}],
                                    inputStyle={'margin-right': '3px'},
                                ),
                                dbc.Tooltip(
                                    "Only show peak positions in RNA structure Heatmap(s)",
                                    target="sec_peak"
                                ),
                                html.Br(),
                                html.Div("Normalization:", id="norm_header",
                                         style={'font-weight': 'bold', 'padding-bottom': '10px'}),
                                html.Div("ERROR: sum of custom rates should be equal to 1", id="error",
                                         style={'font-weight': 'bold', 'color': 'red',
                                                'padding-bottom': '10px'}, hidden=True),
                                html.Div("ERROR: only numerical values between zero and one allowed", id="error_type",
                                         style={'font-weight': 'bold', 'color': 'red',
                                                'padding-bottom': '10px'}, hidden=True),
                                dcc.RadioItems(
                                    id="db",
                                    options=[
                                        {'label': 'none', 'value': 'none'},
                                        {'label': 'use A.thaliana database', 'value': 'at_db'},
                                        {'label': 'use custom k-mer rates', 'value': 'custom_vals'}
                                    ],
                                    value='none',
                                    labelStyle={'display': 'block'},
                                    inputStyle={'margin-right': '3px'}
                                ),
                                dbc.Tooltip(
                                    "Used data for normalization of structural data",
                                    target="norm_header"
                                ),
                                html.Div(id="norm_input", children=[
                                    html.Table(children=[
                                        html.Tr(children=[
                                            html.Td(children=[
                                                html.Div("EE"),
                                                dbc.Input(id="EE", type="number", style={'width': '100px'}, max=1,
                                                          min=0, step=0.001, value=0)], ),
                                            html.Td(children=[
                                                html.Div("ES"),
                                                dbc.Input(id="ES", type="number", style={'width': '100px'}, max=1,
                                                          min=0, step=0.001, value=0)], ),
                                            html.Td(children=[
                                                html.Div("SS"),
                                                dbc.Input(id="SS", type="number", style={'width': '100px'}, max=1,
                                                          min=0, step=0.001, value=0)], )
                                        ]),
                                        html.Tr(children=[
                                            html.Td(children=[
                                                html.Div("SI"),
                                                dbc.Input(id="SI", type="number", style={'width': '100px'}, max=1,
                                                          min=0, step=0.001, value=0), ], ),
                                            html.Td(children=[
                                                html.Div("IS"),
                                                dbc.Input(id="IS", type="number", style={'width': '100px'}, max=1,
                                                          min=0, step=0.001, value=0), ], ),
                                            html.Td(children=[
                                                html.Div("II"),
                                                dbc.Input(id="II", type="number", style={'width': '100px'}, max=1,
                                                          min=0, step=0.001, value=0), ], )
                                        ]),
                                        html.Tr(children=[
                                            html.Td(children=[
                                                html.Div("SH"),
                                                dbc.Input(id="SH", type="number", style={'width': '100px'}, max=1,
                                                          min=0, step=0.001, value=0), ], ),
                                            html.Td(children=[
                                                html.Div("HS"),
                                                dbc.Input(id="HS", type="number", style={'width': '100px'}, max=1,
                                                          min=0, step=0.001, value=0), ], ),
                                            html.Td(children=[
                                                html.Div("HH"),
                                                dbc.Input(id="HH", type="number", style={'width': '100px'}, max=1,
                                                          min=0, step=0.001, value=0), ], )
                                        ]),
                                        html.Tr(children=[
                                            html.Td(children=[
                                                html.Div("SM"),
                                                dbc.Input(id="SM", type="number", style={'width': '100px'}, max=1,
                                                          min=0, step=0.001, value=0), ], ),
                                            html.Td(children=[
                                                html.Div("MS"),
                                                dbc.Input(id="MS", type="number", style={'width': '100px'}, max=1,
                                                          min=0, step=0.001, value=0), ], ),
                                            html.Td(children=[
                                                html.Div("SE"),
                                                dbc.Input(id="SE", type="number", style={'width': '100px'}, max=1,
                                                          min=0, step=0.001, value=0), ], ),

                                        ]),
                                        html.Tr(children=[
                                            html.Td(children=[
                                                html.Div("BB"),
                                                dbc.Input(id="BB", type="number", style={'width': '100px'}, max=1,
                                                          min=0, step=0.001, value=0), ], ),
                                            html.Td(children=[
                                                html.Div("BS"),
                                                dbc.Input(id="BS", type="number", style={'width': '100px'}, max=1,
                                                          min=0, step=0.001, value=0), ], ),
                                            html.Td(children=[
                                                html.Div("SB"),
                                                dbc.Input(id="SB", type="number", style={'width': '100px'}, max=1,
                                                          min=0, step=0.001, value=0), ], ),

                                        ]),
                                        html.Tr(children=[
                                            html.Td(children=[
                                                html.Div("MM"),
                                                dbc.Input(id="MM", type="number", style={'width': '100px'}, max=1,
                                                          min=0, step=0.001, value=0), ], ),
                                            html.Td(children=[]),
                                            html.Td(children=[
                                                html.Br(),
                                                dbc.Button("Reset", id="opt_btn_reset",
                                                           style={'margin': 'auto'})]),
                                            dbc.Tooltip(
                                                "Reset table",
                                                target="opt_btn_reset"
                                            ),

                                        ])
                                    ], style={'width': '100%'}
                                    )
                                ], style={'display': 'block'}, hidden=True),
                            ]),
                            dbc.ModalFooter(children=[
                                dbc.ButtonGroup(
                                    [dbc.Button("Apply", id="opt_btn_apply"),
                                     dbc.Button("Close", id="opt_btn_close")],
                                    className="mr-1",
                                ),

                            ]
                            ),

                        ],
                        id="ex_options",
                        backdrop='static',
                        centered=True
                    ),

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
                    dbc.Spinner(children=[
                        dcc.Tabs(value="s-tab", children=[
                            dcc.Tab(label="Scatterplot", value='s-tab', id="s-tab1", children=[
                                dcc.Graph(figure={}, id="scatter", style={'height': '40vh'})
                            ]),
                            # -------------------------------------- FornaContainer ------------------------------------
                            dcc.Tab(value='r-tab', id="s-tab2", children=[
                                dbc.Card(
                                    dashbio.FornaContainer(
                                        id='forna', height='300', width='400', colorScheme='custom'
                                    ),
                                    className="w-100 p-3",
                                ),
                            ]),
                            dcc.Tab(value='r-tab2', id="s-tab3", children=[
                                dbc.Card(
                                    dashbio.FornaContainer(
                                        id='forna2', height='300', width='400', colorScheme='custom'
                                    ),
                                    className="w-100 p-3",
                                ),
                            ])
                        ]),
                        dbc.Tooltip(
                            "Scatterplot of k-mer occurences from selected files containing "
                            "nucleotide sequences",
                            target="s-tab1"
                        ),
                        dbc.Tooltip(
                            "Visualization of arbitrary RNA structure, highlighting k-mer occurrences of "
                            "element strings from first selected structural data file",
                            target="s-tab2"
                        ),
                        dbc.Tooltip(
                            "Visualization of arbitrary RNA structure, highlighting k-mer occurrences of "
                            "element strings from second selected structural data file",
                            target="s-tab3"
                        ),
                    ],
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
                                 ),
                        dbc.Tooltip(
                            "Principal component analysis (PCA) of first selected file containing nucleotide sequences",
                            target="Tab1"
                        ),
                        dbc.Tooltip(
                            "Principal component analysis (PCA) of "
                            "second selected file containing nucleotide sequences",
                            target="Tab2"
                        ),
                    ], color="primary",
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
    [dash.dependencies.Output('memory', 'data')],
    [dash.dependencies.Input('file1', 'value'),
     dash.dependencies.Input('file2', 'value'),
     dash.dependencies.Input('file3', 'value'),
     dash.dependencies.Input('file4', 'value'),
     dash.dependencies.Input('k', 'value'),
     dash.dependencies.Input('peak', 'value'),
     dash.dependencies.Input('top', 'value'),
     dash.dependencies.Input('Feature', 'value'),
     dash.dependencies.Input('opt_btn_apply', 'n_clicks'),
     dash.dependencies.State('sec_peak', 'value'),
     dash.dependencies.State('EE', 'value'),
     dash.dependencies.State('SS', 'value'),
     dash.dependencies.State('II', 'value'),
     dash.dependencies.State('MM', 'value'),
     dash.dependencies.State('BB', 'value'),
     dash.dependencies.State('SI', 'value'),
     dash.dependencies.State('IS', 'value'),
     dash.dependencies.State('SM', 'value'),
     dash.dependencies.State('MS', 'value'),
     dash.dependencies.State('ES', 'value'),
     dash.dependencies.State('SE', 'value'),
     dash.dependencies.State('HH', 'value'),
     dash.dependencies.State('HS', 'value'),
     dash.dependencies.State('SH', 'value'),
     dash.dependencies.State('SB', 'value'),
     dash.dependencies.State('BS', 'value'),
     dash.dependencies.State('db', 'value'),
     dash.dependencies.State('memory', 'data')]
)
# calculates new data for tables/diagrams
# k: k-mer length
# peak: peak: peak-position, where sequences should be aligned
# top: number of best values
# pca_feature: number of T or k-mer-Frequency for PCAs
# apply_options_btn: n_clicks of apply-button within modal
# sec_peak: peak status (-1: no data, 0: False, 1: True) for structural data
# parameters (e.g. ee,ss,etc. ...): custom rates of 2-mer
# norm_option: normalization option (none, for A.thaliana, custom)
# data: storage to share data between callbacks
def updateData(f1, f2, f3, f4, k, peak, top, pca_feature, apply_options_btn, sec_peak,
               ee, ss, ii, mm, bb, si, i_s, sm, ms, es, se, hh, hs, sh, sb, bs, norm_option, data):
    normalization_vector = None

    selected_struc = None

    normalization_status = -1

    no_peak = 0

    no_sec_peak_false = 0

    no_sec_peak_true = 1

    # if custom rates given, check input
    if apply_options_btn is not None and norm_option == 'custom_vals':
        normalization_status = 1
        custom_rates = [ee, ss, ii, mm, bb, si, i_s, sm, ms, es, se, hh, hs, sh, sb, bs]
        # if input contains non-digits, prevent update
        labels = ["EE", "SS", "II", "MM", "BB", "SI", "IS", "SM", "MS", "ES", "SE", "HH", "HS", "SH", "SB", "BS"]
        if None in custom_rates:
            return dash.no_update
        check_sum_passed = check_sum(ee, ss, ii, mm, bb, si, i_s, sm, ms, es, se, hh, hs, sh, sb, bs)
        # if sum of custom rates is one, do normalization
        if check_sum_passed:
            normalization_vector = dict(zip(labels, custom_rates))
        # otherwise prevent update
        else:
            return dash.no_update
    elif apply_options_btn is not None and norm_option == 'at_db':
        normalization_status = 0

    # translate dropdown value into real value
    top_opt_val = {'0': 10, '1': 20, '2': 50, '3': 100}

    top = top_opt_val[top]

    if peak == no_peak:
        peak = None

    if sec_peak == ['peaking']:
        no_sec_peak = no_sec_peak_false  # =False
    else:
        no_sec_peak = no_sec_peak_true  # =True

    # initialize (structural) data for calculations
    if data is None:
        selected = [file_list[0], file_list[1]]

        if struct_data is not None:
            if len(struct_data) > 1:
                selected_struc = [struct_data[0], struct_data[1]]
            else:
                selected_struc = [struct_data[0]]
    else:
        selected = [file_list[int(f1)], file_list[int(f2)]]
        if struct_data is not None:
            if len(struct_data) > 1:
                selected_struc = [struct_data[int(f3)], struct_data[int(f4)]]
            else:
                selected_struc = [struct_data[int(f3)]]

    new_process = initializeData.initData(selected, selected, k, peak, top, pca_feature, selected_struc, no_sec_peak)

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

    algn1, algn2, f1_name, f2_name = initializeData.getAlignmentData(new_process)

    # if columns differ in their length, need to do some adaptions
    if (len(algn1) > 1 and len(algn2) > 1) or (len(algn1) <= 1 and len(algn2) <= 1):
        if len(algn1) <= 1 and len(algn2) <= 1:
            algn1_df = pd.DataFrame(columns=[f1_name], data=['No data to align'])
            algn2_df = pd.DataFrame(columns=[f2_name], data=['No data to align'])
        else:
            algn1_df = pd.DataFrame(columns=[f1_name], data=algn1)
            algn2_df = pd.DataFrame(columns=[f2_name], data=algn2)

        algn1_df = pd.concat([algn1_df, algn2_df], ignore_index=False, axis=1)
        msas = [
            dash_table.DataTable(columns=[{"name": i, "id": i} for i in algn1_df.columns],
                                 data=algn1_df.to_dict('records'),
                                 style_table={'overflow-x': 'hidden'},
                                 style_cell={'textAlign': 'center'},
                                 export_format="csv")]

    else:
        if len(algn1) <= 1:
            algn1 = ['No data to align']

            algn1_df = pd.DataFrame(columns=[f1_name], data=algn1)
            algn2_df = pd.DataFrame(columns=[f2_name], data=algn2)
            algn1_df = pd.concat([algn1_df, algn2_df], ignore_index=False, axis=1)
        else:
            algn2 = ['No data to align']

            algn1_df = pd.DataFrame(columns=[f1_name], data=algn1)
            algn2_df = pd.DataFrame(columns=[f2_name], data=algn2)
            algn1_df = pd.concat([algn1_df, algn2_df], ignore_index=False, axis=1)

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

    seq_len = new_process.getSeqLen()

    # calculate RNA-Template(s), dotbracket-string(s), color-vector, color-scale
    # and color-domain(s) (highest value in color-vector)

    if struct_data is not None:

        structure_info = initializeData.getTemplateSecondaryStructure(new_process, normalization_vector,
                                                                      normalization_status, no_sec_peak)

        struct1, struct2, color1, color2, color_domain_max1, color_domain_max2, color_scale = structure_info

        if struct1 is not None and struct2 is not None:
            templates = [struct1[0], struct2[0]]
            dbs = [struct1[1], struct2[1]]
        elif struct1 is not None:
            templates = [struct1[0]]
            dbs = [struct1[1]]
        else:
            templates = []
            dbs = []
    else:
        templates = None
        dbs = None
        color1 = None
        color2 = None
        color_domain_max1 = None
        color_domain_max2 = None
        color_scale = None

    data = {'topK': top_k_table, 'msas': msas, 'scatter': scatter, 'pcas': pcas, 'seqLen': seq_len,
            'templates': templates, 'dbs': dbs, 'colors': [color1, color2],
            'color_max': [color_domain_max1, color_domain_max2], 'color_scale': color_scale}

    return [data]


# --------------------------------------- File Dropdown Updater --------------------------------------------------------
@app.callback([
    dash.dependencies.Output("file1", "value"),
    dash.dependencies.Output("file2", "value"),
    dash.dependencies.Input('memory', 'modified_timestamp'),
])
# initializes data dropdowns
# ts: store timestamp
def initialSelect(ts):
    if ts is None:
        f1 = "0"
        f2 = "1"
    else:
        raise PreventUpdate

    return f1, f2


@app.callback([
    dash.dependencies.Output("file1", "options"),
    dash.dependencies.Input("file2", "value"),
])
# returns new option for dropdown based on selection
# f2: second selected file
def updateFile1Dropdown(f2):
    return updateFileList(f2, False)


@app.callback([
    dash.dependencies.Output("file2", "options"),
    dash.dependencies.Input("file1", "value"),
])
# returns new option for dropdown based on selection
# f1: first selected file
def updateFile2Dropdown(f1):
    return updateFileList(f1, False)


# disables already selected file in other dropdown
# val: (structural) file
# struct: bool (True= structural file is given)
def updateFileList(val, struct):
    if struct and struct_data is not None:
        files = struct_data
    elif struct and struct_data is None:
        return [{"label": "-", "value": "0"}]
    else:
        files = file_list

    option = [
        {'label': os.path.basename(files[i]), 'value': str(i)} if not (str(i) == val)
        else {'label': os.path.basename(files[i]), 'value': str(i), 'disabled': True}
        for i in range(0, len(files))]

    return [option]


# --------------------------------------- Structure File Dropdown Updater ----------------------------------------------
@app.callback([
    dash.dependencies.Output("file3", "value"),
    dash.dependencies.Output("file4", "value"),
    dash.dependencies.Input('memory', 'modified_timestamp'),
])
# initializes structural data dropdowns
# ts: store timestamp
def initialStructSelect(ts):
    if ts is None and struct_data is not None:
        f3 = "0"
        f4 = "1"
    else:
        raise PreventUpdate

    return f3, f4


@app.callback([
    dash.dependencies.Output("file3", "options"),
    dash.dependencies.Input("file4", "value"),
])
# returns new option for dropdown based on selection
# f4: second selected structural file
def updateFile4Dropdown(f4):
    return updateFileList(f4, True)


@app.callback([
    dash.dependencies.Output("file4", "options"),
    dash.dependencies.Input("file3", "value"),
])
# returns new option for dropdown based on selection
# f1: first selected structural file
def updateFile3Dropdown(f3):
    if struct_data is not None and len(struct_data) > 1:
        return updateFileList(f3, True)
    else:
        raise PreventUpdate


# --------------------------------------- Slider Values Updater --------------------------------------------------------


@app.callback(
    [
        dash.dependencies.Output("k", "min"),
        dash.dependencies.Output("k", "max"),
        dash.dependencies.Output("k", "marks"),
        dash.dependencies.Output("peak", "min"),
        dash.dependencies.Output("peak", "max"),
        dash.dependencies.Output("peak", "marks"),
    ],
    [
        dash.dependencies.Input('memory', 'modified_timestamp'),
        dash.dependencies.State('memory', 'data'),
    ],
)
# calculates slider ranges (marks)
# fil1/file2: input file
# ts: timestamp when data was modified
# data: storage to share data between callbacks
def updateSliderRange(ts, data):
    if ts is None:
        raise PreventUpdate
    k_p_slider_max = data['seqLen']
    k_p_slider_min = 2

    k_slider_max = k_p_slider_max - 1
    peak_min = 0

    # calculation of new slider ranges if files were changed

    k_range = markSliderRange(k_p_slider_min, k_slider_max, False)
    peak_range = markSliderRange(peak_min, k_p_slider_max, True)

    return k_p_slider_min, k_slider_max, k_range, peak_min, k_p_slider_max, peak_range


# ----------------------------------------- Forna-Container Update -----------------------------------------------------

@app.callback(
    dash.dependencies.Output('forna', 'sequences'),
    dash.dependencies.Output('forna', 'customColors'),
    dash.dependencies.Output('s-tab2', 'label'),
    dash.dependencies.Output('s-tab2', 'disabled'),
    dash.dependencies.Output('forna2', 'sequences'),
    dash.dependencies.Output('forna2', 'customColors'),
    dash.dependencies.Output('s-tab3', 'label'),
    dash.dependencies.Output('s-tab3', 'disabled'),
    [dash.dependencies.Input('memory', 'data'),
     dash.dependencies.Input('file3', 'value'),
     dash.dependencies.Input('file4', 'value'),
     ]
)
# create RNA Structure Heatmap visualizations
# data: store
# f3: first selected structural file
# f4: second selected structural file
def show_selected_sequences(data, f3, f4):
    if data is None:
        raise PreventUpdate

    template_list = data['templates']
    dotbracket_list = data['dbs']
    color_domain_max1 = data['color_max'][0]
    color_domain_max2 = data['color_max'][1]

    color_domain_max = ((color_domain_max1 + color_domain_max2) / 2)

    color_vals1 = list(set(data['colors'][0].values()))
    if 0 in color_vals1:
        color_vals1.remove(0)
    color_domain_min1 = min(color_vals1)

    color_vals2 = list(set(data['colors'][1].values()))
    if 0 in color_vals2:
        color_vals2.remove(0)
    color_domain_min2 = min(color_vals2)

    color_domain_min = (color_domain_min1 + color_domain_min2) / 2

    color_range = data['color_scale']

    # disable tab for files if no or only one structural file is given
    disable_t1 = False
    disable_t2 = False

    # color-vector
    custom_colors = None
    custom_colors2 = None

    tab1_label = "RNA-Structure Heatmap 1"
    tab2_label = "RNA-Structure Heatmap 2"

    steps = ((color_domain_max - color_domain_min) / (len(color_range) - 1))
    if steps == 0:
        steps = 1

    color_domain = [i for i in float_range(color_domain_min, steps, (len(color_range) - 1))]
    color_domain.append(color_domain_max)

    if struct_data is not None:

        color1 = data['colors'][0]

        tab1_label = os.path.basename(struct_data[int(f3)]) + " Structure Heatmap"

        # create color-vector-object for FornaContainer
        custom_colors = {
            'domain': color_domain,
            'range': color_range,
            'colorValues': {
                'template1': color1,
            }
        }

        # create sequence-object for FornaContainer
        template1 = [{
            'sequence': template_list[0],
            'structure': dotbracket_list[0],
            'options': {'name': 'template1'}
        }]

        if len(template_list) > 1:  # more than one structure file committed
            color2 = data['colors'][1]

            tab2_label = os.path.basename(struct_data[int(f4)]) + " Structure Heatmap"

            custom_colors2 = {
                'domain': color_domain,
                'range': color_range,
                'colorValues': {
                    'template2': color2,
                }
            }

            template2 = [{
                'sequence': template_list[1],
                'structure': dotbracket_list[1],
                'options': {'name': 'template2'}
            }]

        else:  # if no second structural file is available
            template2 = [{
                'sequence': "",
                'structure': ""
            }]
            disable_t2 = True

    else:  # if not structural data is available
        template1 = [{
            'sequence': "",
            'structure': ""
        }]
        template2 = [{
            'sequence': "",
            'structure': ""
        }]
        disable_t1 = True
        disable_t2 = True

    return template1, custom_colors, tab1_label, disable_t1, template2, custom_colors2, tab2_label, disable_t2


# -------------------------------------------- Modals Updater ----------------------------------------------------------

@app.callback([dash.dependencies.Output('ex_options', 'is_open'),
               dash.dependencies.Output('norm_input', 'hidden'),
               ],
              [dash.dependencies.Input('memory', 'modified_timestamp'),
               dash.dependencies.Input('opt_btn_open', 'n_clicks'),
               dash.dependencies.Input('opt_btn_close', 'n_clicks'),
               dash.dependencies.Input('opt_btn_apply', 'n_clicks'),
               dash.dependencies.Input('db', 'value'),
               dash.dependencies.Input('error', 'hidden'),
               dash.dependencies.Input('error_type', 'hidden'),
               dash.dependencies.State('ex_options', 'is_open'),
               ], prevent_initial_call=True)
# opens or closes modal
# ts: timestamp when data was modified
# data: storage to share data between callbacks
# btn_open, btn_close, btn_apply: n_clicks of open-/apply/reset-button for/in modal
# norm_val: normalization option (none, for A.thaliana, custom)
# error1, error2: error messages hidden status (True/False)
# is_open: modal status (True/False)
def updateExtendedOptionModal(ts, btn_open, btn_close, btn_apply, norm_val, error1, error2, is_open):
    if ts is None:
        raise PreventUpdate

    # determine which button was triggered
    ctx = dash.callback_context
    btn_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if norm_val == 'custom_vals':
        show_table = False
    else:
        show_table = True

    # if open-/close button was triggered, then open or close modal
    if btn_id == "opt_btn_open" or btn_id == "opt_btn_close":
        return [not is_open, show_table]
    # if apply button was triggered, close modal if no error message is shown
    elif btn_id == 'opt_btn_apply':
        if not error1 or not error2:
            return [is_open, show_table]
        else:
            return [not is_open, show_table]
    else:
        return [is_open, show_table]


@app.callback([
    dash.dependencies.Output('EE', 'value'),
    dash.dependencies.Output('SS', 'value'),
    dash.dependencies.Output('II', 'value'),
    dash.dependencies.Output('MM', 'value'),
    dash.dependencies.Output('BB', 'value'),
    dash.dependencies.Output('SI', 'value'),
    dash.dependencies.Output('IS', 'value'),
    dash.dependencies.Output('SM', 'value'),
    dash.dependencies.Output('MS', 'value'),
    dash.dependencies.Output('ES', 'value'),
    dash.dependencies.Output('SE', 'value'),
    dash.dependencies.Output('HH', 'value'),
    dash.dependencies.Output('HS', 'value'),
    dash.dependencies.Output('SH', 'value'),
    dash.dependencies.Output('SB', 'value'),
    dash.dependencies.Output('BS', 'value'),

],
    [dash.dependencies.Input('opt_btn_reset', 'n_clicks'),
     ], prevent_initial_call=True)
# resets custom rate table in modal
# reset_btn: n_clicks of reset button
def resetTable(reset_btn):
    if reset_btn:
        return [0 for i in range(0, 16)]
    else:
        return [dash.no_update for i in range(0, 16)]


@app.callback([
    dash.dependencies.Output('error', 'hidden'),
    dash.dependencies.Output('error_type', 'hidden'),

],
    [
        dash.dependencies.Input('opt_btn_apply', 'n_clicks'),
        dash.dependencies.Input('db', 'value'),
        dash.dependencies.State('EE', 'value'),
        dash.dependencies.State('SS', 'value'),
        dash.dependencies.State('II', 'value'),
        dash.dependencies.State('MM', 'value'),
        dash.dependencies.State('BB', 'value'),
        dash.dependencies.State('SI', 'value'),
        dash.dependencies.State('IS', 'value'),
        dash.dependencies.State('SM', 'value'),
        dash.dependencies.State('MS', 'value'),
        dash.dependencies.State('ES', 'value'),
        dash.dependencies.State('SE', 'value'),
        dash.dependencies.State('HH', 'value'),
        dash.dependencies.State('HS', 'value'),
        dash.dependencies.State('SH', 'value'),
        dash.dependencies.State('SB', 'value'),
        dash.dependencies.State('BS', 'value'),
    ], prevent_initial_call=True)
# show error message, if input in custom rates table is invalid
# apply_btn: n_clicks of apply button for custom rates
# norm_option: normalization options (none, for A.thaliana, custom)
# parameter (e.g. ee,ss,etc. ...): custom rates for 2-mer
def showErrorMessages(apply_btn, norm_option, ee, ss, ii, mm, bb, si, i_s, sm, ms, es, se, hh, hs, sh, sb, bs):
    hide_error_msg = True
    hide_error_type_msg = True

    ctx = dash.callback_context
    triggered_component = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_component == 'opt_btn_apply':
        if not norm_option == 'custom_vals':
            return [hide_error_msg, hide_error_type_msg]
        custom_rates = [ee, ss, ii, mm, bb, si, i_s, sm, ms, es, se, hh, hs, sh, sb, bs]
        if None in custom_rates:
            hide_error_type_msg = False
            return [hide_error_msg, hide_error_type_msg]
        check_sum_passed = check_sum(ee, ss, ii, mm, bb, si, i_s, sm, ms, es, se, hh, hs, sh, sb, bs)
        if not check_sum_passed:
            hide_error_msg = False
    return [hide_error_msg, hide_error_type_msg]


@app.callback([dash.dependencies.Output('opt_btn_open', 'disabled'),
               ],
              [dash.dependencies.Input('memory', 'modified_timestamp')])
# disables 'extended options' button if no structural data is available
# ts: store timestamp
def disableButton(ts):
    if ts is None:
        raise PreventUpdate

    disable_btn = False
    if struct_data is None:
        disable_btn = True

    return [disable_btn]


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
