class Setting:
    data = None  # data: file input list
    selected = None  # selected: two files, which are processed
    sec_struct_data = None  # sec_struct_data: list of structural data
    feature = None  # feature: number of T or kmer-Frequency for pcas
    k = 0  # k: kmer length
    peak = 0  # peak: peak: peak-position, where sequences should be aligned
    top = 0  # top: number of best values

    def __init__(self, data, selected, k, peak, top, feature, secStruct_data):
        self.data = data
        self.selected = selected
        self.k = k
        self.peak = peak
        self.top = top
        self.feature = feature
        self.sec_struct_data = secStruct_data

    def setData(self, data):
        self.data = data

    def setSelected(self, selected):
        self.selected = selected

    def setK(self, k):
        self.k = k

    def setPeak(self, peak):
        self.peak = peak

    def setTop(self, top):
        self.top = top

    def setFeature(self, feature):
        self.feature = feature

    def getFeature(self):
        return self.feature

    def getData(self):
        return self.data

    def getSecStrucData(self):
        return self.sec_struct_data

    def getSelected(self):
        return self.selected

    def getK(self):
        return self.k

    def getPeak(self):
        return self.peak

    def getTop(self):
        return self.top
