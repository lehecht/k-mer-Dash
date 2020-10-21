from processing import Processing
from kValueException import *
from kMerTableData import KMerTableData
from kMerScatterPlotData import KMerScatterPlotData
from kMerPCAData import KMerPCAData
import math


# import plotly.express as px


def printData(data, k, peak, top):
    try:
        process = Processing(data, None, k, peak, top)
        printKMerFrequency(process)
    except KValueException:
        print("Invalid k: k must be smaller than sequence length")


def printScatterPlot(process):
    pass


# S = KMerScatterPlotData.processData(process)
# x = S.processData()[0]
# y = S.processData()[1]
# label = S.processData()[2]
# print(x)
# print(y)
# print(label)
# fig = px.scatter(x=x, y=y, hover_name=label)
# fig.show()


def printKMerFrequency(process):
    top = process.getSettings().getTop()
    k = process.getSettings().getK()
    peak = process.getSettings().getPeak()
    selected = process.getSettings().getSelected()

    result = KMerTableData.processData(process)
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


def printPCA():
    pass
