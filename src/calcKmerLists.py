from Bio import SeqIO
from src.inputValueException import InputValueException
import os
import pandas as pd


# calculates kmer frequencies
# k: kmer-length
# peak: peak-position, where sequences should be aligned
# selected: input files
def calcFrequency(k, peak, selected):
    profile1 = dict()  # for file1
    profile2 = dict()  # for file2
    kmer = ''
    for file in selected:  # selects data
        if file == selected[0]:  # Name of first File
            profile = profile1
        else:
            profile = profile2
        for record in SeqIO.parse(file, "fasta"):  # reads fasta-file
            sequence = str(record.seq)
            seq_length = len(sequence)
            if peak is not None:
                if seq_length < peak:  # is thrown if peak is greater than sequence length
                    raise InputValueException('Invalid peak: must be smaller than sequence length or equal')
                sequence = createPeakPosition(peak, sequence)
            if seq_length <= k:
                raise InputValueException(  # is thrown if k is greater or equal than sequence length
                    "Invalid k: must be smaller than sequence length")
            # kmer frequency counting:
            for i in range(0, (seq_length - k + 1)):
                if i == 0:
                    kmer = sequence[0:k]  # init first kmer
                else:
                    kmer = ''.join([kmer[1:], sequence[k + i - 1]])
                try:
                    profile[kmer] += 1
                except KeyError:
                    profile[kmer] = 1
    return [profile1, profile2]


# determines sequence length of first sequence of file
# it is assumed, that every sequence has same length
# file: not empty fasta file
def getSeqLength(file):
    records = list(SeqIO.parse(file, "fasta").records)
    seq_len = len(records[0].seq)
    return seq_len


# changes sequence with only capital letters to sequence with only one capital letter (peak position)
# peak: peak-position, where sequences should be aligned
# seq: sequence
def createPeakPosition(peak, seq):
    sequence = seq.lower()
    peak_val = seq[peak - 1]
    res = ''.join([sequence[:peak - 1], peak_val, sequence[peak:]])
    return res


# table which contains kmer-frequencies as coordinates (kmer: x:(file1) = fre1,y:(file2)= fre2)
def createDataFrame(p1, p2, selected):
    x_axis = []  # frequency count from file 1
    y_axis = []  # frequency count from file 2
    kmer_list = []
    profile1 = p1.getProfile()
    profile2 = p2.getProfile()

    file1_kmer = list(p1.getProfile().keys())

    file2_kmer = list(p2.getProfile().keys())

    # calculates coordinates
    intersec = set(file1_kmer).intersection(file2_kmer)  # ascertains kmeres which appear in both files

    # all kmers, which are in profile1 but not in profile2
    p1_diff = set(file1_kmer).difference(file2_kmer)

    # all kmers, which are in profile2 but not in profile1
    p2_diff = set(file2_kmer).difference(file1_kmer)

    for kmer in intersec:
        x_axis.append(profile1[kmer])
        y_axis.append(profile2[kmer])

        kmer_list.append(kmer)

    for k1 in p1_diff:
        kmer_freq = profile1[k1]
        x_axis.append(kmer_freq)
        y_axis.append(0)
        kmer_list.append(k1)

    for k2 in p2_diff:
        kmer_freq = profile2[k2]
        x_axis.append(0)
        y_axis.append(kmer_freq)
        kmer_list.append(k2)

    file_name1 = os.path.basename(selected[0])
    file_name2 = os.path.basename(selected[1])

    res = pd.DataFrame(x_axis, index=kmer_list, columns=[file_name1])
    res[file_name2] = y_axis

    return res


# creates table with only top k-mers
# top: number of best values
# p1/p2: dictionary with kmers and their frequencies
def calcTopKmer(top, p1, p2):
    profile1 = p1.getProfile().copy()
    file_name1 = os.path.basename(p1.getName())
    profile1 = list(map((lambda e: (e[0], e[1], file_name1)),
                        list(profile1.items())))  # creates list of triples (kmer, frequency, filename)
    profile1.sort(key=(lambda item: item[1]), reverse=True)

    if not p2 is None:
        profile2 = p2.getProfile().copy()
        file_name2 = os.path.basename(p2.getName())
        profile2 = list(map((lambda e: (e[0], e[1], file_name2)), list(profile2.items())))
        profile2.sort(key=(lambda item: item[1]), reverse=True)

    if top is not None:
        profile1_top = profile1[:top]
        if not p2 is None:
            profile2_top = profile2[:top]

        if not p2 is None:
            profiles = [profile1, profile2]
        else:
            profiles = [profile1]

        # checks if only last of top values appears several times in profile
        for p in profiles:
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

        if not p2 is None:
            profile2_top = profile2.copy()

    all_kmer = profile1_top

    if not p2 is None:
        all_kmer.extend(profile2_top)

    top_kmer = pd.DataFrame(all_kmer, columns=['', 'Frequency', 'File'])
    top_kmer = top_kmer.set_index('')

    return top_kmer
