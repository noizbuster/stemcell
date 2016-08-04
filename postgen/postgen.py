import argparse
import shutil
import os
import sys
import re

defaultPathSrc = './'
defaultPathDest = './postgen-posts'
defaultPathAssets = './postgen-assets'
defaultRelativeImagePath = '/postgen-assets/'

parser = argparse.ArgumentParser(description='Process some integers.')
# parser.add_argument('integers', metavar='N', type=int, nargs='+',
#                     help='an integer for the accumulator')
parser.add_argument('--src', '-s', default=defaultPathSrc, help='path of source directory (default: "./")')
parser.add_argument('--dest', '-d', default=defaultPathDest,
                    help='path of destination directory (default: "./postgen")')
parser.add_argument('--assets', '-a', default=defaultPathAssets,
                    help='path of assets(not a md) destination directory (default: "./postgen")')
parser.add_argument('--image', '-i', default=defaultRelativeImagePath,
                    help='path of assets(not a md) destination directory (default: "./postgen")')

args = parser.parse_args()
sourceDir = parser.parse_args()
print('======================================================================')
print('Source Directory : ', sourceDir.src)
print('Destination Directory : ', sourceDir.dest)
print('Assets Destination Directory : ', sourceDir.assets)
print('======================================================================')

for file in os.listdir(sourceDir.src):
    print(file)
print('======================================================================')
# print(os.listdir(sourceDir.src))
src = os.path.abspath(sourceDir.src)
dest = os.path.abspath(sourceDir.dest)
asset = os.path.abspath(sourceDir.assets)
img = sourceDir.image

print('full path of source : ', src)
print('full path of destination : ', dest)
print('full path of assets : ', dest)
print('relative image path: ', img)

directories = []
mdFiles = []
assetFiles = []
print('======================================================================')


def copy_only_markdown(_src, _dest):
    _ext = os.path.splitext(_src)[1]
    if _ext == '.md':
        shutil.copy2(_src, _dest)
    else:
        return


def replace_word(infile, imgPath):
    if not os.path.isfile(infile):
        print("Error on replace_word, not a regular file: " + infile)
        sys.exit(1)

    f1 = open(infile, 'r').read()
    f2 = open(infile, 'w')
    # to = compile('![$1](' + imgPath + '$2)')
    # m = f1.replace(old_word, new_word)
    m = re.sub(r'!\[?(.*)\]\((.*)\)', r'![\1](%s\2)' % (imgPath) , f1)
    f2.write(m)


for dirname, dirnames, filenames in os.walk(src):
    # print path to all subdirectories first.
    for subdirname in dirnames:
        # print(dirname, subdirname)
        path = os.path.join(dirname, subdirname)
        path = path.replace(src + '/', '')
        # path = os.path.join(dest, path)
        directories.append(path)

    # print path to all filenames.
    for filename in filenames:
        path = os.path.join(dirname, filename)
        path = path.replace(src + '/', '')
        ext = os.path.splitext(os.path.join(dirname, filename))[1]
        print(ext)
        # print('f', os.path.join(dirname, filename))
        if ext == '.md':
            path = os.path.join(dest, path)
            mdFiles.append(path)
        else:
            path = os.path.join(asset, path)
            assetFiles.append(path)
    # Advanced usage:
    # editing the 'dirnames' list will stop os.walk() from recursing into there.
    if '.git' in dirnames:
        # don't go into any .git directories.
        dirnames.remove('.git')
shutil.copytree(sourceDir.src, sourceDir.assets, ignore=shutil.ignore_patterns('*.md'))
shutil.copytree(sourceDir.src, sourceDir.dest, copy_function=copy_only_markdown)
for md in mdFiles:
    replace_word(md, img)
# '-s', 'source');
print('======================================================================')
print('Directories:')
for direc in directories:
    print(direc)
print('======================================================================')
print('markdown:')
for md in mdFiles:
    print(md)
print('======================================================================')
print('assets:')
for asset in assetFiles:
    print(asset)
# print(args.accumulate(args.integers))
