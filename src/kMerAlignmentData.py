from Bio import SeqIO, AlignIO
from src.processing import Processing
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
import os
import sys
import subprocess
from distutils.spawn import find_executable
import re


# inherits from process
class KMerAlignmentData(Processing):

    def __init__(self, data, selected, k, peak, top, feature, cmd, sec_struct_data, no_sec_peak):
        super().__init__(data, selected, k, peak, top, feature, cmd, sec_struct_data, no_sec_peak)

    # calculates multiple alignments for both files via clustalw
    def processData(self):  # throws FileNotFoundError
        peak = self.getSettings().getPeak()
        top_kmer_list = self.getTopKmer()
        profile2 = self.getProfileObj2()

        file_name1 = os.path.basename(self.getProfileObj1().getName())
        top_kmer_f1 = top_kmer_list.query("File==@file_name1")
        top_kmer_f1.sort_values(by="Frequency", ascending=False)

        if profile2 is not None:
            file_name2 = os.path.basename(self.getProfileObj2().getName())
            top_kmer_f2 = top_kmer_list.query("File==@file_name2")
            top_kmer_f2.sort_values(by="Frequency", ascending=False)
        else:
            file_name2 = None
            top_kmer_f2 = None

        alignments = []

        if peak is None:
            if not os.path.exists('./tmp'):  # directory, where top-kmer-fasta files and alignments will be saved
                # directory will be deleted after program exit
                os.mkdir('tmp')

            if profile2 is not None:
                # list of separated top k-mer lists
                sep_top_kmer_df = [top_kmer_f1, top_kmer_f2]
            else:
                sep_top_kmer_df = [top_kmer_f1]

            for sep_top_kmer_df in sep_top_kmer_df:

                current_file_name = sep_top_kmer_df.iloc[0]["File"]
                current_file_name = current_file_name.split(".")[0]

                input_file_name = ('tmp/' + current_file_name + '.fa')
                output_file_name = ('tmp/' + current_file_name + '.aln')
                kmer_list = sep_top_kmer_df.index.tolist()

                records = []
                for i in range(0, len(sep_top_kmer_df)):
                    records.append(SeqRecord(Seq(kmer_list[i]), id=str(i), description=current_file_name))

                SeqIO.write(records, input_file_name,
                            'fasta')  # creates fasta-file from top-kmer list for alignment process

                clustalw = find_executable('clustalw')
                if clustalw is not None:
                    infile = "-INFILE={}".format(input_file_name)
                    outfile = '-OUTFILE={}'.format(output_file_name)
                    # executes clustalw multiple alignment
                    subprocess.run([clustalw, infile, outfile],
                                   stdout=subprocess.DEVNULL)
                    alignments.append(AlignIO.read(output_file_name, "clustal"))  # reads multiple alignment file

                else:
                    if sys.platform == 'linux' or sys.platform == 'linux2':
                        raise FileNotFoundError(
                            'ERROR: ClustalW not found.' +
                            '\nPlease install ClustalW with: \'sudo apt install clustalw\'' +
                            '\nFor more information, see: http://www.clustal.org/clustal2/ ')
                    else:
                        raise FileNotFoundError(
                            'ERROR: ClustalW not found.' +
                            '\nPlease install ClustalW. For more information, see: http://www.clustal.org/clustal2/')

        else:  # if peak position is given, then alignment takes place at position 'peak'
            k = self.getSettings().getK()
            pattern = '[A-Z]'

            if profile2 is not None:
                sep_top_kmer_df = [top_kmer_f1, top_kmer_f2]
            else:
                sep_top_kmer_df = [top_kmer_f1]

            for top_df in sep_top_kmer_df:

                top_kmer_index = top_df.index.tolist()
                peak_kmer = list(filter(lambda s: s if len(re.findall(pattern, s)) == 1 else None, top_kmer_index))

                if None in peak_kmer:
                    peak_kmer.remove(None)

                algnm_list = []
                for kmer in peak_kmer:
                    idx = re.search(pattern, kmer).span()[0]  # index of peak position within k-mer
                    # Assume k-mer character are rotated until peak-position is at the end.
                    # Shift is the number of dashes and equal to number of character before peak-position.
                    # It is calculated through the difference between k-Mer length and peak-position.
                    shift = (k - 1) - idx
                    algn = "-" * shift + kmer
                    # Assume string length for alignment is two times k.
                    # For number of end dashes calculate the difference between total length and length of algn
                    end_gaps = int(2 * k - 1) - len(algn)  # add end gaps
                    algn = algn + "-" * end_gaps
                    algnm_list.append(algn)

                alignments.append(algnm_list)

        return alignments, file_name1, file_name2
