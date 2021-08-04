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
# implements processData for multiple alignments
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
                files = [top_kmer_f1, top_kmer_f2]
            else:
                files = [top_kmer_f1]

            for file in files:

                current_file_name = file.iloc[0]["File"]
                current_file_name = current_file_name.split(".")[0]

                input_file_name = ('tmp/' + current_file_name + '.fa')
                output_file_name = ('tmp/' + current_file_name + '.aln')
                kmer_list = file.index.tolist()

                records = []
                for i in range(0, len(file)):
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
                files = [top_kmer_f1, top_kmer_f2]
            else:
                files = [top_kmer_f1]

            for file in files:

                top_kmer_index = file.index.values.tolist()
                peak_kmer = list(filter(lambda s: s if len(re.findall(pattern, s)) > 0 else None, top_kmer_index))

                algnm_list = []
                for kmer in peak_kmer:
                    idx = re.search(pattern, kmer).span()[0]  # index of peak position within k-mer
                    shift = (k - 1) - idx  # for alignment, add '-' several times (=shift)
                    algn = "-" * shift + kmer
                    end_gaps = int(2 * k - 1) - len(algn)  # add end gaps
                    algn = algn + "-" * end_gaps
                    algnm_list.append(algn)

                alignments.append(algnm_list)

        return alignments, file_name1, file_name2
