from src.processing import Processing
from src.inputValueException import *
from src.kMerScatterPlotData import KMerScatterPlotData
from src.kMerPCAData import KMerPCAData
from src.kMerAlignmentData import KMerAlignmentData
import math

import plotly.express as px


def printData(data, k, peak, top):
    try:
        process = Processing(data, None, k, peak, top)
        printMultAlignment(process)
        printKMerFrequency(process)
        printScatterPlot(process)
        printPCA(process)
    except InputValueException as ive:
        print(ive.args[0])
    except FileNotFoundError as fnf:
        print(fnf.args[0])


def printScatterPlot(process):
    result = KMerScatterPlotData.processData(process)
    df = result[0]
    label = result[1]
    fileNames = result[2]
    fig = px.scatter(df, x=fileNames[0], y=fileNames[1], hover_name=label, color='highlight',
                     labels={'highlight': 'Top k-Mer'}, title='Scatterplot')
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
    print()
    print('Options:')
    print('k: {k}, peak: {p}, top: {t}, files: {f}'.
          format(k=k, p=peak, t=top, f=selected))
    print()
    print('k-Mer\t\tFrequency' + '\t' * tabs + 'File')
    for i in range(0, min(top * 2, len(kmer_list))):
        print("{}\t\t{:<{space}}\t\t{}".format(kmer_list[i], freq_list[i], file_list[i], space=char_space))


def printMultAlignment(process):
    alignment_list = KMerAlignmentData.processData(process)
    print('Alignment of Top-kmere created with ClustalW')
    print('(for more information, see: http://www.clustal.org/clustal2/)')
    for alg in alignment_list:
        print(alg.seq)


def printPCA(process):
    K = process.getSettings().getK()
    pca_dfs = KMerPCAData.processData(process)
    pca_df1 = pca_dfs[0]
    pca_df2 = pca_dfs[1]
    filename1 = pca_dfs[2]
    filename2 = pca_dfs[3]
    wDf1 = pca_dfs[4]
    wDf1.name = '#T'
    wDf2 = pca_dfs[5]
    wDf2.name = '#T'

    fig1 = px.scatter(pca_df1, x='PC1', y='PC2', hover_name=pca_df1.index.tolist(), title='PCA of {}'.format(filename1),
                      color=wDf1, range_color=[0, K], color_continuous_scale=px.colors.sequential.deep)
    fig2 = px.scatter(pca_df2, x='PC1', y='PC2', hover_name=pca_df2.index.tolist(), title='PCA of {}'.format(filename2),
                      color=wDf2, range_color=[0, K], color_continuous_scale=px.colors.sequential.deep)
    fig1.update_layout(coloraxis_colorbar=dict(
        title="#T",
    ))
    fig2.update_layout(coloraxis_colorbar=dict(
        title="#T"
    ))
    fig1.show()
    fig2.show()
