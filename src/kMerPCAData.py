from src.processing import Processing
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

    def __init__(self, data, selected, k, peak, top, highlight):
        super().__init__(data, selected, k, peak, top, highlight)

    def processData(self):
        top = self.getSettings().getTop()
        topKmer = self.getTopKmer()
        all_tripplets = self.getAllTripplets()
        p1_len = len(self.getProfilObj1().getProfile())

        fileName1 = topKmer['File'].drop_duplicates().values.tolist()[0]  # get filenames
        fileName2 = topKmer['File'].drop_duplicates().values.tolist()[1]

        if top is not None:
            top_list_file1 = (topKmer['Frequency'].iloc[:top]).to_dict()  # get top kmeres
            top_list_file2 = (topKmer['Frequency'].iloc[top:]).to_dict()
        else:
            top_list_file1 = topKmer['Frequency'].iloc[:p1_len].to_dict()  # get top kmeres
            top_list_file2 = topKmer['Frequency'].iloc[p1_len:].to_dict()

        # create dataframe
        top_list_df1 = fillDataFrame(top_list_file1, all_tripplets)  # fill remaining data
        top_list_df2 = fillDataFrame(top_list_file2, all_tripplets)

        pca = PCA(n_components=2)

        pca_data1 = pca.fit_transform(top_list_df1)
        pca_data2 = pca.fit_transform(top_list_df2)
        pca_df1 = pd.DataFrame(data=pca_data1, columns=['PC1', 'PC2'], index=top_list_df1.index)
        pca_df2 = pd.DataFrame(data=pca_data2, columns=['PC1', 'PC2'], index=top_list_df2.index)

        return [pca_df1, pca_df2, fileName1, fileName2, top_list_df1, top_list_df2]
