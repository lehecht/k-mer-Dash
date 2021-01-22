from src.processing import Processing
import pandas as pd
import time


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

        k = self.getSettings().getK()

        result_df['highlight'] = "{}-mer".format(k)  # highlights top kmere

        for kmer in topKmer.index.tolist():
            result_df.loc[kmer, ['highlight']] = "TOP {}-mer".format(k)  # set highlight-entries on true for max-kmeres

        max_score = result_df[fileName1].max() * result_df[fileName2].max()

        result_df = pd.eval("size_score = (result_df[fileName1] * result_df[fileName2])/max_score", target=result_df)

        small_freq = result_df.query("size_score < 0.01").index.tolist()
        result_df.loc[small_freq,["size_score"]] = 0.01

        # result_df["size_score"] = result_df["size_score"].replace("<0.01",0.01)
        # print(result_df)
        # result_df["size_score"] = result_df["size_score"].fillna(0.01)
        # print(result_df)

        # t1 = time.time()
        # print(t1 - t0)

        # for i in range(0, len(result_df)):
        #     score = result_df.iloc[i][fileName1] * result_df.iloc[i][fileName2]
        #     score = score / max_score
        #     if score < 0.01:
        #         score = 0.01
        #     size_score.append(score)

        # result_df["size_score"] = size_score
        size_score = result_df["size_score"].tolist()

        return [result_df, label, [fileName1, fileName2], size_score]
