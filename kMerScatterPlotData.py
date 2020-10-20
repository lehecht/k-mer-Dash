from processing import Processing
from Bio import SeqIO


class KMerScatterPlotData(Processing):

    def __init__(self, data, selected, k, peak, top):
        super().__init__(data, selected, k, peak, top)

    def processData(self):
        cpyProfil1 = self.getProfilObj1().getProfile().copy()
        cpyProfil2 = self.getProfilObj2().getProfile().copy()
        top = self.getSettings().getTop()
        k = self.getSettings().getK()

        x_coordinates = []
        y_coordinates = []
        kmer_info = []

        int_max_kmer_list1 = []
        int_max_kmer_list2 = []





    # for i in range(0, min(top, len(cpyProfil1), len(cpyProfil2))):
    #     maxVal1 = max(cpyProfil1, key=cpyProfil1.get)
    #     maxVal2 = max(cpyProfil2, key=cpyProfil2.get)
    #
    #     int_max_kmer_list1.append(maxVal1)
    #     int_max_kmer_list2.append(maxVal2)
    #
    #     cpyProfil1.pop(maxVal1)
    #     cpyProfil2.pop(maxVal2)
    #
    # cpyProfil1 = self.getProfilObj1().getProfile().copy()  # reset edited profile1
    # cpyProfil2 = self.getProfilObj2().getProfile().copy()  # reset edited profile2
    #
    # intersec = list(set(int_max_kmer_list1).intersection(int_max_kmer_list2))
    # print(intersec)
    # if len(intersec) != 0:
    #     for coord in intersec:
    #         x_coordinates.append(cpyProfil1[coord])
    #         y_coordinates.append(cpyProfil2[coord])
    #
    #         kmer_info.append(self.unranking(coord))
    #
    #         int_max_kmer_list1.pop(coord)
    #         int_max_kmer_list2.pop(coord)
    #
    # for x in int_max_kmer_list1:
    #     x_coordinates.append(x)
    #     y_coordinates.append(0)
    #     x_int_kmer = list(cpyProfil1.keys())[list(cpyProfil1.values()).index(x)]
    #     kmer_info.append(self.unranking(x_int_kmer))
    #
    # for y in int_max_kmer_list2:
    #     x_coordinates.append(0)
    #     y_coordinates.append(y)
    #     y_int_kmer = list(cpyProfil2.keys())[list(cpyProfil2.values()).index(y)]
    #     kmer_info.append(self.unranking(y_int_kmer))

