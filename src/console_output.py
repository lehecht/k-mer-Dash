from src.processing import Processing
from src.kMerScatterPlotData import KMerScatterPlotData
from src.kMerPCAData import KMerPCAData
from src.kMerAlignmentData import KMerAlignmentData
import math
import src.layout.plot_theme_templates as ptt

import plotly.express as px


# starts preprocess to calculate kmer-frequencies,etc and call print-methods
# data: file list
# k: kmer length
# peak: peak: peak-position, where sequences should be aligned
# top: number of best values
def printData(data, k, peak, top):
    process = Processing(data, data, k, peak, top, None)
    printPairwAlignment(process)
    printKMerFrequency(process)
    printScatterPlot(process)
    printPCA(process)


# gets data and displays scatterplot
# process: object, which contains information for further calculation-processes
def printScatterPlot(process):
    result = KMerScatterPlotData.processData(process)
    df = result[0]
    # list of kmers
    label = result[1]
    file_names = result[2]

    fig = px.scatter(df, x=file_names[0], y=file_names[1], hover_name=label,
                     color='highlight',
                     color_discrete_map={"TOP {}-mer".format(process.getSettings().getK()): "red",
                                         "{}-mer".format(process.getSettings().getK()): "black"},
                     title='Scatterplot of k-Mer occurences (#)',
                     opacity=0.55,
                     size="size_score",
                     hover_data={'highlight': False, file_names[0]: True, file_names[1]: True, 'size_score': False},
                     )
    fig.update_layout(dict(template=ptt.custom_plot_template, legend=dict(title=None)),
                      title=dict(font_size=25))
    fig.update_xaxes(title="#k-Mer of " + file_names[0], title_font=dict(size=18))
    fig.update_yaxes(title="#k-Mer of " + file_names[1], title_font=dict(size=18))
    fig.show()


# gets data and prints kmer-frequency table to stdout
# process: object, which contains information for further calculation-processes
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
        entry_count = top
    else:
        entry_count = min(top * 2, len(kmer_list))
    print()
    print('Options:')
    print('k: {k}, peak: {p}, top: {t}, files: {f}'.
          format(k=k, p=peak, t=top, f=selected))
    print()
    print('k-Mer\t\tFrequency' + '\t' * tabs + 'File')
    for i in range(0, entry_count):
        print("{}\t\t{:<{space}}\t\t{}".format(kmer_list[i], freq_list[i], file_list[i], space=char_space))


# gets alignment data and prints alignment to stdout
# process: object, which contains information for further calculation-processes
def printPairwAlignment(process):
    try:
        alignment_lists, f1_name, f2_name = KMerAlignmentData.processData(process)

        if process.getSettings().getPeak() is None:
            print('Alignment of Top-kmere created with ClustalW')
            print('(for more information, see: http://www.clustal.org/clustal2/)')
            print("")
            name = f1_name
            for file in alignment_lists:
                print("File: " + name)
                for alg in file:
                    print(alg.seq)
                name = f2_name
                print()
        else:
            print('Alignment of Top-kmere created with Peak-Position: {}'.format(process.getSettings().getPeak()))
            name = f1_name
            for file in alignment_lists:
                print("File: " + name)
                for alg in file:
                    print(alg)
                name = f2_name
                print()
    except ValueError:
        print("ERROR: Alignment cannot be calculated. Top-Value is too big.")


# gets pca data separate for both files and displays it as scatterplot
# process: object, which contains information for further calculation-processes
def printPCA(process):
    pca_dfs = KMerPCAData.processData(process)
    pca_df1 = pca_dfs[0]
    pca_df2 = pca_dfs[1]
    top_list1 = pca_dfs[4]
    top_list2 = pca_dfs[5]

    pca_df1 = pca_df1.join(top_list1.Frequency)
    pca_df2 = pca_df2.join(top_list2.Frequency)

    for p in [pca_df1, pca_df2]:
        fig = px.scatter(p, x='PC1', y='PC2', hover_name=p.index.tolist(),
                         color='Frequency',
                         color_continuous_scale='plasma',
                         hover_data={"PC1": False, "PC2": False})
        fig.update_layout(template=ptt.custom_plot_template, xaxis=dict(zeroline=False, showline=True),
                          yaxis=dict(zeroline=False, showline=True), title=dict(font_size=25))
        fig.update_xaxes(title_font=dict(size=18))
        fig.update_yaxes(title_font=dict(size=18))
        fig.update_traces(marker=dict(size=18, line=dict(width=2,
                                                         color='DarkSlateGrey')))
        fig.show()
