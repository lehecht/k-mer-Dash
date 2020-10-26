class Profile:
    profile = None
    file_name = None

    def __init__(self, profile, name):
        self.profile = profile
        self.file_name = name

    def setProfile(self, profile):
        self.profile = profile

    def setName(self, name):
        self.file_name = name

    def getProfile(self):
        return self.profile

    def getName(self):
        return self.file_name
