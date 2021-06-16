from src.kMerAlignmentData import KMerAlignmentData
from src.kMerPCAData import KMerPCAData
from src.kMerScatterPlotData import KMerScatterPlotData
from src.secStructure import SecStructure
from src.processing import Processing
import src.layout.plot_theme_templates as ptt
import plotly.express as px

from src.secStructure import SecStructure


# starts preprocess to calculate kmer-frequencies,etc
# data: file list
# selected: two files, which are processed
# k: kmer length
# peak: peak: peak-position, where sequences should be aligned
# top: number of best values
# feature: number of T or kmer-Frequency for pcas
def initData(data, selected, k, peak, top, feature, secStruct_data, no_sec_peak):
    process = Processing(data, selected, k, peak, top, feature, False, secStruct_data, no_sec_peak)
    return process


# def getTemplateSecondaryStructure(process, norm_vector, custom_norm_vec):
#     color_scale = px.colors.sequential.Viridis
#
#     structProfile1 = process.getStructProfil1()
#     structProfile2 = process.getStructProfil2()
#
#     single_template = True
#
#     no_seq_peak = process.getNoSecPeak()
#
#     # if not norm_vector is None:
#     if custom_norm_vec:
#         process.setNormVector(norm_vector)
#     else:
#         at_norm_vector = process.getATnormVector()
#         process.setNormVector(at_norm_vector)
#
#     if not structProfile1 is None:
#
#         alphabet1 = structProfile1.getAlphabet()
#
#         s1 = SecStructure.createTemplates(process, alphabet1)
#
#         structProfile1_profil = structProfile1.getProfile()
#
#         if isinstance(s1[0], str):
#             structProfile1.setTemplate(s1[0])
#             structProfile1.setDotbracket(s1[1])
#             color1, color_domain_max1, not_matched = SecStructure.createHeatMapColoring(process, s1[0],
#                                                                                         structProfile1_profil,
#                                                                                         no_seq_peak)
#         else:
#             color1 = []
#             color_domain_max1 = []
#             not_matched = []
#             single_template = False
#             structProfile1.setDictTemplate(s1[0])
#             structProfile1.setDictDotbracket(s1[1])
#
#             for template in s1[0]:
#                 color, color_domain_max, not_matched = SecStructure.createHeatMapColoring(process, template,
#                                                                                           structProfile1_profil,
#                                                                                           no_seq_peak,
#                                                                                           not_matched)
#                 color1.append(color)
#                 color_domain_max1.append(color_domain_max)
#
#         if not structProfile2 is None:
#             alphabet2 = structProfile2.getAlphabet()
#             s2 = SecStructure.createTemplates(process, alphabet2)
#             structProfile2_profil = structProfile2.getProfile()
#
#             if single_template:
#                 structProfile2.setTemplate(s2[0])
#                 structProfile2.setDotbracket(s2[1])
#                 color2, color_domain_max2, not_matched = SecStructure.createHeatMapColoring(process, s2[0],
#                                                                                             structProfile2_profil,
#                                                                                             no_seq_peak)
#             else:
#                 color2 = []
#                 color_domain_max2 = []
#                 not_matched = []
#                 structProfile2.setDictTemplate(s2[0])
#                 structProfile2.setDictDotbracket(s2[1])
#
#                 for template in s2[0]:
#                     color, color_domain_max, not_matched = SecStructure.createHeatMapColoring(process, template,
#                                                                                               structProfile2_profil,
#                                                                                               no_seq_peak,
#                                                                                               not_matched)
#                     color2.append(color)
#                     color_domain_max2.append(color_domain_max)
#
#             return s1, s2, color1, color2, color_domain_max1, color_domain_max2, color_scale
#         else:
#             if isinstance(s1[0], str):
#                 structProfile1.setTemplate(s1[0])
#                 structProfile1.setDotbracket(s1[1])
#                 color1, color_domain_max1, not_matched = SecStructure.createHeatMapColoring(process, s1[0],
#                                                                                             structProfile1_profil,
#                                                                                             no_seq_peak)
#             else:
#                 color1 = []
#                 color_domain_max1 = []
#                 not_matched = []
#                 structProfile1.setDictTemplate(s1[0])
#                 structProfile1.setDictDotbracket(s1[1])
#
#                 for template in s1[0]:
#                     color, color_domain_max, not_matched = SecStructure.createHeatMapColoring(process, template,
#                                                                                               structProfile1_profil,
#                                                                                               no_seq_peak,
#                                                                                               not_matched)
#                     color1.append(color)
#                     color_domain_max1.append(color_domain_max)
#
#             return s1, None, color1, None, color_domain_max1, None,color_scale
#     else:
#         return None, None, None, None, None, None, None

