import os

from src.inputValueException import InputValueException
from src.processing import Processing
import pandas as pd
import re
from sklearn.decomposition import PCA


# counts triplets and number of nucleic acids in kmer
def fillDataFrame(df, all_triplets):
    alphabet = ['A', 'C', 'G', 'T']
    top_list_df = df.copy()
    del top_list_df['File']

    # add columns
    for b in alphabet:
        top_list_df[b] = 0

    for tpl in all_triplets:
        top_list_df[tpl] = 0

    # counts nucleotides in kmer
    for b in alphabet:
        top_list_df[b] = [kmer.upper().count(b) for kmer in top_list_df.index.tolist()]

    # counts triplets in kmer
    for trpl in all_triplets:
        top_list_df[trpl] = [sum(1 for _ in re.finditer('(?={})'.format(trpl), kmer.upper())) for kmer in
                             top_list_df.index.tolist()]

    return top_list_df


# inherits from process
# implements processData for pca
class KMerPCAData(Processing):

    def __init__(self, data, selected, k, peak, top, feature):
        super().__init__(data, selected, k, peak, top, feature)

    # processes data to display pca as scatterplot
    def processData(self):
        top_kmer = self.getTopKmer()
        all_triplets = self.getAllTriplets()

        file_name1 = os.path.basename(self.getProfilObj1().getName())  # get filenames
        file_name2 = os.path.basename(self.getProfilObj2().getName())

        top_list_file1 = top_kmer.query('File==@file_name1')  # get top kmeres
        top_list_file2 = top_kmer.query('File==@file_name2')  # get top kmeres

        pca = PCA(n_components=2)

        pca_df1 = None
        pca_df2 = None
        top_list_df1 = None
        top_list_df2 = None

        # create dataframe
        if len(top_list_file1) > 1:
            try:
                top_list_df1 = fillDataFrame(top_list_file1, all_triplets)  # fill remaining data
                pca_data1 = pca.fit_transform(top_list_df1)
                pca_df1 = pd.DataFrame(data=pca_data1, columns=['PC1', 'PC2'], index=top_list_df1.index)
            except ValueError:
                pca_df1 = None

        if len(top_list_file2) > 1:
            try:
                top_list_df2 = fillDataFrame(top_list_file2, all_triplets)
                pca_data2 = pca.fit_transform(top_list_df2)
                pca_df2 = pd.DataFrame(data=pca_data2, columns=['PC1', 'PC2'], index=top_list_df2.index)
            except ValueError:
                pca_df2 = None

        return [pca_df1, pca_df2, file_name1, file_name2, top_list_df1, top_list_df2]
