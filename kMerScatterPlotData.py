from processing import Processing
from kMerTableData import KMerTableData
import pandas


class KMerScatterPlotData(Processing):

    def __init__(self, data, selected, k, peak, top):
        super().__init__(data, selected, k, peak, top)

    def processData(self):
        df = KMerTableData.processData(self)  # get top kmeres
        top = self.getSettings().getTop()
        freq = df['Frequency'].tolist()
        kmer = df.index.tolist()

        fileNames = df['File'].drop_duplicates().tolist()

        file1_freq = []
        file2_freq = []

        file1_kmer = []
        file2_kmer = []

        xAxis = []
        yAxis = []
        label = []

        for i in range(0, top):  # separates frequencies and kmeres for each file
            file1_freq.append(freq[i])
            file2_freq.append(freq[top + i])

            file1_kmer.append(kmer[i])
            file2_kmer.append(kmer[top + i])

        # calculates coordinates

        intersec = set(file1_kmer).intersection(file2_kmer)  # ascertains kmeres which appear in both files
        for kmer in intersec:
            idx1 = file1_kmer.index(kmer)
            idx2 = file2_kmer.index(kmer)

            xAxis.append(file1_freq[idx1])
            yAxis.append(file2_freq[idx2])
            label.append(kmer)

            file1_kmer.remove(kmer)
            file2_kmer.remove(kmer)
            del file1_freq[idx1]
            del file2_freq[idx2]

        for i in range(0, len(file1_kmer)):
            xAxis.extend([file1_freq[i], 0])
            yAxis.extend([0, file2_freq[i]])
            label.extend([file1_kmer[i], file2_kmer[i]])

        return [xAxis, yAxis, label, fileNames]
