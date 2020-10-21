from processing import Processing
from kMerTableData import KMerTableData
import pandas as pd
import os


class KMerScatterPlotData(Processing):

    def __init__(self, data, selected, k, peak, top):
        super().__init__(data, selected, k, peak, top)

    def processData(self):
        fileNames = self.getSettings().getSelected()

        xAxis = []
        yAxis = []
        label = []

        df_profil1 = pd.DataFrame.from_dict(self.getProfilObj1().getProfile(), orient='index')
        df_profil1.columns = ['Frequency']
        df_profil2 = pd.DataFrame.from_dict(self.getProfilObj2().getProfile(), orient='index')
        df_profil2.columns = ['Frequency']

        file1_kmer = df_profil1.index.tolist()
        file2_kmer = df_profil2.index.tolist()

        file1_freq = df_profil1['Frequency'].tolist()
        file2_freq = df_profil2['Frequency'].tolist()

        # calculates coordinates

        intersec = set(file1_kmer).intersection(file2_kmer)  # ascertains kmeres which appear in both files

        for kmer in intersec:
            idx1 = file1_kmer.index(kmer)
            idx2 = file2_kmer.index(kmer)

            xAxis.append(file1_freq[idx1])
            yAxis.append(file2_freq[idx2])
            label.append(self.unranking(kmer))

            file1_kmer.remove(kmer)
            file2_kmer.remove(kmer)
            del file1_freq[idx1]
            del file2_freq[idx2]

        for i in range(0, len(file1_kmer)):
            xAxis.append(file1_freq[i])
            yAxis.append(0)
            label.append(self.unranking(file1_kmer[i]))

        for j in range(0, len(file2_kmer)):
            xAxis.append(0)
            yAxis.append(file2_freq[j])
            label.append(self.unranking(file2_kmer[j]))

        fileName1 = os.path.basename(fileNames[0])
        fileName2 = os.path.basename(fileNames[1])

        result_df = pd.DataFrame(xAxis, index=label, columns=[fileName1])
        result_df[fileName2] = yAxis
        result_df['highlight'] = False

        df = KMerTableData.processData(self)  # get top kmeres
        kmerList = df.index.tolist()
        for kmer in kmerList:
            result_df.loc[kmer, 'highlight'] = True

        return [result_df, label, [fileName1, fileName2]]

