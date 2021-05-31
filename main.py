import argparse
import os
import subprocess
import sys
from pathlib import Path
from Bio import SeqIO

from src.console_output import printData
from src.dashView import dashLayout
from src.inputValueException import InputValueException
from src.fileCountException import FileCountException


def checkValue(value):
    if not value.isdigit():
        raise argparse.ArgumentTypeError("Invalid Value: Value must be integer.")
    elif int(value) <= 0:
        raise argparse.ArgumentTypeError("Invalid Value: Must be greater than 0.")
    return int(value)


argparser = argparse.ArgumentParser()
argparser.add_argument('-fs', '--files', dest='fs', type=argparse.FileType('r'), nargs='+',
                       help="List of space-separated nucleotide Fasta-files. "
                            "Allowed file extensions are \'.fa, .fasta, .fna, .fsa, .ffn\'")
argparser.add_argument('-d', '--directory', dest='d', action='store',
                       help="Directory with nucleotide Fasta-Files. Allowed file extensions are "
                            "\'.fa, .fasta, .fna, .fsa, .ffn\'")
argparser.add_argument('-f', '--file', dest='f', action='store', type=argparse.FileType('r'),
                       help="Single nucleotide Fasta-File for commandline-mode. "
                            "Allowed file extensions are \'.fa, .fasta, .fna, .fsa, .ffn\'")
argparser.add_argument('-sfs', '--files_struct', dest='sfs', type=argparse.FileType('r'), nargs='+',
                       help="List of space-separated Fasta-files for secondary structure. "
                            "Allowed file extensions are \'.fa, .fasta, .fsa\'")
argparser.add_argument('-sd', '--directory_struct', dest='sd', action='store',
                       help="Directory with Fasta-Files for secondary structure. Allowed file extensions are "
                            "\'.fa, .fasta, .fsa\'")
argparser.add_argument('-sf', '--file_struct', dest='sf', action='store', type=argparse.FileType('r'),
                       help="Single nucleotide Fasta-File for commandline-mode. "
                            "Allowed file extensions are \'.fa, .fasta, .fsa\'")
argparser.add_argument('-k', dest='k', action='store', type=checkValue,
                       help="Length of k-Mer. Must be smaller than sequence length. Required in commandline-mode only.")
argparser.add_argument('-p', '--peak', dest='peak', action='store', type=checkValue,
                       help="(optional) Peak position in sequence. Must be smaller or equal than given sequence length."
                            + " Required in commandline-mode only.")
argparser.add_argument('-t', '--top', dest='top', default=10, action='store', type=checkValue,
                       help="(optional) Number of displayed top kmers (Default: 10). Required in commandline-mode only.")
argparser.add_argument('-c', '--console', dest='console', default=False, action='store', type=bool,
                       help="Starts program with GUI (= False (Default)) or on commandline (= True).")
argparser.add_argument('-pt', '--port', dest='port', default=8088, action='store', type=int,
                       help="(optional) Port on which dash app runs")


def checkSecFileFormat(file):
    record = str(list(SeqIO.parse(file, "fasta"))[0].seq)

    if 'A' in record or 'T' in record or 'C' in record or 'G' in record:
        print(file, record)
        raise InputValueException("ERROR: Fasta files for secondary structure must only contain element-strings.")


def checkFileExtension(file, struct):
    ext = os.path.splitext(file)[1]
    if struct:
        ext_list = [".fa", ".fasta", ".fsa"]
    else:
        ext_list = [".fa", ".fasta", ".fna", ".fsa", ".ffn"]

    if ext not in ext_list:
        if struct:
            msg = "ERROR: only Fasta-files with file-extension: \'.fa\', \'.fasta\', \'.fsa\' allowed!"
        else:
            msg = "ERROR: only Fasta-files with file-extension: " \
                  "\'.fa\', \'.fasta\', \'.fna\', \'.fsa\', \'.ffn\' allowed!"

        raise InputValueException(msg)

    if os.stat(file).st_size is 0:
        raise FileCountException('ERROR: file(s) is empty.')


def checkArguments(file_list, f, c, k, fasta_dir, fs_list, sfs, sd, sf):
    if not sfs is None:
        struct_file_list = sfs
    else:
        struct_file_list = sd

    if c and (k is None):
        raise InputValueException("ERROR: k is required in commandline-mode.")
    if len(file_list) > 0 and (not f is None):
        raise InputValueException("ERROR: please choose either -fs or -d for interactive mode "
                                  "or -f for command-line mode.")
    elif len(file_list) > len(set(file_list)):
        raise InputValueException("ERROR: every nucleotide FASTA-file must be unique.")
    elif not struct_file_list is None and len(struct_file_list) > len(set(struct_file_list)):
        raise InputValueException("ERROR: every structural FASTA-file must be unique.")
    elif (not f is None or len(file_list) < 2) and not c:
        raise InputValueException("ERROR: interactive mode needs at least two files.")
    elif len(file_list) > 0 and c:
        raise InputValueException("ERROR: commandline-mode requires only single Fasta-file. Please use -f option.")
    elif (not fasta_dir is None) and (not fs_list is None):
        raise InputValueException("ERROR: please choose either -fs to commit a list of files or -d for a directory.")
    elif not [sfs, sd, sf].count(None) > 1:
        raise InputValueException("ERROR: please choose either -sfs, -sd or -sf to commit structural data.")


