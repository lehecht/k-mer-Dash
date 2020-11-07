from src.processing import Processing
import os
import pandas as pd
from sklearn.decomposition import PCA
from sklearn import preprocessing


def sortTripleList(kmer):
    list = []
    for i in range(0, len(kmer) - 3 + 1):
        list.append(kmer[i:i + 3])
    return list

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
        top_list_df1 = pd.DataFrame.from_dict(top_list_file1, orient='index', columns=['Frequency'])
        top_list_df2 = pd.DataFrame.from_dict(top_list_file2, orient='index', columns=['Frequency'])

        # add columns
        for b in alphabet:
            top_list_df1[b] = 0
            top_list_df2[b] = 0

        for tpl in all_tripplets:
            top_list_df1[tpl] = 0
            top_list_df2[tpl] = 0

        # fill new columns
        for i in range(0, len(top_list_df2)):
            kmer1 = top_list_df1.index.tolist()[i]
            kmer2 = top_list_df2.index.tolist()[i]

            case_insens_kmer1 = top_list_df1.index.tolist()[i].upper()
            case_insens_kmer2 = top_list_df2.index.tolist()[i].upper()

            for b in alphabet:
                top_list_df1.loc[kmer1, b] = case_insens_kmer1.count(b)
                top_list_df2.loc[kmer2, b] = case_insens_kmer2.count(b)

            for trpl in all_tripplets:
                if trpl in case_insens_kmer1:
                    top_list_df1.loc[kmer1, trpl] += 1
                if trpl in case_insens_kmer2:
                    top_list_df2.loc[kmer2, trpl] += 1

        # print(top_list_df2[top_list_df2.index == 'TGTTT'])
        # print(top_list_df2[top_list_df2.index == 'TTTAA'])
        # print(top_list_df2[top_list_df2.index == 'GGTGT'])

        test_df = top_list_df2.loc[:,'AAA':'TTT']
        # print(test)
        sum = test_df.sum(axis=0)
        # cols = sum[sum > 5].index.tolist()
        cols = sum[sum > 5]
        cols = cols.sort_values(ascending=True)
        cols = cols.index.tolist()[0:10]
        # print(cols)



        # newDf = top_list_df2.loc[:,'Frequency':'T']
        # # print(newDf)
        # cut = top_list_df2[cols]
        # newDf = newDf.join(cut)
        # print(len(top_list_df2))


        a = {'A': 0, 'C': 1, 'G': 2, 'T': 3}

        homogeneity = []
        t_dict = {}

        for i in range(1, len(all_tripplets) + 1):
            t_dict[all_tripplets[i - 1]] = i

        best_t = []
        order = []
        for kmer in top_list_df2.index.tolist():
            row = top_list_df2.loc[kmer, 'A':]
            data = row[row != 0]
            max = data.max()
            b = data[data == max].index.tolist()[0]
            homo = max/K
            # tripplets_list = [elem for elem in data.index.tolist() if len(elem) == 3]
            # tripplets_list.sort()
            i = 0
            tripplets_list = sortTripleList(kmer)
            trp = ''
            for t in tripplets_list:
                if t in cols:
                    i+=1
                trp = trp + str(t_dict[t])
            best_t.append(i)
            order.append(trp)
            homogeneity.append(homo)
        # print(order)
        # print(somelist)

        newDf = pd.DataFrame(homogeneity, columns=['Homogeneity'], index=top_list_df2.index)
        newDf2 = pd.DataFrame(order, columns=['Order'], index=top_list_df2.index)
        newDf3 = pd.DataFrame(best_t, columns=['best'], index=top_list_df2.index)
        # newDf = pd.DataFrame(order, columns=['Order'], index=top_list_df2.index)

        test = top_list_df2.loc[:, 'Frequency':'T']
        # test = top_list_df2.loc[:, ['Frequency','T']]
        # test = top_list_df2.loc[:, 'Frequency']
        # test = top_list_df2.loc[:, ['Frequency','C','T']]
        # test = pd.DataFrame(test)

        newDf = test.join(newDf)
        newDf = newDf.join(newDf2)
        newDf = newDf.join(newDf3)


        print(newDf.head())

        pca = PCA(n_components=2)
        # scaled_data1 = preprocessing.scale(top_list_df1)
        # scaled_data2 = preprocessing.scale(top_list_df2)
        scaled_data2 = preprocessing.scale(newDf)
        # pca_data1 = pca.fit_transform(scaled_data1)
        # pca_data2 = pca.fit_transform(scaled_data2)

        # pca_data2 = pca.fit_transform(top_list_df2)

        pca_data2 = pca.fit_transform(scaled_data2)
        # pca_df = pd.DataFrame(data=pca_data1, columns=test.columns.tolist(),index=top_list_df1.index)
        # pca_df = pd.DataFrame(data=pca_data1, columns=['PC2','PC1'], index=top_list_df1.index)
        pca_df = pd.DataFrame(data=pca_data2, columns=['PC1', 'PC2'], index=top_list_df2.index)

        return pca_df
