from Bio import SeqIO, AlignIO
from src.processing import Processing
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
import glob
import os
import sys
import subprocess
from distutils.spawn import find_executable


class KMerAlignmentData(Processing):

    def __init__(self, data, selected, k, peak, top):
        super().__init__(data, selected, k, peak, top)

    def processData(self):  # throws FileNotFoundError
        if not os.path.exists('./tmp'):  # directory, where top-kmere-fasta files and alignments will be saved
            os.mkdir('tmp')

        alignment = []

        top_kmer_list = self.getTopKmer()
        top_kmer_index = top_kmer_list.index.drop_duplicates()

        fileNames_list = top_kmer_list['File']

        fileName1_wExt = fileNames_list.drop_duplicates().tolist()[0]  # Filename #1 with extension
        fileName2_wExt = fileNames_list.drop_duplicates().tolist()[1]  # Filename #2 with extension

        newFileName = "{f1}_{f2}".format(f1=os.path.splitext(fileName1_wExt)[0],
                                         f2=os.path.splitext(fileName2_wExt)[0])  # new Filename without extension

        input_file_name = ('tmp/' + newFileName + '.fa')

        output_file_name = ('tmp/' + newFileName + '.aln')

        records = []
        for i in range(0, len(top_kmer_index)):
            records.append(SeqRecord(Seq(top_kmer_index[i]), id=str(i), description=fileNames_list[i]))
        if not os.path.exists(input_file_name):
            SeqIO.write(records, input_file_name,
                        'fasta')  # creates fasta-file from top-kmere list for alignment process
        else:
            print('Top-k-Mere File {i} already exists. Alignment will be done for existing file'.format(
                i=input_file_name))
            print()

        clustalw = find_executable('clustalw')
        if clustalw is not None:
            infile = "-INFILE={i}".format(i=input_file_name)
            outfile = '-OUTFILE={f}'.format(f=output_file_name)
            subprocess.run([clustalw, infile, outfile],
                           stdout=subprocess.DEVNULL)  # executes clustalw multiple alignment

            dnd_files = glob.glob('tmp/*.dnd')  # deletes guide tree file
            os.remove(dnd_files[0])
            alignment = AlignIO.read(output_file_name, "clustal")  # reads multiple alignment file
        else:
            if sys.platform == 'linux' or sys.platform == 'linux2':
                raise FileNotFoundError(
                    'Please install ClustalW with: \'sudo apt install clustalw\'' +
                    '\nFor more information, see: http://www.clustal.org/clustal2/ ')
            else:
                raise FileNotFoundError(
                    'Please install ClustalW. For more information, see: http://www.clustal.org/clustal2/')

        return alignment