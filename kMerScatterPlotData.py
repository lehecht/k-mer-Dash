from processing import Processing
from kMerTableData import KMerTableData
import pandas as pd
import os


class KMerScatterPlotData(Processing):

    def __init__(self, data, selected, k, peak, top):
        super().__init__(data, selected, k, peak, top)

    def processData(self):
        fileNames = self.getSettings().getSelected()

        xAxis = self.getDF()[0]
        yAxis = self.getDF()[1]
        label = self.getDF()[2]

        fileName1 = os.path.basename(fileNames[0])
        fileName2 = os.path.basename(fileNames[1])

        result_df = pd.DataFrame(xAxis, index=label, columns=[fileName1])
        result_df[fileName2] = yAxis
        result_df['highlight'] = False

        top_kmer_df = KMerTableData.processData(self)  # get top kmeres
        kmerList = top_kmer_df.index.tolist()
        for kmer in kmerList:
            result_df.loc[kmer, 'highlight'] = True

        return [result_df, label, [fileName1, fileName2]]
