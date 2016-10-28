import argparse
import shutil
import os
import sys
import re
import stat
from datetime import datetime

# default values for test
dtargetDirectory = './'
dtitle = 'untitled'
dcategory = 'uncategorized'
dauthor = 'anonymous'

# initialize argument parser
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--dest', '-d', default=dtargetDirectory, help='path of source directory (default: "./")')
parser.add_argument('--title', '-t', default=dtitle,
                    help='title of article (default: "untitled")')
parser.add_argument('--category', '-c', default=dcategory,
                    help='category of article (default: "uncategorized")')
parser.add_argument('--author', '-a', default=dauthor,
                    help='author of article (default: "anonymous")')


def createArticleFile(path, contents):
    with open(path, 'a') as file:
        os.utime(path, None)
        file.write(contents);

# parse arguments
args = parser.parse_args()
targetDirectory = os.path.abspath(args.dest)
title = args.title
category = args.category
author = args.author

# make some parameters
now = datetime.now()
path = now.strftime('%Y-%m-%d-%H%M%S-') + title.replace(' ', '-')
date = now.strftime('%Y-%m-%d %H:%M:%S')
directory = os.path.join(targetDirectory, path)
filename = os.path.join(directory, path + '.md')

print(path)
print(targetDirectory)

frontmatter = """
---

title:  {0}

author: {1}

date:   {2}

categories: {3}

tags: []

---

""".format(title, author, date, category)

os.makedirs(directory)
createArticleFile(filename, frontmatter)
