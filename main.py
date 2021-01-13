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
argparser.add_argument('-f1', '--file1', dest='f1', action='store', required=True,
                       help="first Fasta-File. Allowed file extensions are \'.fa, .fasta, .fna, .fsa, .ffn\'")
argparser.add_argument('-f2', '--file2', dest='f2', action='store', required=True,
                       help="second Fasta-File. Allowed file extensions are \'.fa, .fasta, .fna, .fsa, .ffn\'")
argparser.add_argument('-k', dest='k', action='store', type=checkValue,
                       help="length of k-Mer. Must be smaller than sequence length. Required in commandline-mode only.")
argparser.add_argument('-p', '--peak', dest='peak', nargs='?', action='store', type=checkValue,
                       help="(optional) peak position in sequence. Must be smaller or equal than given sequence length.")
argparser.add_argument('-t', '--top', dest='top', default=10, nargs='?', action='store', type=checkValue,
                       help="(optional) shows top kmers (Default: 10).")
argparser.add_argument('-c', '--console', dest='console', default=False, nargs='?', action='store', type=bool,
                       help="starts program with gui (= False (Default)) or on commandline (= True).")


def checkFileFormat(file):
    ext = os.path.splitext(file)[1]
    if ext not in [".fa", ".fasta", ".fna", ".fsa", ".ffn"]:
        raise InputValueException(
            "Only Fasta-files with file-extension: \'.fa\', \'.fasta\', \'.fna\', \'.fsa\', \'.ffn\' allowed!")


def checkArguments(c, k):
    if c and (k is None):
        raise InputValueException("k is required in commandline-mode.")


if __name__ == '__main__':
    exit = False
    args = argparser.parse_args()

    try:
        checkArguments(args.console, args.k)
    except InputValueException as ive:
        print(ive.args[0])
        sys.exit(0)

    files = [args.f1, args.f2]
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
            dashLayout.startDash(files)
        except InputValueException as ive:
            print(ive.args[0])
        except FileNotFoundError as fnf:
            print(fnf.args[0])
    if os.path.exists('./tmp/'):
        subprocess.run(['rm', '-r', './tmp/'])
