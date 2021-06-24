from src.processing import Processing
import pandas as pd


# inherits from process
# implements processData for scatterplot of frequencies
class KMerScatterPlotData(Processing):

    def __init__(self, data, selected, k, peak, top, feature, cmd, sec_struct_data, no_sec_peak):
        super().__init__(data, selected, k, peak, top, feature, cmd, sec_struct_data, no_sec_peak)

    # processes data to display k-mer according their frequency later
    def processData(self):
        top_kmer = self.getTopKmer()
        data = self.getDF()  # get top k-mer

        file_name1 = data.columns.tolist()[0]  # get column names
        file_name2 = data.columns.tolist()[1]

        x_axis = data[file_name1].tolist()
        y_axis = data[file_name2].tolist()
        label = data.index.tolist()

        result_df = pd.DataFrame(x_axis, index=label, columns=[file_name1])
        result_df[file_name2] = y_axis

        k = self.getSettings().getK()

        top_kmer_dict = dict.fromkeys(top_kmer.index.tolist(), True)  # set highlight-entries on true for max-k-mere
        all_kmer_dict = dict.fromkeys(result_df.index.tolist(), False)
        all_kmer_dict.update(top_kmer_dict)

        result_df['highlight'] = ["TOP {}-mer".format(k) if all_kmer_dict[kmer] else "{}-mer".format(k) for
                                  kmer in result_df.index.tolist()]  # save highlight-values for legend

        max_score = result_df[file_name1].max() * result_df[file_name2].max()

        # calculates scores for point size in diagram
        result_df = pd.eval("size_score = (result_df[file_name1] * result_df[file_name2])/max_score", target=result_df)

        # overwrite all point sizes < 0.01 with 0.01
        small_freq = result_df.query("size_score < 0.01").index.tolist()
        result_df.loc[small_freq, ["size_score"]] = 0.01

        size_score = result_df["size_score"].tolist()

        return [result_df, label, [file_name1, file_name2], size_score]
