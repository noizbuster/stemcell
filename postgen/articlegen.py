import argparse
import shutil
import os
import sys
import re
import stat
from datetime import datetime

# default values for test
dtargetDirectory = './'
dtitle = './postgen-posts'

# initialize argument parser
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--dest', '-d', default=dtargetDirectory, help='path of source directory (default: "./")')
parser.add_argument('--title', '-t', default=dtitle,
                    help='path of destination directory (default: "./postgen")')


def touch(path):
    with open(path, 'a'):
        os.utime(path, None)


# parse arguments
args = parser.parse_args()
targetDirectory = os.path.abspath(args.dest)
title = args.title

now = datetime.now()
path = now.strftime('%Y-%m-%d-%H%M%S-') + title

print(path)
print(targetDirectory)

directory = os.path.join(targetDirectory, path)
filename = os.path.join(directory, path + '.md')

os.makedirs(directory)
touch(filename)

# data
directories = []
mdFiles = []
assetFiles = []
