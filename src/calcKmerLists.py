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
                if k < peak:  # is thrown if peak is greater than sequence length
                    raise InputValueException('Invalid peak: must be smaller than k-Mer length or equal')
                sequence = createPeakPosition(peak, sequence)
            if seqLength <= k:
                raise InputValueException(  # is thrown if k is greater or equal than sequence length
                    "Invalid k: must be smaller than sequence length")
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

    profile1 = list(map((lambda e: (e[0], e[1], fileName1)),
                        list(profile1.items())))  # creates list of triples (kmer, frequency, filename)
    profile2 = list(map((lambda e: (e[0], e[1], fileName2)), list(profile2.items())))

    profile1.sort(key=(lambda item: item[1]), reverse=True)
    profile2.sort(key=(lambda item: item[1]), reverse=True)

    if top is not None:
        profile1_top = profile1[:top]
        profile2_top = profile2[:top]

        for p in [profile1, profile2]:
            dup_kmer_freq = []
            for i in range(top, len(p)):
                next_kmer_freq = p[i][1]
                if p[i - 1][1] == next_kmer_freq:
                    dup_kmer_freq.append(p[i])
                else:
                    break
            if p == profile1:
                profile1_top.extend(dup_kmer_freq)
            else:
                profile2_top.extend(dup_kmer_freq)

    else:
        profile1_top = profile1.copy()
        profile2_top = profile2.copy()

    allKmer = profile1_top
    allKmer.extend(profile2_top)

    topKmer = pd.DataFrame(allKmer, columns=['', 'Frequency', 'File'])
    topKmer = topKmer.set_index('')

    return topKmer
