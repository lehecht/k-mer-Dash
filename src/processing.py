from src.setting import *
from src.fileCountException import *
from src.calcKmerLists import *
from src.profile import Profile
from itertools import combinations_with_replacement, permutations
import os


# abstract class
class Processing:
    profile1 = None
    profile2 = None
    setting = None
    df = None
    top_kmer_df = None
    all_tripplets = None

    def __init__(self, data, selected, k, peak, top):
        if selected is not None:
            self.setting = Setting(data, selected, k, peak, top)
        elif len(data) >= 2:
            selected = data[:2]
            self.setting = Setting(data, selected, k, peak, top)

        if os.stat(selected[0]).st_size is 0 or os.stat(selected[1]).st_size is 0:
            raise FileCountException('One of the files is empty!')

        self.profile1 = Profile(dict(), selected[0])
        self.profile2 = Profile(dict(), selected[1])

        self.profile1.setProfile(calcFrequency(k, peak, selected)[0])
        self.profile2.setProfile(calcFrequency(k, peak, selected)[1])

        len_p1 = len(self.profile1.getProfile())
        len_p2 = len(self.profile2.getProfile())

        if (top > len_p1 or top > len_p2) and ((len_p1 is not 0) and (len_p2 is not 0)):
            print("WARNING: top-value is greater than amount of entries.")
            print("All entries will be displayed.")
            self.setting.setTop(None)
            top = None

        self.df = createDataFrame(self.profile1, self.profile2, selected)
        self.top_kmer_df = calcTopKmer(top, self.profile1, self.profile2)

        self.all_tripplets = []
        tripplet_comb = list(combinations_with_replacement(['A', 'C', 'G', 'T'], r=3))

        comb = []
        for trip in tripplet_comb:
            comb = list(set(permutations(trip)))
        self.all_tripplets.extend([''.join(comb[i]) for i in range(0, len(comb))])




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

    def getAllTripplets(self):
        return self.all_tripplets
