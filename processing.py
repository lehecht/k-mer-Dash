from setting import *
from fileCountException import *


class Processing:
    profile1 = None
    profile2 = None
    setting = None

    def __init__(self, data, selected, k, peak, top):
        if selected is not None:
            self.setting = Setting(data, selected, k, peak, top)
        elif len(data) >= 2:
            selected_from_data = data[:2]
            self.setting = Setting(data, selected_from_data, k, peak, top)
        else:
            raise FileCountException

    def createProfile(self):
        pass

    def createMultAlignment(self):
        pass

    def processData4PCA(self):
        pass