def getTemplateSecondaryStructure(process, norm_vector, custom_norm_vec, no_seq_peak):
    color_scale = px.colors.sequential.Viridis

    if custom_norm_vec:
        process.setNormVector(norm_vector)
    else:
        at_norm_vector = process.getATnormVector()
        process.setNormVector(at_norm_vector)

    templates_dotbrs = SecStructure.processData(process)

    file1_t_d = templates_dotbrs[0]
    file2_t_d = None
    file1_template = file1_t_d[0]

    file2_template = None
    if len(templates_dotbrs) > 1:
        file2_t_d = templates_dotbrs[1]
        file2_template = file2_t_d[0]

    heat_map_coloring = SecStructure.createHeatMapColoring(process, file1_template, file2_template,
                                                           no_seq_peak)

    color1, color_domain_max1, not_matched1 = heat_map_coloring[0]

    color2, color_domain_max2, not_matched2 = [None, None, None]

    if len(heat_map_coloring) > 1:
        color2, color_domain_max2, not_matched2 = heat_map_coloring[1]

    return file1_t_d, file2_t_d, color1, color2, color_domain_max1, color_domain_max2, color_scale


# gets alignment data
# process: object, which contains information for further calculation-processes
def getAlignmentData(process):
    alignment_lists, f1_name, f2_name = KMerAlignmentData.processData(process)
    algn1 = alignment_lists[0]
    algn2 = alignment_lists[1]
    # if peak position is not given, record-type alignment must be casted to strings
    if process.getSettings().getPeak() is None:
        algn1 = [str(e.seq) for e in algn1]
        algn2 = [str(e.seq) for e in algn2]

    return algn1, algn2, f1_name, f2_name


# gets data for scatterplot and creates scatterplot-figure
# process: object, which contains information for further calculation-processes
def getScatterPlot(process):
    result = KMerScatterPlotData.processData(process)
    df = result[0]
    # list of kmers
    label = result[1]
    file_names = result[2]

    fig = px.scatter(df, x=file_names[0], y=file_names[1], hover_name=label,
                     color='highlight',
                     color_discrete_map={"TOP {}-mer".format(process.getSettings().getK()): "red",
                                         "{}-mer".format(process.getSettings().getK()): "black"},
                     title='Scatterplot of k-Mer occurrences (#)',
                     opacity=0.55,
                     size="size_score",
                     hover_data={'highlight': False, file_names[0]: True, file_names[1]: True, 'size_score': False},
                     )
    fig.update_layout(dict(template=ptt.custom_plot_template, legend=dict(title=None)),
                      title=dict(font_size=20))
    fig.update_xaxes(title="#k-Mer of " + file_names[0], title_font=dict(size=15))
    fig.update_yaxes(title="#k-Mer of " + file_names[1], title_font=dict(size=15))
    return fig


# gets pca data and created two pca-figures
# process: object, which contains information for further calculation-processes
def getPCA(process):
    pca_dfs = KMerPCAData.processData(process)
    pca_df1 = pca_dfs[0]
    pca_df2 = pca_dfs[1]
    file_name1 = pca_dfs[2]
    file_name2 = pca_dfs[3]
    top_list1 = pca_dfs[4]
    top_list2 = pca_dfs[5]

    # if feature was changed, name for colorscale and highlighting must also be changed
    if process.getSettings().getFeature() is "2":
        feature_name = 'T'
        colorscale_feat_name = '#T'
        feature_df1 = top_list1['T']
        feature_df2 = top_list2['T']
    else:
        feature_name = 'Frequency'
        colorscale_feat_name = feature_name
        feature_df1 = top_list1.Frequency
        feature_df2 = top_list2.Frequency

    pca_df1 = pca_df1.join(feature_df1)
    pca_df2 = pca_df2.join(feature_df2)

    figures = []
    for p in [pca_df1, pca_df2]:
        fig = px.scatter(p, x='PC1', y='PC2', hover_name=p.index.tolist(),
                         color=feature_name,
                         opacity=0.6,
                         color_continuous_scale='plasma',
                         hover_data={"PC1": False, "PC2": False})
        fig.update_layout(template=ptt.custom_plot_template, xaxis=dict(zeroline=False, showline=True),
                          yaxis=dict(zeroline=False, showline=True), coloraxis_colorbar=dict(
                title=colorscale_feat_name))
        fig.update_xaxes(title_font=dict(size=15))
        fig.update_yaxes(title_font=dict(size=15))
        fig.update_traces(marker=dict(size=12, line=dict(width=2,
                                                         color='DarkSlateGrey')))
        figures.append(fig)

    return figures, file_name1, file_name2
