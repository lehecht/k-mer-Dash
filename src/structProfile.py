from src.profile import Profile


class StructProfile(Profile):
    template_string = None  # element-string
    dotbracket_string = None  # template in dotbracket notation
    alphabet = None  # alphabet of used elements

    def __init__(self, profile, name, alpha):
        super().__init__(profile, name)
        self.alphabet = alpha

    def setTemplate(self, template):
        self.template_string = template

    def setDotbracket(self, db):
        self.dotbracket_string = db

    def setAlphabet(self, a):
        self.alphabet = a

    def getTemplate(self):
        return self.template_string

    def getDotbracket(self):
        return self.dotbracket_string

    def getAlphabet(self):
        return self.alphabet
