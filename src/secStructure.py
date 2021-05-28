from src.processing import Processing
from itertools import product, filterfalse


class SecStructure(Processing):

    def __init__(self, data, selected, k, peak, top, feature, cmd, secStruct_data):
        super().__init__(data, selected, k, peak, top, feature, cmd, secStruct_data)

    def createTemplate(self):
        k = self.getSettings().getK()
        alphabet = self.getStructAlphabet()

        hairpin = bool(lambda: True if "H" in alphabet else False)
        multiloop = bool(lambda: True if "M" in alphabet else False)
        bulge = bool(lambda: True if "B" in alphabet else False)
        internalloop = bool(lambda: True if "I" in alphabet else False)

        template = list()
        template.append(k * "E")

        if multiloop:
            hp = k * "S" + k * "H"
            template.append(hp)
            template = helpAddIBloop(k, template, internalloop, bulge)
            template.append(k * "S" + k * "M")
            template = helpAddIBloop(k, template, internalloop, bulge)
            template.append(hp)

        else:
            if hairpin:
                hp = k * "S" + k * "H"
                template.append(hp)
                template = helpAddIBloop(k, template, internalloop, bulge)
                template = helpAddIBloop(k, template, internalloop, False)
                template.append(hp)
            else:
                template = helpAddIBloop(k, template, internalloop, bulge)

        template.append(k*"S"+k*"E")

        template = ''.join(template)

        print(hairpin)
        print(multiloop)
        print(internalloop)
        print(bulge)
        print(template)

        # kmer_list = [k * c for c in alphabet]

        # kmer_combinations = list(combinations(kmer_list, r=2))
        # kmer_combinations = list(product(kmer_list, repeat=2))
        # kmer_combinations = list(filterfalse(lambda x: len(set(x)) == 1, kmer_combinations))
        # kmer_combinations = list(filterfalse(lambda x: k * "H" in x and not k * "S" in x, kmer_combinations))

        # print(kmer_combinations)
        #
        # kmer_comb_len = len(kmer_combinations)

        # template = ["" if 0 < i < kmer_comb_len - 2 else k * "E" for i in range(0, kmer_comb_len)]
        #
        # for cb in kmer_combinations:
        #     stem = k * "S"
        #     if stem in cb:
        #         pass
        #     else:
        #         pass


def helpAddIBloop(k, template, internalloop, bulge):
    if internalloop:
        il = k * "S" + k * "I"
        template.append(il)
    if bulge:
        b = k * "S" + k * "B"
        template.append(b)
    return template
