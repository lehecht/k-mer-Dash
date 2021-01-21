from src.processing import Processing
import pandas as pd
import math


class KMerScatterPlotData(Processing):

    def __init__(self, data, selected, k, peak, top, feature):
        super().__init__(data, selected, k, peak, top, feature)

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
        result_df['highlight'] = "{}-mer".format(self.getSettings().getK())  # highlights top kmere

        for kmer in topKmer.index.tolist():
            result_df.loc[kmer, ['highlight']] = "TOP {}-mer".format(
                self.getSettings().getK())  # set highlight-entries on true for max-kmeres

        size_score = []
        max_score = result_df[fileName1].max() * result_df[fileName2].max()
        for i in range(0, len(result_df)):
            score = result_df.iloc[i][fileName1] * result_df.iloc[i][fileName2]
            score = score / max_score
            if score < 0.01:
                score = 0.01
            size_score.append(score)

        result_df["size_score"] = size_score

        return [result_df, label, [fileName1, fileName2], size_score]
