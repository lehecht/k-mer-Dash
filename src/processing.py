from src.setting import *
from src.fileCountException import *
from src.calcKmerLists import *
from src.profile import Profile
from itertools import combinations_with_replacement, permutations


# abstract class
class Processing:
    profile1 = None
    profile2 = None
    setting = None
    df = None
    top_kmer_df = None
    all_tripplets = None

    def __init__(self, data, selected, k, peak, top, highlight):
        if selected is not None:
            self.setting = Setting(data, selected, k, peak, top, highlight)
        elif len(data) >= 2:
            selected = data[:2]
            self.setting = Setting(data, selected, k, peak, top, highlight)
        else:
            raise FileCountException

        self.profile1 = Profile(dict(), selected[0])
        self.profile2 = Profile(dict(), selected[1])

        self.profile1.setProfile(calcFrequency(k, peak, selected)[0])
        self.profile2.setProfile(calcFrequency(k, peak, selected)[1])

        if top > len(self.profile1.getProfile()) or top > len(self.profile2.getProfile()):
            print("WARNING: top-value is greater than amount of entries.")
            print("All entries will be displayed.")
            self.setting.setTop(None)
            top = None

        self.df = createDataFrame(self.profile1, self.profile2, selected)
        self.top_kmer_df = calcTopKmer(top, self.profile1, self.profile2)

        self.all_tripplets = []
        tripplet_comb = list(combinations_with_replacement(['A', 'C', 'G', 'T'], r=3))

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
