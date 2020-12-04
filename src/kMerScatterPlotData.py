from src.processing import Processing
import pandas as pd


class KMerScatterPlotData(Processing):

    def __init__(self, data, selected, k, peak, top):
        super().__init__(data, selected, k, peak, top)

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
        result_df['highlight'] = False  # highlights top kmere

        for kmer in topKmer.index.tolist():
            result_df.loc[kmer, ['highlight']] = True  # set highlight-entries on true for max-kmeres

        return [result_df, label, [fileName1, fileName2]]
