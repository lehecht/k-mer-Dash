from processing import Processing


class KMerTable(Processing):

    def __init__(self, data, selected, k, peak, top):
        super().__init__(data, selected, k, peak, top)

    def processData(self):
        print(self.getSettings().getK())
        print('Table')
