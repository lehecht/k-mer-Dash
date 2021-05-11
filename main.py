import argparse
import os
import subprocess
import sys

from src.console_output import printData
from src.dashView import dashLayout, initializeData
from src.inputValueException import InputValueException
from src.fileCountException import FileCountException


def checkValue(value):
    val = int(value)
    if val <= 0:
        raise argparse.ArgumentTypeError("Invalid Value: Must be greater than 0")
    return val


argparser = argparse.ArgumentParser()
argparser.add_argument('-fs', '--files', dest='fs', type=argparse.FileType('r'), nargs='+')

argparser.add_argument('-f1', '--file1', dest='f1', action='store',
                       help="first Fasta-File. Allowed file extensions are \'.fa, .fasta, .fna, .fsa, .ffn\'")
argparser.add_argument('-f2', '--file2', dest='f2', action='store',
                       help="second Fasta-File. Allowed file extensions are \'.fa, .fasta, .fna, .fsa, .ffn\'")
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


def checkArguments(file_list, f1, f2, c, k):
    if c and (k is None):
        raise InputValueException("k is required in commandline-mode.")
    if file_list is None and f1 is None and f2 is None:
        raise InputValueException("files are missing.")
    elif (file_list is None and (f1 is None or f2 is None)) or len(file_list) == 1:
        raise InputValueException("at least two files are needed.")


if __name__ == '__main__':
    exit = False
    args = argparser.parse_args()

    file_list = [f.name for f in args.fs]

    try:
        checkArguments(file_list, args.f1, args.f2, args.console, args.k)
    except InputValueException as ive:
        print(ive.args[0])
        sys.exit(0)

    if args.f1 is not None and args.f2 is not None:
        files = [args.f1, args.f2]
    else:
        files = [file_list[0],file_list[1]]

    for file in files:
        try:
            open(file)
            checkFileFormat(file)
        except IOError:
            print('\'{}\' does not exist'.format(file))
            sys.exit(0)
        except InputValueException as ive:
            print(ive.args[0])
            sys.exit(0)
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
