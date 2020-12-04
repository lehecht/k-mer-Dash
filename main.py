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
argparser.add_argument('-f1', '--file1', dest='f1', action='store', required=True, help="first Fasta-File.")
argparser.add_argument('-f2', '--file2', dest='f2', action='store', required=True, help="second Fasta-File.")
argparser.add_argument('-k', dest='k', action='store', type=checkValue, required=True,
                       help="length of k-Mer. Must be smaller than sequence length.")
argparser.add_argument('-p', '--peak', dest='peak', nargs='?', action='store', type=checkValue,
                       help="peak position in sequence. Must be smaller than 'k' or equal.")
argparser.add_argument('-t', '--top', dest='top', default=10, nargs='?', action='store', type=checkValue,
                       help="shows first 't' entries (Default: 10).")
argparser.add_argument('-hl', '--highlights', dest='highlight', default=10, nargs='?', action='store', type=checkValue,
                       help="number of max-value highlights in scatter-plot (Default: 10).")
argparser.add_argument('-c', '--console', dest='console', default=False, nargs='?', action='store', type=bool,
                       help="starts program in dash mode (= Default) or on commandline (= True).")

if __name__ == '__main__':
    exit = False
    args = argparser.parse_args()
    files = [args.f1, args.f2]
    for file in files:
        try:
            open(file)
        except IOError:
            print('\'{}\' does not exist'.format(file))
            sys.exit(0)
    if args.console:
        try:
            printData(files, args.k, args.peak, args.top, args.highlight)
        except FileCountException as fce:
            print(fce.args[0])
        except InputValueException as ive:
            print(ive.args[0])
        except FileNotFoundError as fnf:
            print(fnf.args[0])
    else:
        try:
            dashLayout.startDash(files, args.k, args.peak, args.top, args.highlight)
        except InputValueException as ive:
            print(ive.args[0])
        except FileNotFoundError as fnf:
            print(fnf.args[0])
    if os.path.exists('./tmp/'):
        subprocess.run(['rm', '-r', './tmp/'])
