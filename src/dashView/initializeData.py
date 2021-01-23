from src.kMerAlignmentData import KMerAlignmentData
from src.kMerPCAData import KMerPCAData
from src.kMerScatterPlotData import KMerScatterPlotData
from src.processing import Processing
import src.layout.plot_theme_templates as ptt
import plotly.express as px


# starts preprocess to calculate kmer-frequencies,etc
# data: file list
# selected: two files, which are processed
# k: kmer length
# peak: peak: peak-position, where sequences should be aligned
# top: number of best values
# feature: number of T or kmer-Frequency for pcas
def initData(data, selected, k, peak, top, feature):
    process = Processing(data, selected, k, peak, top, feature)
    return process


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
