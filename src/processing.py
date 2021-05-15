from src.setting import *
from src.fileCountException import *
from src.calcKmerLists import *
from src.profile import Profile
from itertools import combinations_with_replacement, permutations
import os


# abstract class
class Processing:
    profile1 = None  # dictionary for kmers and their frequencies for file1
    profile2 = None  # dictionary for kmers and their frequencies for file2
    setting = None  # object containing all information, which are needed for calculation
    df = None  # table which contains kmer-frequencies as coordinates (kmer: x:(file1) = fre1,y:(file2)= fre2)
    top_kmer_df = None  # table of top kmers
    all_triplets = None  # list of all combinations of triplets
    seq_len = None  # sequence length

    # data: file input list
    # selected: two files, which are processed
    # k: kmer length
    # peak: peak: peak-position, where sequences should be aligned
    # top: number of best values
    # feature: number of T or kmer-Frequency for pcas
    # cmd: bool, determines if second profile should be created
    def __init__(self, data, selected, k, peak, top, feature,cmd):
        if selected is not None:
            self.setting = Setting(data, selected, k, peak, top, feature)

        # calculates kmer-frequency dictionaries
        self.profile1 = Profile(calcFrequency(k, peak, selected)[0], selected[0])
        if not cmd:
            self.profile2 = Profile(calcFrequency(k, peak, selected)[1], selected[1])

        self.seq_len = getSeqLength(selected[0])

        # smallest sequence length between both files is set as default
        # if seq1_len < seq2_len:
        #     self.seq_len = seq1_len
        # else:
        #     self.seq_len = seq2_len

        len_p1 = len(self.profile1.getProfile())  # dict length
        if not cmd:
            len_p2 = len(self.profile2.getProfile())

        # checks if top-value is greater than one of profile lengths
        # if so, top is set on None

        top_value_msg1 = "INFO: top-value is greater than amount of calculated entries for one or more files."
        top_value_msg2 = "All entries will be displayed."

        if not cmd:
            if (not top is None) and (top > len_p1 or top > len_p2) and ((len_p1 is not 0) and (len_p2 is not 0)):
                print(top_value_msg1)
                print(top_value_msg2)
                self.setting.setTop(None)
                top = None
        else:
            if (not top is None) and (top > len_p1) and (len_p1 is not 0):
                print(top_value_msg1)
                print(top_value_msg2)
                self.setting.setTop(None)
                top = None

        if not cmd:
            # calculates dataframe
            self.df = createDataFrame(self.profile1, self.profile2, selected)

            # calculates top-kmer dataframe
            self.top_kmer_df = calcTopKmer(top, self.profile1, self.profile2)

            # calculates all possible triples from dna-bases
            self.all_triplets = []
            triplet_comb = list(combinations_with_replacement(['A', 'C', 'G', 'T'], r=3))

            for trip in triplet_comb:
                comb = list(set(permutations(trip)))
                self.all_triplets.extend([''.join(comb[i]) for i in range(0, len(comb))])

        else:
            self.top_kmer_df = calcTopKmer(top, self.profile1, None)

        # abstract method

    def processData(self):
        pass

    def getProfilObj1(self):
        return self.profile1

    def getProfilObj2(self):
        return self.profile2

    def getSettings(self):
        return self.setting

    def getDF(self):
        return self.df

    def getTopKmer(self):
        return self.top_kmer_df

    def getAllTriplets(self):
        return self.all_triplets

    def getSeqLen(self):
        return self.seq_len
