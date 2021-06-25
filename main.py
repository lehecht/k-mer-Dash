import argparse
import os
import subprocess
import sys
import socket
from pathlib import Path
from Bio import SeqIO
from src.console_output import printData
from src.dashView import dashLayout
from src.inputValueException import InputValueException
from src.fileCountException import FileCountException


# checks if input is a digit greater than zero
# value: input peak, k or top value
def checkValue(value):
    if not value.isdigit():
        raise argparse.ArgumentTypeError("Invalid Value: Value must be integer.\nFor help use option -h.")
    elif int(value) <= 0:
        raise argparse.ArgumentTypeError("Invalid Value: Must be greater than 0.\nFor help use option -h.")
    return int(value)


# checks if port is valid number and port status
# port: input port number
def checkPort(port):
    if not port.isdigit():
        raise argparse.ArgumentTypeError("Invalid Value: Port must be integer.\nFor help use option -h.")
    p = int(port)
    if p not in list(range(1, 65535 + 1)):
        raise argparse.ArgumentTypeError("Invalid Value: Port must be in range of 1 to 65535.\n"
                                         "For help use option -h.")
    # test if port is open
    try:
        ip = "0.0.0.0"
        serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serv.bind((ip, p))
        serv.close()
    except OSError:
        raise argparse.ArgumentTypeError(
            "ERROR: Port {} is already in use or cannot be used.\nFor help use option -h.".format(p))

    return p


# checks if value is boolean
# b: input value
def checkBool(b):
    if b in ["True", "true", "1"]:
        return True
    elif b in ["False", "false", "0"]:
        return False
    else:
        raise argparse.ArgumentTypeError("ERROR: -c option must be a boolean value: True or False (Default).\n"
                                         "For help use option -h.")


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
                       help="(optional) Number of displayed top kmers (Default: 10). "
                            "Required in commandline-mode only.")
argparser.add_argument('-c', '--console', dest='console', default=False, action='store', type=checkBool,
                       help="Starts program with GUI (Default: False) or on commandline (=True).")
argparser.add_argument('-pt', '--port', dest='port', default=8088, action='store', type=checkPort,
                       help="(optional) Port on which interactive dash app runs. "
                            "Must be in range of 1 to 65535 (Default: 8088).")


def checkSecFileFormat(f):
    record = str(list(SeqIO.parse(f, "fasta"))[0].seq)

    if 'A' in record or 'T' in record or 'C' in record or 'G' in record:
        raise InputValueException("ERROR: Fasta files for secondary structure must only contain element-strings.\n"
                                  "For help use option -h.")


def checkFileExtension(f, struct):
    ext = os.path.splitext(f)[1]
    if struct:
        ext_list = [".fa", ".fasta", ".fsa"]
    else:
        ext_list = [".fa", ".fasta", ".fna", ".fsa", ".ffn"]

    if ext not in ext_list:
        if struct:
            msg = "ERROR: only Fasta-files with file-extension: \'.fa\', \'.fasta\', \'.fsa\' allowed!\n" \
                  "For help use option -h."
        else:
            msg = "ERROR: only Fasta-files with file-extension: " \
                  "\'.fa\', \'.fasta\', \'.fna\', \'.fsa\', \'.ffn\' allowed!\nFor help use option -h."

        raise InputValueException(msg)

    if os.stat(f).st_size is 0:
        raise FileCountException('ERROR: file(s) is empty.\nFor help use option -h.')


