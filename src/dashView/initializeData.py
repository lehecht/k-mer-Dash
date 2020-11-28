from src.inputValueException import InputValueException
from src.kMerAlignmentData import KMerAlignmentData
from src.kMerPCAData import KMerPCAData
from src.kMerScatterPlotData import KMerScatterPlotData
from src.processing import Processing
import plotly.express as px


def initData(data, selected, k, peak, top, highlight):
    try:
        return Processing(data, selected, k, peak, top, highlight)
    except InputValueException as ive:
        print(ive.args[0])
    except FileNotFoundError as fnf:
        print(fnf.args[0])


def getAlignmentData(process):
    try:
        return KMerAlignmentData.processData(process)
    except FileNotFoundError as fnf:
        print(fnf.args[0])


def getScatterPlot(process):
    result = KMerScatterPlotData.processData(process)
    df = result[0]
    label = result[1]
    fileNames = result[2]
    fig = px.scatter(df, x=fileNames[0], y=fileNames[1], hover_name=label, color='highlight',
                     labels={'highlight': 'Top k-Mer'}, title='Scatterplot')
    return fig


def getPCA(process):
    pca_dfs = KMerPCAData.processData(process)
    pca_df1 = pca_dfs[0]
    pca_df2 = pca_dfs[1]
    filename1 = pca_dfs[2]
    filename2 = pca_dfs[3]
    prop1 = pca_dfs[4].Frequency  # highlighting property Frequency
    prop2 = pca_dfs[5].Frequency
    propName = pca_dfs[4].Frequency.name

    fig1 = px.scatter(pca_df1, x='PC1', y='PC2', hover_name=pca_df1.index.tolist(), title='PCA of {}'.format(filename1),
                      color=prop1, color_continuous_scale='plasma')
    fig2 = px.scatter(pca_df2, x='PC1', y='PC2', hover_name=pca_df2.index.tolist(), title='PCA of {}'.format(filename2),
                      color=prop2, color_continuous_scale='plasma')
    fig1.update_layout(coloraxis_colorbar=dict(
        title=propName,
    ))
    fig2.update_layout(coloraxis_colorbar=dict(
        title=propName
    ))
    return fig1, fig2
