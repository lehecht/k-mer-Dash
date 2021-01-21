from Bio import SeqIO, AlignIO
from src.processing import Processing
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
import glob
import os
import sys
import subprocess
from distutils.spawn import find_executable
import re


class KMerAlignmentData(Processing):

    def __init__(self, data, selected, k, peak, top, feature):
        super().__init__(data, selected, k, peak, top, feature)

    def processData(self):  # throws FileNotFoundError
        peak = self.getSettings().getPeak()
        topKmer_List = self.getTopKmer()
        fileName1 = os.path.basename(self.getProfilObj1().getName())
        fileName2 = os.path.basename(self.getProfilObj2().getName())

        topKmer_f1 = topKmer_List.query("File==@fileName1")
        topKmer_f2 = topKmer_List.query("File==@fileName2")

        topKmer_f1.sort_values(by="Frequency", ascending=False)
        topKmer_f2.sort_values(by="Frequency", ascending=False)

        alignments = []

        if peak is None:
            if not os.path.exists('./tmp'):  # directory, where top-kmere-fasta files and alignments will be saved
                os.mkdir('tmp')

            for file in [topKmer_f1, topKmer_f2]:

                current_fileName = file.iloc[0]["File"]
                current_fileName = current_fileName.split(".")[0]

                input_file_name = ('tmp/' + current_fileName + '.fa')
                output_file_name = ('tmp/' + current_fileName + '.aln')
                kmer_list = file.index.tolist()

                records = []
                for i in range(0, len(file)):
                    records.append(SeqRecord(Seq(kmer_list[i]), id=str(i), description=current_fileName))

                SeqIO.write(records, input_file_name,
                            'fasta')  # creates fasta-file from top-kmere list for alignment process

                clustalw = find_executable('clustalw')
                if clustalw is not None:
                    infile = "-INFILE={i}".format(i=input_file_name)
                    outfile = '-OUTFILE={f}'.format(f=output_file_name)
                    subprocess.run([clustalw, infile, outfile],
                                   stdout=subprocess.DEVNULL)  # executes clustalw multiple alignment
                    alignments.append(AlignIO.read(output_file_name, "clustal"))  # reads multiple alignment file

                else:
                    if sys.platform == 'linux' or sys.platform == 'linux2':
                        raise FileNotFoundError(
                            'Please install ClustalW with: \'sudo apt install clustalw\'' +
                            '\nFor more information, see: http://www.clustal.org/clustal2/ ')
                    else:
                        raise FileNotFoundError(
                            'Please install ClustalW. For more information, see: http://www.clustal.org/clustal2/')

        else:  # if peak position is given, then alignment takes place at position 'peak'
            k = self.getSettings().getK()
            pattern = '[A-Z]'
            for file in [topKmer_f1, topKmer_f2]:

                top_kmer_index = file.index.values.tolist()
                peak_kmeres = list(filter(lambda s: s if len(re.findall(pattern, s)) > 0 else None, top_kmer_index))

                algnmList = []
                for kmer in peak_kmeres:
                    idx = re.search('[A-T]', kmer).span()[0]  # index of peak position within kmer
                    shift = (k - 1) - idx  # for alignment, add '-' several times (=shift)
                    algn = "-" * shift + kmer
                    endGaps = int(2 * k - 1) - len(algn)  # add end gaps
                    algn = algn + "-" * endGaps
                    algnmList.append(algn)

                alignments.append(algnmList)

        return alignments, fileName1, fileName2