def checkArguments(f_list, f, c, k, fasta_dir, fs_list, sfs, sd, sf):
    if sfs is not None:
        struct_file_list = sfs
    else:
        struct_file_list = sd

    if c and (k is None):
        raise InputValueException("ERROR: k is required in commandline-mode.\nFor help use option -h.")
    if len(f_list) > 0 and (f is not None):
        raise InputValueException("ERROR: please choose either -fs or -d for interactive mode "
                                  "or -f for command-line mode.\nFor help use option -h.")
    elif len(f_list) > len(set(f_list)):
        raise InputValueException("ERROR: every nucleotide FASTA-file name must be unique.\nFor help use option -h.")
    elif struct_file_list is not None and len(struct_file_list) > len(set(struct_file_list)):
        raise InputValueException("ERROR: every structural FASTA-file name must be unique.\nFor help use option -h.")
    elif (f is not None or len(f_list) < 2) and not c:
        raise InputValueException("ERROR: interactive mode needs at least two files.\nFor help use option -h.")
    elif len(f_list) > 0 and c:
        raise InputValueException(
            "ERROR: commandline-mode requires only single Fasta-file.\nPlease use -f option. For help use option -h.")
    elif (fasta_dir is not None) and (fs_list is not None):
        raise InputValueException(
            "ERROR: please choose either -fs to commit a list of files or -d for a directory.\nFor help use option -h.")
    elif not [sfs, sd, sf].count(None) > 1:
        raise InputValueException(
            "ERROR: please choose either -sfs, -sd or -sf to commit structural data.\nFor help use option -h.")


def selectAllFastaFiles(drctry, struct):
    files_list = []
    if struct:
        ext_list = [".fa", ".fasta", ".fsa"]
    else:
        ext_list = [".fa", ".fasta", ".fna", ".fsa", ".ffn"]

    for ext in ext_list:
        files_list.extend(Path(drctry).glob('*{}'.format(ext)))

    if len(files_list) == 0:
        if struct:
            msg = 'ERROR: \'{}\' has no Fasta-files with extension: .fa, .fasta, .fsa .\n' \
                  'For help use option -h.'.format(drctry)
        else:
            msg = 'ERROR: \'{}\' has no Fasta-files with extension: .fa, .fasta, .fna, .fsa, .ffn .\n' \
                  'For help use option -h.'.format(drctry)

        raise FileCountException(msg)

    for f in files_list:
        if os.stat(f).st_size is 0:
            raise FileCountException(
                'ERROR: file(s) in \'{}\' is/are empty.\nFor help use option -h.'.format(drctry))
    return files_list


def checkTargetLengths(files_list):
    f = open(files_list[0])
    target = f.readline()
    target = f.readline()  # read only first sequence
    target_len = len(target)
    for f in files_list[1:]:
        f = open(f)
        f.readline()
        target = f.readline()  # read only first sequence
        if not target_len == len(target):
            raise ValueError("ERROR: sequence-length must be equal in all files.\nFor help use option -h.")
    f.close()


if __name__ == '__main__':
    args = argparser.parse_args()

    # ------------------------------------------ save files ------------------------------------------------------------

    struct_sfs_list = None
    struct_sd_list = None
    struct_sf_list = None
    struct_list = None

    if args.fs is not None:  # if file-list option is used
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

    elif args.d is not None:  # if directory option is used
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
            print('ERROR: directory \'{}\' was not found or does not exist.\nFor help use option -h.'.format(args.d))
            sys.exit(0)
    else:  # if single file option was used
        file_list = []

    if args.sfs is not None:  # if file-list option is used
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

    if args.sd is not None:  # if directory option is used
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
        else:
            print('ERROR: directory \'{}\' was not found or does not exist.\nFor help use option -h.'.format(args.sd))
            sys.exit(0)
    if args.sf is not None:  # if single file option was used
        struct_sf_list = [args.sf.name]
        struct_list = struct_sf_list
        try:
            checkSecFileFormat(args.sf)
        except InputValueException as ive:
            print(ive.args[0])
            sys.exit(0)

    try:
        checkArguments(file_list, args.f, args.console, args.k, args.d, args.fs, struct_sfs_list, struct_sd_list,
                       struct_sf_list)
        if struct_list is not None:
            checkTargetLengths(struct_list)
    except InputValueException as ive:
        print(ive.args[0])
        sys.exit(0)
    except ValueError as ve:
        print(ve.args[0])
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
        if args.console and (args.sd or args.sf or args.sfs):
            print("INFO: Console mode does not support visualization for structural data.")
            print()
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
            dashLayout.startDash(file_list, args.port, struct_list)
        except InputValueException as ive:
            print(ive.args[0])
        except FileNotFoundError as fnf:
            print(fnf.args[0])
    if os.path.exists('./tmp/'):
        subprocess.run(['rm', '-r', './tmp/'])
