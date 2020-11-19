from src.processing import Processing
import pandas as pd


class KMerScatterPlotData(Processing):

    def __init__(self, data, selected, k, peak, top, highlight):
        super().__init__(data, selected, k, peak, top, highlight)

    def processData(self):
        top_kmer_df = self.getTopKmer()  # get top kmeres
        fileName1 = top_kmer_df['File'].drop_duplicates().tolist()[0]  # get column names
        fileName2 = top_kmer_df['File'].drop_duplicates().tolist()[1]

        highlights = self.getSettings().getHighlight()

        xAxis = self.getDF()[fileName1].tolist()
        yAxis = self.getDF()[fileName2].tolist()
        label = self.getDF().index.tolist()

        result_df = pd.DataFrame(xAxis, index=label, columns=[fileName1])
        result_df[fileName2] = yAxis
        result_df['highlight'] = False  # highlights top kmere

        top_kmer_df = top_kmer_df.sort_values(by=['Frequency'],
                                              ascending=False)  # sort df by frequency getting max entries

        if len(result_df) < highlights:  # checks if highlight value is valid
            print("Amount of highlights is greater than the amount of entries!")
            highlights = int(len(result_df) * 0.01)
            print("Amount of highlights was set on {}".format(highlights))

        highlightKmer = top_kmer_df[:highlights].index.tolist()  # collect max-kmeres for highlighting

        for kmer in highlightKmer:
            result_df.loc[kmer, ['highlight']] = True  # set highlight-entries on true for max-kmeres

        return [result_df, label, [fileName1, fileName2]]
