class Setting:
    data = None
    selected = None
    k = 0
    peak = 0
    top = 0
    highlight = 0

    def __init__(self, data, selected, k, peak, top, highlight):
        self.data = data
        self.selected = selected
        self.k = k
        self.peak = peak
        self.top = top
        self.highlight = highlight

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

    def setHighlight(self, highlight):
        self.highlight = highlight

    def getData(self):
        return self.data

    def getSelected(self):
        return self.selected

    def getK(self):
        return self.k

    def getPeak(self):
        return self.peak

    def getTop(self):
        return self.top

    def getHighlight(self):
        return self.highlight
