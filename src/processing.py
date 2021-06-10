from src.setting import *
from src.fileCountException import *
from src.calcKmerLists import *
from src.profile import Profile
from src.structProfile import StructProfile
from itertools import combinations_with_replacement, permutations
import os


# abstract class
class Processing:
    profile1 = None  # dictionary for kmers and their frequencies for file1
    profile2 = None  # dictionary for kmers and their frequencies for file2
    struct_profile1 = None
    struct_profile2 = None
    no_sec_peak = -1
    # struct_alphabet1 = None
    # struct_alphabet2 = None
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
    def __init__(self, data, selected, k, peak, top, feature, cmd, struct_data,no_sec_peak):
        if selected is not None:
            self.setting = Setting(data, selected, k, peak, top, feature, struct_data)

        top_value_msg1 = "INFO: top-value is greater than amount of calculated entries for one or more files."
        top_value_msg2 = "All entries will be displayed."

        if not cmd:
            self.profile1 = Profile(calcFrequency(k, peak, selected, -1)[0], selected[0])
            self.profile2 = Profile(calcFrequency(k, peak, selected, -1)[1], selected[1])

            len_p1 = len(self.profile1.getProfile())  # dict length
            len_p2 = len(self.profile2.getProfile())

            if (not top is None) and (top > len_p1 or top > len_p2) and ((len_p1 is not 0) and (len_p2 is not 0)):
                print(top_value_msg1)
                print(top_value_msg2)
                self.setting.setTop(None)
                top = None

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

            if not struct_data is None:
                self.no_sec_peak = no_sec_peak
                struct_kmer_list1, struct_alphabet1 = calcFrequency(2, None, [str(struct_data[0])], no_sec_peak)
                print(struct_kmer_list1)
                print(struct_alphabet1)
                self.struct_profile1 = StructProfile(struct_kmer_list1, str(struct_data[0]), struct_alphabet1)
                if len(struct_data) > 1:
                    struct_kmer_list2, struct_alphabet2 = calcFrequency(2, None, [str(struct_data[1])], no_sec_peak)
                    self.struct_profile2 = StructProfile(struct_kmer_list2, str(struct_data[1]), struct_alphabet2)

        else:
            self.profile1 = Profile(calcFrequency(k, peak, selected, False)[0], selected[0])

            len_p1 = len(self.profile1.getProfile())  # dict length

            if (not top is None) and (top > len_p1) and (len_p1 is not 0):
                print(top_value_msg1)
                print(top_value_msg2)
                self.setting.setTop(None)
                top = None

            self.top_kmer_df = calcTopKmer(top, self.profile1, None)

        self.seq_len = getSeqLength(selected[0])

        # abstract method

    def processData(self):
        pass

    def getProfilObj1(self):
        return self.profile1

    def getProfilObj2(self):
        return self.profile2

    def getStructProfil1(self):
        return self.struct_profile1

    def getStructProfil2(self):
        return self.struct_profile2

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

    def getNoSecPeak(self):
        return self.no_sec_peak