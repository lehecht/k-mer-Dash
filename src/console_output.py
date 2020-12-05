from src.processing import Processing
from src.kMerScatterPlotData import KMerScatterPlotData
from src.kMerPCAData import KMerPCAData
from src.kMerAlignmentData import KMerAlignmentData
import math

import plotly.express as px


def printData(data, k, peak, top):
    process = Processing(data, data, k, peak, top)
    # printPairwAlignment(process)
    # printKMerFrequency(process)
    printScatterPlot(process)
    # printPCA(process)


def printScatterPlot(process):
    result = KMerScatterPlotData.processData(process)
    df = result[0]
    label = result[1]
    fileNames = result[2]
    # size_score = result[3]

    fig = px.scatter(df, x=fileNames[0], y=fileNames[1], hover_name=label,
                     color='highlight',
                     color_discrete_map={"TOP {}-mer".format(process.getSettings().getK()): "red",
                                         "{}-mer".format(process.getSettings().getK()): "black"},
                     title='Scatterplot of k-Mer occurences (#)',
                     opacity=0.55,
                     size="size_score",
                     hover_data={'highlight': False, fileNames[0]: True, fileNames[1]: True, 'size_score': False},
                     )
    fig.update_layout(
        dict(font_color='black', legend_traceorder="reversed", legend=dict(title=None, bordercolor="Black",
                                                                           borderwidth=1, font_size=18),
             plot_bgcolor="white"),
        title=dict(font_size=25, xanchor='center', yanchor='top', y=0.95, x=0.5))
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#e6e6e6', linecolor="black",
                     title="#k-Mer of " + fileNames[0],title_font=dict(size=18))
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#e6e6e6', linecolor="black",
                     title="#k-Mer of " + fileNames[1],title_font=dict(size=18))
    fig.show()


def printKMerFrequency(process):
    top = process.getSettings().getTop()
    k = process.getSettings().getK()
    peak = process.getSettings().getPeak()
    selected = process.getSettings().getSelected()

    result = process.getTopKmer()
    freq_list = result['Frequency'].values.tolist()
    char_space = len(str(max(freq_list)))  # ascertains column space to maintain table readability
    tabs = 1
    if char_space >= 10:  # calculate tab count to maintain readability
        tabs = math.ceil(char_space / 5)

    file_list = result['File'].values.tolist()
    kmer_list = result.index.tolist()

    if top is None:
        top = len(process.getTopKmer())
        entryCount = top
    else:
        entryCount = min(top * 2, len(kmer_list))
    print()
    print('Options:')
    print('k: {k}, peak: {p}, top: {t}, files: {f}'.
          format(k=k, p=peak, t=top, f=selected))
    print()
    print('k-Mer\t\tFrequency' + '\t' * tabs + 'File')
    for i in range(0, entryCount):
        print("{}\t\t{:<{space}}\t\t{}".format(kmer_list[i], freq_list[i], file_list[i], space=char_space))


def printPairwAlignment(process):
    alignment_list = KMerAlignmentData.processData(process)
    if process.getSettings().getPeak() is None:
        print('Alignment of Top-kmere created with ClustalW')
        print('(for more information, see: http://www.clustal.org/clustal2/)')
        print("")
        for alg in alignment_list:
            print(alg.seq)
    else:
        print('Alignment of Top-kmere created with Peak-Position: {}'.format(process.getSettings().getPeak()))
        for alg in alignment_list:
            print(alg)


def printPCA(process):
    pca_dfs = KMerPCAData.processData(process)
    pca_df1 = pca_dfs[0]
    pca_df2 = pca_dfs[1]
    filename1 = pca_dfs[2]
    filename2 = pca_dfs[3]
    propName = 'Frequency'

    if pca_df1 is not None:
        prop1 = pca_dfs[4].Frequency  # highlighting property Frequency
        fig1 = px.scatter(pca_df1, x='PC1', y='PC2', hover_name=pca_df1.index.tolist(),
                          title='PCA of {}'.format(filename1),
                          color=prop1, color_continuous_scale='plasma')
        fig1.update_layout(coloraxis_colorbar=dict(
            title=propName,
        ))
        fig1.show()

    if pca_df2 is not None:
        prop2 = pca_dfs[5].Frequency
        fig2 = px.scatter(pca_df2, x='PC1', y='PC2', hover_name=pca_df2.index.tolist(),
                          title='PCA of {}'.format(filename2),
                          color=prop2, color_continuous_scale='plasma')

        fig2.update_layout(coloraxis_colorbar=dict(
            title=propName
        ))
        fig2.show()
