from src.processing import Processing
from suffix_trees import STree


class SecStructure(Processing):

    def __init__(self, data, selected, k, peak, top, feature, cmd, secStruct_data):
        super().__init__(data, selected, k, peak, top, feature, cmd, secStruct_data)

    def createTemplate(self, alphabet):
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

    def createHeatMapColoring(self):
        k = self.getSettings().getK()

        struct_template1 = self.getStructProfil1()
        struct_template2 = self.getStructProfil2()

        template1 = struct_template1.getTemplate()

        struct_kmer_list1 = self.getStructProfil1().getProfile()
        template1_sTree = STree.STree(template1)

        color_hm1 = {str(i): 0 for i in range(1, len(template1) + 1)}
        color_hm1, not_matched_kmer1 = createColorVector(k, template1_sTree, struct_kmer_list1, color_hm1)

        if not struct_template2 is None:
            template2 = struct_template2.getTemplate()
            struct_kmer_list2 = self.getStructProfil2().getProfile()
            template2_sTree = STree.STree(template2)
            color_hm2 = {str(i): 0 for i in range(1, len(template2) + 1)}
            color_hm2, not_matched_kmer2 = createColorVector(k, template2_sTree, struct_kmer_list2, color_hm2)
        else:
            color_hm2 = None

        return color_hm1, color_hm2


def createColorVector(k, tree, kmer_list, color_hm):
    not_matched_kmer = []

    for kmer in kmer_list:
        idx = tree.find(kmer)
        if idx >= 0:
            for i in range(0, k):
                color_hm[str(idx + i + 1)] += kmer_list[kmer]
        else:
            not_matched_kmer.append(kmer)
    max_key = max(color_hm, key=lambda key: color_hm[key])
    max_val = color_hm[max_key]
    color_hm = {x: (y / max_val) * 400 for x, y in color_hm.items()}

    return color_hm, not_matched_kmer


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
