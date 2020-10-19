from setting import *
from fileCountException import *


# abstract class
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

    # abstract method
    def processData(self):
        pass

    def getProfiles(self):
        return self.profile1, self.profile2

    def getSettings(self):
        return self.setting
