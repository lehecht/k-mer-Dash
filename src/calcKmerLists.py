from Bio import SeqIO
from src.inputValueException import InputValueException
import os
import pandas as pd


def calcFrequency(k, peak, selected):
    profil1 = dict()
    profil2 = dict()
    kmer = ''
    for file in selected:  # selects data
        if file == selected[0]:  # Name of first File
            profile = profil1
        else:
            profile = profil2
        for record in SeqIO.parse(file, "fasta"):  # reads fasta-file
            sequence = str(record.seq)
            seqLength = len(sequence)
            if peak is not None:
                if seqLength < peak:  # is thrown if peak is greater than sequence length
                    raise InputValueException('Invalid peak: \'peak\' is greater than sequence length')
                sequence = createPeakPosition(peak, sequence)
            if seqLength <= k:
                raise InputValueException(  # is thrown if k is greater or equal than sequence length
                    "Invalid k: \'k\' must be smaller than sequence length")
            for i in range(0, (seqLength - k + 1)):
                if i == 0:
                    kmer = sequence[0:k]  # init first kmer
                else:
                    kmer = ''.join([kmer[1:], sequence[k + i - 1]])
                try:
                    profile[kmer] += 1
                except KeyError:
                    profile[kmer] = 1
    return [profil1, profil2]


def createPeakPosition(peak, seq):
    sequence = seq.lower()
    peakVal = seq[peak - 1]
    res = ''.join([sequence[:peak - 1], peakVal, sequence[peak:]])
    return res


def createDataFrame(p1, p2, selected):
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
        kmer_List.append(kmer)

        file1_kmer.remove(kmer)
        file2_kmer.remove(kmer)
        del file1_freq[idx1]
        del file2_freq[idx2]

    for i in range(0, len(file1_kmer)):
        xAxis.append(file1_freq[i])
        yAxis.append(0)
        kmer_List.append(file1_kmer[i])

    for j in range(0, len(file2_kmer)):
        xAxis.append(0)
        yAxis.append(file2_freq[j])
        kmer_List.append(file2_kmer[j])

    fileName1 = os.path.basename(selected[0])
    fileName2 = os.path.basename(selected[1])

    res = pd.DataFrame(xAxis, index=kmer_List, columns=[fileName1])
    res[fileName2] = yAxis

    return res


def calcTopKmer(top, p1, p2):
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

    if len(profile1) < top:
        print('INFO: Profile is shorter than top-Value')
        print()

    for i in range(0, min(top, len(profile1))):  # TODO: kontrollieren, was bei mehreren Max-Einträgen passiert
        p1_fileName.append(fileName1)
        p2_fileName.append(fileName2)

        max1 = p1List.max().tolist()[0]  # get entry with max Frequency
        max2 = p2List.max().tolist()[0]

        p1_top_list_val.append(max1)
        p2_top_list_val.append(max2)

        max1_key = p1List.query('Frequency==@max1').index.tolist()[0]  # get key of max-frequency entry
        max2_key = p2List.query('Frequency==@max2').index.tolist()[0]  # the key encodes the kmer

        p1_top_list_kmer.append(max1_key)
        p2_top_list_kmer.append(max2_key)

        p1List = p1List.drop(max1_key)  # delete max entry to find next max-entry
        p2List = p2List.drop(max2_key)

    p1_top_list_val.extend(p2_top_list_val)  # connects list entries to one list
    p1_top_list_kmer.extend(p2_top_list_kmer)
    p1_fileName.extend(p2_fileName)

    res = pd.DataFrame(p1_top_list_val, index=p1_top_list_kmer, columns=['Frequency'])
    res['File'] = p1_fileName  # append Filename column
    return res
