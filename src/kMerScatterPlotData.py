from src.processing import Processing
import pandas as pd


# inherits from process
# implements processData for scatterplot of frequencies
class KMerScatterPlotData(Processing):

    def __init__(self, data, selected, k, peak, top, feature):
        super().__init__(data, selected, k, peak, top, feature)

    # processes data to display kmers according their frequency later
    def processData(self):
        topKmer = self.getTopKmer()
        data = self.getDF()  # get top kmeres

        fileName1 = data.columns.tolist()[0]  # get column names
        fileName2 = data.columns.tolist()[1]

        xAxis = data[fileName1].tolist()
        yAxis = data[fileName2].tolist()
        label = data.index.tolist()

        result_df = pd.DataFrame(xAxis, index=label, columns=[fileName1])
        result_df[fileName2] = yAxis

        k = self.getSettings().getK()

        # important for legend in scatterplot
        result_df['highlight'] = "{}-mer".format(k)  # highlights top kmere

        #################### langsam #####################
        for kmer in topKmer.index.tolist():
            result_df.loc[kmer, ['highlight']] = "TOP {}-mer".format(k)  # set highlight-entries on true for max-kmeres

        max_score = result_df[fileName1].max() * result_df[fileName2].max()

        # calculates scores for point size in diagram
        result_df = pd.eval("size_score = (result_df[fileName1] * result_df[fileName2])/max_score", target=result_df)

        # overwrite all point sizes < 0.01 with 0.01
        small_freq = result_df.query("size_score < 0.01").index.tolist()
        result_df.loc[small_freq, ["size_score"]] = 0.01

        size_score = result_df["size_score"].tolist()

        return [result_df, label, [fileName1, fileName2], size_score]
