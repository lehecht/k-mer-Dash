import re

from src.processing import Processing
from suffix_trees import STree
import math


class SecStructure(Processing):

    def __init__(self, data, selected, k, peak, top, feature, cmd, secStruct_data):
        super().__init__(data, selected, k, peak, top, feature, cmd, secStruct_data)

    def createTemplate(self, alphabet):
        k = 3

        hairpin = bool("H" in alphabet)
        multiloop = bool("M" in alphabet)
        bulge = bool("B" in alphabet)
        internalloop = bool("I" in alphabet)

        template2dotstring = list()
        dotstring2template = list()

        result = list()
        result.append(k * "E")

        result_dotbracket_string = list()
        result_dotbracket_string.extend(element2dotbracket(result, k, 0, k, True))

        template, dotbracket_string = createIntermediateTemplate(k, hairpin, multiloop,
                                                                 internalloop, bulge)

        result.extend(template)
        result_dotbracket_string.extend(dotbracket_string)

        l3 = len(result)
        result.append(k * "S")
        result_dotbracket_string.extend(element2dotbracket(result, k, l3, len(result) - 1, False))

        l4 = len(result)
        result.append(k * "E")
        result_dotbracket_string.extend(element2dotbracket(result, k, l4, len(result) - 1, False))

        result = ''.join(result)
        result_dotbracket_string = ''.join(result_dotbracket_string)

        return result, result_dotbracket_string

    def createHeatMapColoring(self, template1, struct_kmer_list1,no_sec_peak, not_matched=None,):

        if not_matched is None:
            not_matched = []
        k = 2

        if len(not_matched) > 0:
            struct_kmer_list1 = {kmer: struct_kmer_list1[kmer] for kmer in not_matched}

        template1_sTree = STree.STree(template1)

        color_hm1 = {str(i): 0 for i in range(1, len(template1) + 1)}
        color_hm1, not_matched_kmer1, color_domain_max1 = createColorVector(k, template1_sTree, struct_kmer_list1,
                                                                            color_hm1,no_sec_peak)
        return color_hm1, color_domain_max1, not_matched_kmer1


def createColorVector(k, tree, kmer_list, color_hm,no_sec_peak):
    not_matched_kmer = []

    for kmer in kmer_list:
        idx = tree.find(kmer.upper())
        if idx >= 0:
            if no_sec_peak == 0:
                for match in re.finditer('[A-Z]', kmer):
                    if match.group() == 1:
                        idx += 1
                color_hm[str(idx + 1)] += kmer_list[kmer]
            else:
                for i in range(0, k):
                    color_hm[str(idx + i + 1)] += kmer_list[kmer]
        else:
            not_matched_kmer.append(kmer)

    # print(color_hm)
    color_hm = {x: round(math.log(y, 2)) if y > 0 else y for x, y in color_hm.items()}
    max_val = max(color_hm.values())
    # print(color_hm, max_val)
    color_domain_max = round(max_val, -1)

    return color_hm, not_matched_kmer, color_domain_max


def createIntermediateTemplate(i, hairpin, multiloop, internalloop, bulge):
    template = []
    dotbracket_string = []

    template = helpAddIBloop(i, template, internalloop, bulge, True)

    hp = [i * "S", i * "H"]
    template.extend(hp)

    l1 = len(template) - 1
    dotbracket_string.extend(element2dotbracket(template, i, 0, l1, True))

    template = helpAddIBloop(i, template, internalloop, bulge, False)

    if multiloop and hairpin and i > 1:
        template.extend([i * "S", i * "M"])

        l2 = len(template) - 1
        dotbracket_string.extend(element2dotbracket(template, i, l1 + 1, l2, False))

        hp = [i * "S", i * "H"]
        template.extend(hp)

        l3 = len(template) - 1
        dotbracket_string.extend(element2dotbracket(template, i, l2 + 1, l3, True))

    else:
        l2 = len(template) - 1
        dotbracket_string.extend(element2dotbracket(template, i, l1 + 1, l2, False))

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


def element2dotbracket(template, k, i, j, open_bracket):
    db_sublist = template[i: j + 1]

    if open_bracket:
        db_sublist = [k * "." if e in [k * "E", k * "I", k * "M", k * "B", k * "H"] else k * "(" for e in db_sublist]
    else:
        db_sublist = [k * "." if e in [k * "E", k * "I", k * "M", k * "H"] else k * ")" for e in db_sublist]

    return db_sublist
