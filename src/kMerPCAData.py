from src.processing import Processing
import os
import pandas as pd
from sklearn.decomposition import PCA


# counts tripplets and number of nucleic acids
def fillDataFrame(df, all_tripplets):
    alphabet = ['A', 'C', 'G', 'T']
    top_list_df = pd.DataFrame.from_dict(df, orient='index', columns=['Frequency'])

    # add columns
    for b in alphabet:
        top_list_df[b] = 0

    for tpl in all_tripplets:
        top_list_df[tpl] = 0

    for i in range(0, len(top_list_df)):
        kmer1 = top_list_df.index.tolist()[i]

        case_insens_kmer1 = top_list_df.index.tolist()[i].upper()

        for b in alphabet:
            top_list_df.loc[kmer1, b] = case_insens_kmer1.count(b)

        for trpl in all_tripplets:
            if trpl in case_insens_kmer1:
                top_list_df.loc[kmer1, trpl] += 1

    return top_list_df


class KMerPCAData(Processing):

    def __init__(self, data, selected, k, peak, top):
        super().__init__(data, selected, k, peak, top)

    def processData(self):
        TOP_VALUES = self.getSettings().getTop()
        K = self.getSettings().getK()
        alphabet = ['A', 'C', 'G', 'T']
        all_tripplets = self.getAllTripplets()

        fileName1 = os.path.basename(self.getSettings().getSelected()[0])
        fileName2 = os.path.basename(self.getSettings().getSelected()[1])

        df = self.getDF().copy()

        df_file1 = df.sort_values(by=[fileName1], ascending=False)
        df_file2 = df.sort_values(by=[fileName2], ascending=False)

        df_val1 = df_file1[fileName1].values.tolist()
        df_val2 = df_file2[fileName2].values.tolist()

        df_sorted_data_f1 = list(set(df_val1[:TOP_VALUES]))
        df_sorted_data_f2 = list(set(df_val2[:TOP_VALUES]))

        top_list_file1 = dict()
        top_list_file2 = dict()

        # find max and create dict
        for i in range(0, len(df_sorted_data_f1)):
            max1 = df_sorted_data_f1[i]

            max_kmere_f1 = df[df[fileName1] == max1].index.tolist()

            for kmer in max_kmere_f1:
                top_list_file1[kmer] = max1

        for i in range(0, len(df_sorted_data_f2)):
            max2 = df_sorted_data_f2[i]

            max_kmere_f2 = df[df[fileName2] == max2].index.tolist()

            for kmer in max_kmere_f2:
                top_list_file2[kmer] = max2

        # create dataframe
        top_list_df1 = fillDataFrame(top_list_file1, all_tripplets)
        top_list_df2 = fillDataFrame(top_list_file2, all_tripplets)

        pca = PCA(n_components=2)

        pca_data1 = pca.fit_transform(top_list_df1)
        pca_data2 = pca.fit_transform(top_list_df2)
        pca_df1 = pd.DataFrame(data=pca_data1, columns=['PC1', 'PC2'], index=top_list_df1.index)
        pca_df2 = pd.DataFrame(data=pca_data2, columns=['PC1', 'PC2'], index=top_list_df2.index)

        return [pca_df1, pca_df2, fileName1, fileName2, top_list_df1['T'], top_list_df2['T']]
