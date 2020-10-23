from processing import Processing
import pandas as pd
import os


class KMerScatterPlotData(Processing):

    def __init__(self, data, selected, k, peak, top):
        super().__init__(data, selected, k, peak, top)

    def processData(self):
        top_kmer_df = self.getTopKmer()  # get top kmeres
        fileName1 = top_kmer_df['File'].drop_duplicates().tolist()[0]  # get colum names
        fileName2 = top_kmer_df['File'].drop_duplicates().tolist()[1]

        xAxis = self.getDF()[fileName1].tolist()
        yAxis = self.getDF()[fileName2].tolist()
        label = self.getDF().index.tolist()

        result_df = pd.DataFrame(xAxis, index=label, columns=[fileName1])
        result_df[fileName2] = yAxis
        result_df['highlight'] = False  # highlights top kmere

        kmerList = top_kmer_df.index.tolist()
        for kmer in kmerList:
            result_df.loc[kmer, 'highlight'] = True

        return [result_df, label, [fileName1, fileName2]]
