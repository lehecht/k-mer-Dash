import re

from src.processing import Processing
from suffix_trees import STree
import math


class SecStructure(Processing):

    def __init__(self, data, selected, k, peak, top, feature, cmd, secStruct_data, no_sec_peak):
        super().__init__(data, selected, k, peak, top, feature, cmd, secStruct_data, no_sec_peak)

    def processData(self):
        k = 3

        alphabet1 = self.getStructProfil1().getAlphabet()

        alphabets = [alphabet1]

        secProfileObj2 = self.getStructProfil2()

        if not secProfileObj2 is None:
            alphabet2 = secProfileObj2.getAlphabet()
            alphabets.append(alphabet2)

        results = []

        for alphabet in alphabets:
            hairpin = bool("H" in alphabet)
            multiloop = bool("M" in alphabet)
            bulge = bool("B" in alphabet)
            internalloop = bool("I" in alphabet)

            template = list()
            template.append(k * "E")
            l0 = len(template)

            dotbracket_string = list()

            dotbracket_string.extend(element2dotbracket(template, k, 0, l0, True))

            l1 = len(template)
            template = helpAddIBloop(k, template, internalloop, bulge, True)

            if "H" in alphabet:
                hp = [k * "S", k * "H"]
                template.extend(hp)
            else:
                template.append(k * "S")

            l2 = len(template) - 1
            dotbracket_string.extend(element2dotbracket(template, k, l1, l2, True))

            template = helpAddIBloop(k, template, internalloop, bulge, False)

            if multiloop and hairpin:
                template.extend([k * "S", k * "M"])

                l3 = len(template) - 1
                dotbracket_string.extend(element2dotbracket(template, k, l2 + 1, l3, False))

                hp = [k * "S", k * "H"]
                template.extend(hp)

                l4 = len(template) - 1
                dotbracket_string.extend(element2dotbracket(template, k, l3 + 1, l4, True))

            else:
                l3 = len(template) - 1
                dotbracket_string.extend(element2dotbracket(template, k, l2 + 1, l3, False))

            l4 = len(template)
            template.append(k * "S")
            dotbracket_string.extend(element2dotbracket(template, k, l4, len(template) - 1, False))

            l5 = len(template)
            template.append(k * "E")
            dotbracket_string.extend(element2dotbracket(template, k, l5, len(template) - 1, False))

            template = ''.join(template)
            dotbracket_string = ''.join(dotbracket_string)

            results.append([template, dotbracket_string])

        return results

    def createHeatMapColoring(self, template1, template2, no_sec_peak):
        k = 2

        structProfile1 = self.getStructProfil1().getProfile()
        struct_kmer_list = [structProfile1]

        template = [template1]

        structProfileObj2 = self.getStructProfil2()
        if not structProfileObj2 is None:
            structProfile2 = structProfileObj2.getProfile()
            struct_kmer_list.append(structProfile2)
            template.append(template2)

        norm_vector = self.getNormVector()

        result = []

        for i in range(0, len(struct_kmer_list)):
            current_template = template[i]
            current_profil = struct_kmer_list[i]

            template1_sTree = STree.STree(current_template)

            color_hm1 = {str(i): 0 for i in range(1, len(current_template) + 1)}
            color_hm1, not_matched_kmer1, color_domain_max1 = createColorVector(k, template1_sTree, current_profil,
                                                                                color_hm1, no_sec_peak, norm_vector)

            result.append([color_hm1, color_domain_max1, not_matched_kmer1])

        return result


def createColorVector(k, tree, kmer_list, color_hm, no_sec_peak, norm_vector):
    not_matched_kmer = []

    for kmer in kmer_list:
        idx = tree.find(kmer.upper())
        if norm_vector is None:
            norm = 1
        else:
            norm = norm_vector[kmer.upper()]
            if norm == 0:
                norm = 1
        if idx >= 0:
            if no_sec_peak == 0:
                for match in re.finditer('[A-Z]', kmer):
                    if match.group() == 1:
                        idx += 1
                color_hm[str(idx + 1)] += (kmer_list[kmer] / norm)
            else:
                for i in range(0, k):
                    color_hm[str(idx + i + 1)] += (kmer_list[kmer] / norm)
        else:
            not_matched_kmer.append(kmer)
    color_hm = {x: round(math.log(y, 2)) if y > 0 else y for x, y in color_hm.items()}
    color_domain_max = max(color_hm.values())

    return color_hm, not_matched_kmer, color_domain_max


# def createIntermediateTemplate(i, hairpin, multiloop, internalloop, bulge):
#     template = []
#     dotbracket_string = []
#
#     template = helpAddIBloop(i, template, internalloop, bulge, True)
#
#     hp = [i * "S", i * "H"]
#     template.extend(hp)
#
#     l1 = len(template) - 1
#     dotbracket_string.extend(element2dotbracket(template, i, 0, l1, True))
#
#     template = helpAddIBloop(i, template, internalloop, bulge, False)
#
#     if multiloop and hairpin and i > 1:
#         template.extend([i * "S", i * "M"])
#
#         l2 = len(template) - 1
#         dotbracket_string.extend(element2dotbracket(template, i, l1 + 1, l2, False))
#
#         hp = [i * "S", i * "H"]
#         template.extend(hp)
#
#         l3 = len(template) - 1
#         dotbracket_string.extend(element2dotbracket(template, i, l2 + 1, l3, True))
#
#     else:
#         l2 = len(template) - 1
#         dotbracket_string.extend(element2dotbracket(template, i, l1 + 1, l2, False))
#
#     return template, dotbracket_string


def helpAddIBloop(k, template, internalloop, bulge, forward):
    if forward:
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


def element2dotbracket(template, k, i, j, open_bracket):
    # template example: ['EEE','SSS','HHH','SSS','EEE']

    db_sublist = template[i: j + 1]

    if open_bracket:
        db_sublist = [k * "." if e in [k * "E", k * "I", k * "M", k * "B", k * "H"] else k * "(" for e in db_sublist]
    else:
        db_sublist = [k * "." if e in [k * "E", k * "I", k * "M", k * "H"] else k * ")" for e in db_sublist]

    return db_sublist
