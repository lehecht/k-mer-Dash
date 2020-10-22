from processing import Processing
from kValueException import *
from kMerScatterPlotData import KMerScatterPlotData
from kMerPCAData import KMerPCAData
import math

import plotly.express as px


def printData(data, k, peak, top):
    try:
        process = Processing(data, None, k, peak, top)
        # printKMerFrequency(process)
        # printScatterPlot(process)
        printPCA(process)
    except KValueException:
        print("Invalid k: k must be smaller than sequence length")


def printScatterPlot(process):
    result = KMerScatterPlotData.processData(process)
    df = result[0]
    label = result[1]
    fileNames = result[2]
    fig = px.scatter(df, x=fileNames[0], y=fileNames[1], hover_name=label, color='highlight',
                     labels={'highlight': 'Top k-Mer'})
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
    if char_space >= 10:  # calculate tab count to keep maintain readability
        tabs = math.ceil(char_space / 5)

    file_list = result['File'].values.tolist()
    kmer_list = result.index.tolist()
    print()
    print('Options:')
    print('k: {k}, peak: {p}, top: {t}, files: {f}'.
          format(k=k, p=peak, t=top, f=selected))
    print()
    print('k-Mer\t\tFrequency' + '\t' * tabs + 'File')
    for i in range(0, top * 2):
        print("{}\t\t{:<{space}}\t\t{}".format(kmer_list[i], freq_list[i], file_list[i], space=char_space))


def printMultAlignment():
    pass


def printPCA(process):
    df = process.getDF()
    pca_df = KMerPCAData.processData(process)
    fig = px.scatter(pca_df, x='PC1', y='PC2', hover_name=df.index.tolist())
    fig.show()
