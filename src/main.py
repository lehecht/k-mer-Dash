from argparse import ArgumentParser
from console_output import printData
import subprocess
import os

argparser = ArgumentParser()
argparser.add_argument('-f', '--files', dest='data', action='store', required=True)
argparser.add_argument('-k', dest='k', action='store', type=int, required=True)
argparser.add_argument('-p', '--peak', dest='peak', nargs='?', action='store', type=int)
argparser.add_argument('-t', '--top', dest='top', default=10, nargs='?', action='store', type=int)
argparser.add_argument('-c', '--console', dest='console', default=False, nargs='?', action='store', type=bool)

if __name__ == '__main__':
    args = argparser.parse_args()
    files = args.data.split(',')  # convert string of files in a list
    for file in files:
        try:
            open(file)
        except IOError:
            print('{} does not exist'.format(file))
            break
    if args.console:
        printData(files, args.k, args.peak, args.top)
    else:
        pass  # start dash
    if os.path.exists('./tmp/'):
        subprocess.run(['rm', '-r', './tmp/'])
