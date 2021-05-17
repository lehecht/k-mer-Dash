import argparse
import os
import subprocess
import sys
from pathlib import Path

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
                       help="List of space-separated Fasta-files. "
                            "Allowed file extensions are \'.fa, .fasta, .fna, .fsa, .ffn\'")
argparser.add_argument('-d', '--directory', dest='d', action='store',
                       help="Directory with Fasta-Files. Allowed file extensions are \'.fa, .fasta, .fna, .fsa, .ffn\'")
argparser.add_argument('-f', '--file', dest='f', action='store', type=argparse.FileType('r'),
                       help="Single Fasta-File for commandline-mode. "
                            "Allowed file extensions are \'.fa, .fasta, .fna, .fsa, .ffn\'")
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


def checkFileFormat(file):
    ext = os.path.splitext(file)[1]
    if ext not in [".fa", ".fasta", ".fna", ".fsa", ".ffn"]:
        raise InputValueException(
            "ERROR: only Fasta-files with file-extension: \'.fa\', \'.fasta\', \'.fna\', \'.fsa\', \'.ffn\' allowed!")

    if os.stat(file).st_size is 0:
        raise FileCountException('ERROR: file(s) is empty.')


def checkArguments(file_list, f, c, k, dir, list):
    if c and (k is None):
        raise InputValueException("ERROR: k is required in commandline-mode.")
    if len(file_list) > 0 and (not (f is None)):
        raise InputValueException("ERROR: please choose either -fs or -d for interactive mode "
                                  "or -f for command-line mode.")
    elif len(file_list) > len(set(file_list)):
        raise InputValueException("ERROR: every file must be unique.")
    elif (not f is None or len(file_list) < 2) and not c:
        raise InputValueException("ERROR: interactive mode needs at least two files.")
    elif len(file_list) > 0 and c:
        raise InputValueException("ERROR: commandline-mode requires only single Fasta-file. Please use -f option.")
    elif (not dir is None) and (not list is None):
        raise InputValueException("ERROR: please choose either -fs to commit a list of files or -d for a directory.")


def selectAllFastaFiles(dir):
    file_list = []
    for ext in [".fa", ".fasta", ".fna", ".fsa", ".ffn"]:
        file_list.extend(Path(dir).rglob('*{}'.format(ext)))

    if len(file_list) == 0:
        raise FileCountException(
            'ERROR: {} has no Fasta-files with extension: .fa, .fasta, .fna, .fsa, .ffn'.format(dir))

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
    exit = False
    args = argparser.parse_args()

    # ------------------------------------------ save files ------------------------------------------------------------

    if not args.fs is None:  # if file-list option is used
        file_list = [f.name for f in args.fs]
        try:
            checkTargetLengths(file_list)  # check if all files own sequences with equal lengths
            for f in file_list:
                checkFileFormat(f)  # check file extension
        except ValueError as ve:
            print(ve.args[0])
            sys.exit(0)
        except FileCountException as fce:
            print(fce.args[0])
            sys.exit(0)

    elif not args.d is None:  # if directory option is used
        if os.path.isdir(args.d):
            try:
                file_list = selectAllFastaFiles(args.d)  # select all Fasta-files
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

    try:
        checkArguments(file_list, args.f, args.console, args.k, args.d, args.fs)
    except InputValueException as ive:
        print(ive.args[0])
        sys.exit(0)

    # ----------------------------------------- check options/files ----------------------------------------------------

    if args.f is not None:
        file = args.f.name
        try:
            checkFileFormat(file)
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
            dashLayout.startDash(file_list, args.port)
        except InputValueException as ive:
            print(ive.args[0])
        except FileNotFoundError as fnf:
            print(fnf.args[0])
    if os.path.exists('./tmp/'):
        subprocess.run(['rm', '-r', './tmp/'])