def selectAllFastaFiles(dir, struct):
    file_list = []
    if struct:
        ext_list = [".fa", ".fasta", ".fsa"]
    else:
        ext_list = [".fa", ".fasta", ".fna", ".fsa", ".ffn"]

    for ext in ext_list:
        file_list.extend(Path(dir).glob('*{}'.format(ext)))

    if len(file_list) == 0:
        if struct:
            msg = 'ERROR: {} has no Fasta-files with extension: .fa, .fasta, .fsa'.format(dir)
        else:
            msg = 'ERROR: {} has no Fasta-files with extension: .fa, .fasta, .fna, .fsa, .ffn'.format(dir)

        raise FileCountException(msg)

    for f in file_list:
        if os.stat(f).st_size is 0:
            raise FileCountException(
                'ERROR: there must be no empty Fasta-file in \'{}\'.'.format(dir))
    return file_list


def checkTargetLengths(fileList):
    f = open(fileList[0])
    target = f.readline()
    target = f.readline()  # read only first sequence
    targetLen = len(target)
    for file in fileList[1:]:
        f = open(file)
        target = f.readline()
        target = f.readline()  # read only first sequence
        if not targetLen == len(target):
            raise ValueError("ERROR: sequence-length must be equal in all files.")
    f.close()


if __name__ == '__main__':
    # exit = False
    args = argparser.parse_args()

    # ------------------------------------------ save files ------------------------------------------------------------

    struct_sfs_list = None
    struct_sd_list = None
    struct_sf_list = None
    struct_list = None

    if not args.fs is None:  # if file-list option is used
        file_list = [f.name for f in args.fs]
        try:
            checkTargetLengths(file_list)  # check if all files own sequences with equal lengths
            for f in file_list:
                checkFileExtension(f, False)  # check file extension
        except ValueError as ve:
            print(ve.args[0])
            sys.exit(0)
        except FileCountException as fce:
            print(fce.args[0])
            sys.exit(0)

    elif not args.d is None:  # if directory option is used
        if os.path.isdir(args.d):
            try:
                file_list = selectAllFastaFiles(args.d, False)  # select all Fasta-files
                checkTargetLengths(file_list)
            except ValueError as ve:
                print(ve.args[0])
                sys.exit(0)
            except FileCountException as fce:
                print(fce.args[0])
                sys.exit(0)
        else:
            print('ERROR: directiory {} was not found or does not exist.'.format(args.d))
            sys.exit(0)
    else:  # if single file option was used
        file_list = []

    if not args.sfs is None:  # if file-list option is used
        struct_sfs_list = [f.name for f in args.sfs]
        struct_list = struct_sfs_list
        try:
            for f in struct_sfs_list:
                checkFileExtension(f, True)  # check file extension
                checkSecFileFormat(f)
        except ValueError as ve:
            print(ve.args[0])
            sys.exit(0)
        except FileCountException as fce:
            print(fce.args[0])
            sys.exit(0)
        except InputValueException as ive:
            print(ive.args[0])
            sys.exit(0)

    if not args.sd is None:  # if directory option is used
        if os.path.isdir(args.sd):
            try:
                struct_sd_list = selectAllFastaFiles(args.sd, True)  # select all Fasta-files
                struct_list = struct_sd_list
                for f in struct_sd_list:
                    checkSecFileFormat(f)
            except ValueError as ve:
                print(ve.args[0])
                sys.exit(0)
            except FileCountException as fce:
                print(fce.args[0])
                sys.exit(0)
            except InputValueException as ive:
                print(ive.args[0])
                sys.exit(0)
    if not args.sf is None:  # if single file option was used
        struct_sf_list = [args.sf]
        struct_list = struct_sf_list
        try:
            checkSecFileFormat(args.sf)
        except InputValueException as ive:
            print(ive.args[0])
            sys.exit(0)

    try:
        checkArguments(file_list, args.f, args.console, args.k, args.d, args.fs, struct_sfs_list, struct_sd_list,
                       struct_sf_list)
    except InputValueException as ive:
        print(ive.args[0])
        sys.exit(0)

    # ----------------------------------------- check options/files ----------------------------------------------------

    if args.f is not None:
        file = args.f.name
        try:
            checkFileExtension(file, False)
        except FileCountException as fce:
            print(fce.args[0])
            sys.exit(0)
        files = [file]
    else:
        files = [file_list[0], file_list[1]]

    # -------------------------------------------- program start ------------------------------------------------------

    if args.console:
        try:
            printData(files, args.k, args.peak, args.top)
        except FileCountException as fce:
            print(fce.args[0])
        except InputValueException as ive:
            print(ive.args[0])
        except FileNotFoundError as fnf:
            print(fnf.args[0])
    else:
        try:
            dashLayout.startDash(file_list, args.port,struct_list)
        except InputValueException as ive:
            print(ive.args[0])
        except FileNotFoundError as fnf:
            print(fnf.args[0])
    if os.path.exists('./tmp/'):
        subprocess.run(['rm', '-r', './tmp/'])
