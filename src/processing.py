from src.setting import *
from src.fileCountException import *
from src.calcKmerLists import *
from src.profile import Profile


# abstract class
class Processing:
    profile1 = None
    profile2 = None
    setting = None
    df = None
    top_kmer_df = None

    def __init__(self, data, selected, k, peak, top):
        if selected is not None:
            self.setting = Setting(data, selected, k, peak, top)
        elif len(data) >= 2:
            selected = data[:2]
            self.setting = Setting(data, selected, k, peak, top)
        else:
            raise FileCountException

        self.profile1 = Profile(dict(), selected[0])
        self.profile2 = Profile(dict(), selected[1])
        self.profile1.setProfile(calcFrequency(k, selected)[0])
        self.profile2.setProfile(calcFrequency(k, selected)[1])
        self.df = createDataFrame(self.profile1, self.profile2, selected)
        self.top_kmer_df = calcTopKmer(top, self.profile1, self.profile2)

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
