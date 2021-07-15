from src.processing import Processing
from suffix_trees import STree
import math


class SecStructure(Processing):

    def __init__(self, data, selected, k, peak, top, feature, cmd, sec_struct_data, no_sec_peak):
        super().__init__(data, selected, k, peak, top, feature, cmd, sec_struct_data, no_sec_peak)

    # generate element-string template and dotbracket-string
    def processData(self):
        k = 3

        alphabet1 = self.getStructProfile1().getAlphabet()

        # alphabets of structural data
        alphabets = [alphabet1]

        sec_profile_obj2 = self.getStructProfile2()

        if sec_profile_obj2 is not None:
            alphabet2 = sec_profile_obj2.getAlphabet()
            alphabets.append(alphabet2)

        results = []

        for alphabet in alphabets:
            hairpin = bool("H" in alphabet)
            multiloop = bool("M" in alphabet)
            bulge = bool("B" in alphabet)
            internalloop = bool("I" in alphabet)

            # if element is in alphabet, add to template
            template = list()
            template.append(k * "E")
            l0 = len(template)

            dotbracket_string = list()

            # translate change in template to dotbracket string
            dotbracket_string.extend(element2dotbracket(template, k, 0, l0, True))

            l1 = len(template)

            # add internal-loops and bulges if needed
            template = helpAddIBloop(k, template, internalloop, bulge, True)

            # add hairpin if needed
            if "H" in alphabet:
                hp = [k * "S", k * "H"]
                template.extend(hp)
            else:
                template.append(k * "S")

            # translate change in template to dotbracket string
            l2 = len(template) - 1
            dotbracket_string.extend(element2dotbracket(template, k, l1, l2, True))

            template = helpAddIBloop(k, template, internalloop, bulge, False)

            # add multiloop and second hairpin if needed
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

            # convert into strings
            template = ''.join(template)
            dotbracket_string = ''.join(dotbracket_string)

            results.append([template, dotbracket_string])

        return results

    # calculates color-vector, color-vector maximum and list of not matched k-mers
    # template1: element-string template of first structural file
    # template2: element-string template of second structural file
    # no_sec_peak: status (-1= no data,0= False,1= True) to use 2-mer from structural data with peak-position only
    def createHeatMapColoring(self, template1, template2, no_sec_peak):
        k = 2

        # get list with k-mere and their frequency
        struct_profile1 = self.getStructProfile1().getProfile()
        struct_kmer_list = [struct_profile1]

        template = [template1]

        struct_profile_obj2 = self.getStructProfile2()
        if struct_profile_obj2 is not None:
            struct_profile2 = struct_profile_obj2.getProfile()
            struct_kmer_list.append(struct_profile2)
            template.append(template2)

        norm_vector = self.getNormVector()

        result = []

        for i in range(0, len(struct_kmer_list)):
            current_template = template[i]
            current_profil = struct_kmer_list[i]

            # create suffix-tree to find k-mer position in template
            template1_s_tree = STree.STree(current_template)

            color_hm1 = {str(i): 0 for i in range(1, len(current_template) + 1)}
            color_hm1, not_matched_kmer1, color_domain_max1 = createColorVector(k, template1_s_tree, current_profil,
                                                                                color_hm1, no_sec_peak, norm_vector)

            result.append([color_hm1, color_domain_max1, not_matched_kmer1])

        return result


# calculates values for color-vector
# k: k-mer length
# tree: template suffix-tree
# kmer_list: list of kmere with their frequency
# color_hm: empty dict
# no_sec_peak: status (-1= no data,0= False,1= True) to use 2-mer from structural data with peak-position only
# norm_vector: normalization vector containing rates of 2-mere
def createColorVector(k, tree, kmer_list, color_hm, no_sec_peak, norm_vector):
    not_matched_kmer = []

    for kmer in kmer_list.keys():
        # find index of kmer in template
        indices_list = tree.find_all(kmer.upper())
        if norm_vector is None:
            norm = 1
        else:
            norm = norm_vector[kmer.upper()]
            if norm == 0:
                norm = 1
        # if k-mer was found in template
        for idx in indices_list:
            if idx >= 0:
                # use only peak-position in 2-mer for visualization
                if no_sec_peak == 0:
                    idx = [idx + i for i in range(0, len(kmer)) if kmer[i].isupper()][0]
                    color_hm[str(idx + 1)] += (kmer_list[kmer] / norm)
                else:
                    for i in range(0, k):
                        color_hm[str(idx + i + 1)] += (kmer_list[kmer] / norm)
            else:
                not_matched_kmer.append(kmer)

    # scale values in color-vector
    color_hm = {x: round(math.log(y,2)) if y > 0 else y for x, y in color_hm.items()}
    color_domain_max = max(color_hm.values())

    return color_hm, not_matched_kmer, color_domain_max


# adds internal-loops and bulges to template
# k: k-mer length
# template: list of element-strings
# internal_loop: bool (True if element in alphabet, otherwise False)
# bulge: bool (True if element in alphabet, otherwise False)
# forward: structure orientation (True: ahead of hairpin, False: after hairpin)
def helpAddIBloop(k, template, internal_loop, bulge, forward):
    if forward:
        if internal_loop:
            il = [k * "S", k * "I"]
            template.extend(il)
        if bulge:
            b = [k * "S", k * "B"]
            template.extend(b)
    else:
        if bulge:
            s = k * "S"
            template.append(s)
        if internal_loop:
            il = [k * "S", k * "I"]
            template.extend(il)
    return template


# translates template in dotbracket notation
# template: list of element-strings
# k: length of k-mer
# start_index: position where translation should start
# end_index: position where translations ends
# open_bracket: bracket-orientation (True: open brackets, False: close brackets)
def element2dotbracket(template, k, start_index, end_index, open_bracket):
    # template example: ['EEE','SSS','HHH','SSS','EEE']

    db_sublist = template[start_index: end_index + 1]

    if open_bracket:
        db_sublist = [k * "." if e in [k * "E", k * "I", k * "M", k * "B", k * "H"] else k * "(" for e in db_sublist]
    else:
        db_sublist = [k * "." if e in [k * "E", k * "I", k * "M", k * "H"] else k * ")" for e in db_sublist]

    return db_sublist
