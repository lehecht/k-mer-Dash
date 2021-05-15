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
    val = int(value)
    if val <= 0:
        raise argparse.ArgumentTypeError("Invalid Value: Must be greater than 0")
    return val


argparser = argparse.ArgumentParser()
argparser.add_argument('-fs', '--files', dest='fs', type=argparse.FileType('r'), nargs='+',
                       help="List of space-separated Fasta-Files. "
                            "Allowed file extensions are \'.fa, .fasta, .fna, .fsa, .ffn\'")
argparser.add_argument('-d', '--directory', dest='d', action='store',
                       help="Directory with Fasta-Files. Allowed file extensions are \'.fa, .fasta, .fna, .fsa, .ffn\'")
argparser.add_argument('-f', '--file', dest='f', action='store', type=argparse.FileType('r'),
                       help="single Fasta-File for commandline-mode. "
                            "Allowed file extensions are \'.fa, .fasta, .fna, .fsa, .ffn\'")
argparser.add_argument('-k', dest='k', action='store', type=checkValue,
                       help="length of k-Mer. Must be smaller than sequence length. Required in commandline-mode only.")
argparser.add_argument('-p', '--peak', dest='peak', nargs='?', action='store', type=checkValue,
                       help="(optional) peak position in sequence. Must be smaller or equal than given sequence length.")
argparser.add_argument('-t', '--top', dest='top', default=10, nargs='?', action='store', type=checkValue,
                       help="(optional) shows top kmers (Default: 10).")
argparser.add_argument('-c', '--console', dest='console', default=False, nargs='?', action='store', type=bool,
                       help="starts program with gui (= False (Default)) or on commandline (= True).")
argparser.add_argument('-pt', '--port', dest='port', default=8088, nargs='?', action='store', type=int,
                       help="(optional) port on which runs dash app")


def checkFileFormat(file):
    ext = os.path.splitext(file)[1]
    if ext not in [".fa", ".fasta", ".fna", ".fsa", ".ffn"]:
        raise InputValueException(
            "Only Fasta-files with file-extension: \'.fa\', \'.fasta\', \'.fna\', \'.fsa\', \'.ffn\' allowed!")

    if os.stat(file).st_size is 0:
        raise FileCountException('file(s) is empty.')


def checkArguments(file_list, f, c, k):
    if c and (k is None):
        raise InputValueException("k is required in commandline-mode.")
    if len(file_list) > 0 and (not (f is None)):
        raise InputValueException("please choose either -fs for interactive mode or -f for command-line mode.")
    elif len(file_list) > len(set(file_list)):
        raise InputValueException("every file must be unique.")
    elif not f is None and not c:
        raise InputValueException("interactive mode needs more than one file.")


def selectAllFastaFiles(dir):
    file_list = []
    for ext in [".fa", ".fasta", ".fna", ".fsa", ".ffn"]:
        file_list.extend(Path(dir).rglob('*{}'.format(ext)))

    if len(file_list) == 0:
        raise FileCountException('{} has no Fasta-files with extension: .fa, .fasta, .fna, .fsa, .ffn'.format(dir))

    for f in file_list:
        if os.stat(f).st_size is 0:
            raise FileCountException('file(s) is empty.')
    return file_list


def checkTargetLengths(fileList):
    f = open(fileList[0])
    target = f.readline()
    target = f.readline()  # read sequence
    targetLen = len(target)
    for file in fileList[1:]:
        f = open(file)
        target = f.readline()
        target = f.readline()  # read sequence
        if not targetLen == len(target):
            raise ValueError("sequence-length must be equal in all files.")


if __name__ == '__main__':
    exit = False
    args = argparser.parse_args()

    if not args.fs is None:
        file_list = [f.name for f in args.fs]
        try:
            checkTargetLengths(file_list)
            for f in file_list:
                checkFileFormat(f)
        except ValueError as ve:
            print(ve.args[0])
            sys.exit(0)
        except FileCountException as fce:
            print(fce.args[0])
            sys.exit(0)
    elif not args.d is None:
        if os.path.isdir(args.d):
            try:
                file_list = selectAllFastaFiles(args.d)
                checkTargetLengths(file_list)
            except ValueError as ve:
                print(ve.args[0])
                sys.exit(0)
            except FileCountException as fce:
                print(fce.args[0])
                sys.exit(0)
        else:
            print('{} was not found or does not exist.'.format(args.d))
            sys.exit(0)
    else:
        file_list = []

    try:
        checkArguments(file_list, args.f, args.console, args.k)
    except InputValueException as ive:
        print(ive.args[0])
        sys.exit(0)

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

    # for file in files:
    #     try:
    #         open(file)
    #         checkFileFormat(file)
    #     except IOError:
    #         print('\'{}\' does not exist'.format(file))
    #         sys.exit(0)
    #     except InputValueException as ive:
    #         print(ive.args[0])
    #         sys.exit(0)

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
