from src.processing import Processing


class SecStructure(Processing):

    def __init__(self, data, selected, k, peak, top, feature, cmd, secStruct_data):
        super().__init__(data, selected, k, peak, top, feature, cmd, secStruct_data)

    def createTemplate(self,alphabet):
        k = self.getSettings().getK()

        hairpin = bool("H" in alphabet)
        multiloop = bool("M" in alphabet)
        bulge = bool("B" in alphabet)
        internalloop = bool("I" in alphabet)

        template = list()
        template.append(k * "E")

        dotbracket_string = list()

        template = helpAddIBloop(k, template, internalloop, bulge, True)

        if hairpin:
            hp = [k * "S", k * "H"]
            template.extend(hp)
        else:
            template.append(k * "S")

        l1 = len(template) - 1
        dotbracket_string.extend(element2dotbracket(template, k, 0, l1, True))

        template = helpAddIBloop(k, template, internalloop, bulge, False)

        if multiloop and hairpin:
            template.extend([k * "S", k * "M"])

            l2 = len(template) - 1
            dotbracket_string.extend(element2dotbracket(template, k, l1 + 1, l2, False))

            hp = [k * "S", k * "H"]
            template.extend(hp)

            l3 = len(template) - 1
            dotbracket_string.extend(element2dotbracket(template, k, l2 + 1, l3, True))
        else:
            l2 = len(template) - 1
            dotbracket_string.extend(element2dotbracket(template, k, l1 + 1, l2, False))

        template.extend([k * "S", k * "E"])

        l3 = len(template) - 2
        dotbracket_string.extend(element2dotbracket(template, k, l3, len(template) - 1, False))

        template = ''.join(template)
        dotbracket_string = ''.join(dotbracket_string)

        return template, dotbracket_string


def helpAddIBloop(k, template, internalloop, bulge, lead):
    if lead:
        if internalloop:
            il = [k * "S", k * "I"]
            template.extend(il)
        if bulge:
            b = [k * "S", k * "B"]
            template.extend(b)
    else:
        if bulge:
            s = k * "S"
            template.append(s)
        if internalloop:
            il = [k * "S", k * "I"]
            template.extend(il)
    return template


def element2dotbracket(template, k, i, j, lead):
    db_sublist = template[i: j + 1]

    if lead:
        db_sublist = [k * "." if e in [k * "E", k * "I", k * "M", k * "B", k * "H"] else k * "(" for e in db_sublist]
    else:
        db_sublist = [k * "." if e in [k * "E", k * "I", k * "M", k * "H"] else k * ")" for e in db_sublist]

    return db_sublist
