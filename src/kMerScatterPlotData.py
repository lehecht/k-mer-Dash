from src.processing import Processing
import pandas as pd
import time


# inherits from process
# implements processData for scatterplot of frequencies
class KMerScatterPlotData(Processing):

    def __init__(self, data, selected, k, peak, top, feature,cmd):
        super().__init__(data, selected, k, peak, top, feature,cmd)

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

        top_kmer_dict = dict.fromkeys(topKmer.index.tolist(), True)  # set highlight-entries on true for max-kmeres
        all_kmer_dict = dict.fromkeys(result_df.index.tolist(), False)
        all_kmer_dict.update(top_kmer_dict)

        result_df['highlight'] = ["TOP {}-mer".format(k) if all_kmer_dict[kmer] else "{}-mer".format(k) for
                                  kmer in result_df.index.tolist()]  # save highlight-values for legend

        max_score = result_df[fileName1].max() * result_df[fileName2].max()

        # calculates scores for point size in diagram
        result_df = pd.eval("size_score = (result_df[fileName1] * result_df[fileName2])/max_score", target=result_df)

        # overwrite all point sizes < 0.01 with 0.01
        small_freq = result_df.query("size_score < 0.01").index.tolist()
        result_df.loc[small_freq, ["size_score"]] = 0.01

        size_score = result_df["size_score"].tolist()

        return [result_df, label, [fileName1, fileName2], size_score]
