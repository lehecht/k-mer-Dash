from src.processing import Processing
from Bio import pairwise2
import re


class KMerAlignmentData(Processing):

    def __init__(self, data, selected, k, peak, top, highlight):
        super().__init__(data, selected, k, peak, top, highlight)

    def processData(self):
        k = self.getSettings().getK()
        top_kmer_list = self.getTopKmer().index.drop_duplicates().tolist()
        peak = self.getSettings().getPeak()

        alignment = []

        if peak is None:
            top_kmer_list.sort()

            seq_model = top_kmer_list[0]  # all pairs contains of the seq_model and another top-sequence

            alignment.append(seq_model)

            for seq in top_kmer_list[1:]:
                algnm = pairwise2.align.globalxx(seq_model, seq, one_alignment_only=True)[0][1]
                alignment.append(algnm)
            print('Alignment of Top-kmere created with BioPythons Pairwise2-Module')

        else:
            pattern = '[A-Z]+[a-z]+$'
            peak_kmeres = list(filter(lambda s: re.search(pattern, s),
                                      top_kmer_list))  # filters only kmeres, which include the peak position
            peak_kmeres.sort()
            for kmer in peak_kmeres:
                idx = re.search('[A-T]', kmer).span()[0]  # index of peak position within kmer
                shift = (k - 1) - idx  # for alignment, add '-' several times (=shift)
                alignment.append("-" * shift + kmer)
            print('Alignment of Top-kmere created with Peak-Position: {}'.format(peak))

        return alignment
