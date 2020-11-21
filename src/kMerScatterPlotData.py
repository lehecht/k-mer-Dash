from src.processing import Processing
import pandas as pd


class KMerScatterPlotData(Processing):

    def __init__(self, data, selected, k, peak, top, highlight):
        super().__init__(data, selected, k, peak, top, highlight)

    def processData(self):
        data = self.getDF()  # get top kmeres

        fileName1 = data.columns.tolist()[0]  # get column names
        fileName2 = data.columns.tolist()[1]

        highlights = self.getSettings().getHighlight()

        xAxis = data[fileName1].tolist()
        yAxis = data[fileName2].tolist()
        label = data.index.tolist()

        result_df = pd.DataFrame(xAxis, index=label, columns=[fileName1])
        result_df[fileName2] = yAxis
        result_df['highlight'] = False  # highlights top kmere

        if len(result_df) < highlights:  # checks if highlight value is valid
            print("Amount of highlights is greater than the amount of entries!")
            highlights = max(int(len(result_df) * 0.01), 1)
            print("Amount of highlights was set on {}".format(highlights))

        allFreqs = data[fileName1].values.tolist()
        allFreqs.extend(data[fileName2].values.tolist())  # get all Frequencies
        maxFreqs = list(set(allFreqs))  # drop dublications
        maxFreqs.sort(reverse=True)
        maxFreqs = maxFreqs[:highlights]

        highlightKmer = []

        for val in maxFreqs:
            highlightKmer.extend(data[data[fileName1] == val].index.tolist())  # get kmeres with given Frequency
            highlightKmer.extend(data[data[fileName2] == val].index.tolist())

        for kmer in highlightKmer:
            result_df.loc[kmer, ['highlight']] = True  # set highlight-entries on true for max-kmeres

        return [result_df, label, [fileName1, fileName2]]
