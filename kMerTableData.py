from processing import Processing
import pandas as pd
import os


class KMerTableData(Processing):

    def __init__(self, data, selected, k, peak, top):
        super().__init__(data, selected, k, peak, top)

    def processData(self):
        top = self.getSettings().getTop()

        profilObj1 = self.getProfilObj1()
        profilObj2 = self.getProfilObj2()

        profile1 = profilObj1.getProfile().copy()
        profile2 = profilObj2.getProfile().copy()

        fileName1 = os.path.basename(profilObj1.getName())
        fileName2 = os.path.basename(profilObj2.getName())

        p1List = pd.DataFrame.from_dict(profile1, orient='index')  # create Dataframe from calculated frequency-table
        p1List.columns = ['Frequency']

        p2List = pd.DataFrame.from_dict(profile2, orient='index')
        p2List.columns = ['Frequency']

        p1_top_list_val = []
        p2_top_list_val = []

        p1_top_list_kmer = []
        p2_top_list_kmer = []

        p1_fileName = []
        p2_fileName = []

        for i in range(0, top):
            p1_fileName.append(fileName1)
            p2_fileName.append(fileName2)

            max1 = p1List.max().tolist()[0]  # get entry with max Frequency
            max2 = p2List.max().tolist()[0]

            p1_top_list_val.append(max1)
            p2_top_list_val.append(max2)

            max1_key = p1List.query('Frequency==@max1').index.tolist()[0]  # get key of max-frequency entry
            max2_key = p2List.query('Frequency==@max2').index.tolist()[0]  # the key encodes the kmer

            p1_top_list_kmer.append(self.unranking(max1_key))
            p2_top_list_kmer.append(self.unranking(max2_key))

            p1List = p1List.drop(max1_key)  # delete max entry to find next max-entry
            p2List = p2List.drop(max2_key)

        p1_top_list_val.extend(p2_top_list_val)  # connects list entries to one list
        p1_top_list_kmer.extend(p2_top_list_kmer)
        p1_fileName.extend(p2_fileName)

        res = pd.DataFrame(p1_top_list_val, index=p1_top_list_kmer, columns=['Frequency'])
        res['File'] = p1_fileName  # append Filename column


        return res
