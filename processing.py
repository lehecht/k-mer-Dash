from setting import *
from fileCountException import *
from kValueException import *
from profile import Profile
from Bio import SeqIO
import math


# abstract class
class Processing:
    profile1 = None
    profile2 = None
    setting = None

    alphabet = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
    alpha_size = len(alphabet)

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
        self.calcFrequency()

    # abstract method
    def processData(self):
        pass

    def ranking(self, kmer):  # Rising Ranking Function
        res = 0
        for i in range(0, self.getSettings().getK()):
            res = res + self.alphabet[kmer[i]] * self.alpha_size ** i
        return res

    def unranking(self, int_kmer):  # Decodes integer to kmer
        k = self.getSettings().getK()
        rest = -1
        int_kmer_rest = int_kmer
        kmer = []
        while rest != 0:
            rest = int(int_kmer_rest / self.alpha_size)  # encodes kmer-body without its head
            int_kmer_rest = (int_kmer_rest % self.alpha_size)  # encodes head
            kmer.append(list(self.alphabet.keys())[int_kmer_rest])
            int_kmer_rest = rest

        kmer = ''.join(kmer)  # joins list of single character to string
        if len(kmer) < k:  # fills kmer with consecutive 'A's, if kmer length does not equal k
            diff = k - len(kmer)
            kmer = kmer + 'A' * diff
        return kmer

    def calcFrequency(self):  # throws kValueException
        kmer_ranked = 0
        k = self.setting.getK()
        for file in self.setting.getSelected():  # selects data
            if file == self.getProfilObj1().getName():
                profile = self.getProfilObj1().getProfile()
            else:
                profile = self.getProfilObj2().getProfile()
            for record in SeqIO.parse(file, "fasta"):  # reads fasta-file
                sequence = record.seq
                if len(sequence) <= k:
                    raise KValueException  # is thrown if k is greater or equal than sequence length
                for i in range(0, (len(sequence) - k + 1)):  # calculates kmere-rankings
                    kmer = sequence[i:(k + i)]
                    if i == 0:
                        kmer_ranked = self.ranking(kmer)
                    else:  # frame-shifting
                        kmer_ranked_tail = math.floor(kmer_ranked / self.alpha_size)  # remove head of kmer
                        kmer_ranked = kmer_ranked_tail + self.alphabet[
                            sequence[k + i - 1]] * self.alpha_size ** (k - 1)  # add last ranked char
                    try:
                        profile[kmer_ranked] += 1
                    except KeyError:
                        profile[kmer_ranked] = 1

    def getProfilObj1(self):
        return self.profile1

    def getProfilObj2(self):
        return self.profile2

    def getSettings(self):
        return self.setting
