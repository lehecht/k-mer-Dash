from Bio import SeqIO
from kValueException import KValueException
import os
import pandas as pd
import math

alphabet = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
alpha_size = len(alphabet)


def ranking(kmer, k):  # Rising Ranking Function
    res = 0
    for i in range(0, k):
        res = res + alphabet[kmer[i]] * alpha_size ** i
    return res


def unranking(int_kmer, k):  # Decodes integer to kmer
    rest = -1
    int_kmer_rest = int_kmer
    kmer = []
    while rest != 0:
        rest = int(int_kmer_rest / alpha_size)  # encodes kmer-body without its head
        int_kmer_rest = (int_kmer_rest % alpha_size)  # encodes head
        kmer.append(list(alphabet.keys())[int_kmer_rest])
        int_kmer_rest = rest

    kmer = ''.join(kmer)  # joins list of single character to string
    if len(kmer) < k:  # fills kmer with consecutive 'A's, if kmer length does not equal k
        diff = k - len(kmer)
        kmer = kmer + 'A' * diff
    return kmer


def calcFrequency(k, selected):  # throws kValueException
    profil1 = dict()
    profil2 = dict()
    kmer_ranked = 0
    for file in selected:  # selects data
        if file == selected[0]:
            profile = profil1
        else:
            profile = profil2
        for record in SeqIO.parse(file, "fasta"):  # reads fasta-file
            sequence = record.seq
            if len(sequence) <= k:
                raise KValueException  # is thrown if k is greater or equal than sequence length
            for i in range(0, (len(sequence) - k + 1)):  # calculates kmere-rankings
                kmer = sequence[i:(k + i)]
                if i == 0:
                    kmer_ranked = ranking(kmer, k)
                else:  # frame-shifting
                    kmer_ranked_tail = math.floor(kmer_ranked / alpha_size)  # remove head of kmer
                    kmer_ranked = kmer_ranked_tail + alphabet[
                        sequence[k + i - 1]] * alpha_size ** (k - 1)  # add last ranked char
                try:
                    profile[kmer_ranked] += 1
                except KeyError:
                    profile[kmer_ranked] = 1
    return [profil1, profil2]


def createDataFrame(k, p1, p2, selected):
    xAxis = []  # frequency count from file 1
    yAxis = []  # frequency count from file 2
    kmer_List = []

    file1_kmer = list(p1.getProfile().keys())
    file2_kmer = list(p2.getProfile().keys())

    file1_freq = list(p1.getProfile().values())
    file2_freq = list(p2.getProfile().values())

    # calculates coordinates

    intersec = set(file1_kmer).intersection(file2_kmer)  # ascertains kmeres which appear in both files

    for kmer in intersec:
        idx1 = file1_kmer.index(kmer)
        idx2 = file2_kmer.index(kmer)

        xAxis.append(file1_freq[idx1])
        yAxis.append(file2_freq[idx2])
        kmer_List.append(unranking(kmer, k))

        file1_kmer.remove(kmer)
        file2_kmer.remove(kmer)
        del file1_freq[idx1]
        del file2_freq[idx2]

    for i in range(0, len(file1_kmer)):
        xAxis.append(file1_freq[i])
        yAxis.append(0)
        kmer_List.append(unranking(file1_kmer[i], k))

    for j in range(0, len(file2_kmer)):
        xAxis.append(0)
        yAxis.append(file2_freq[j])
        kmer_List.append(unranking(file2_kmer[j], k))

    fileName1 = os.path.basename(selected[0])
    fileName2 = os.path.basename(selected[1])

    res = pd.DataFrame(xAxis, index=kmer_List, columns=[fileName1])
    res[fileName2] = yAxis

    return res


def calcTopKmer(k, top, p1, p2):
    profile1 = p1.getProfile().copy()
    profile2 = p2.getProfile().copy()

    fileName1 = os.path.basename(p1.getName())
    fileName2 = os.path.basename(p2.getName())

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

        p1_top_list_kmer.append(unranking(max1_key, k))
        p2_top_list_kmer.append(unranking(max2_key, k))

        p1List = p1List.drop(max1_key)  # delete max entry to find next max-entry
        p2List = p2List.drop(max2_key)

    p1_top_list_val.extend(p2_top_list_val)  # connects list entries to one list
    p1_top_list_kmer.extend(p2_top_list_kmer)
    p1_fileName.extend(p2_fileName)

    res = pd.DataFrame(p1_top_list_val, index=p1_top_list_kmer, columns=['Frequency'])
    res['File'] = p1_fileName  # append Filename column
    return res
