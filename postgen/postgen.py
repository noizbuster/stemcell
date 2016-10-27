import argparse
import shutil
import os
import sys
import re
import stat

# default values for test
defaultPathSrc = './'
defaultPathDest = './postgen-posts'
defaultPathAssets = './postgen-assets'
defaultRelativeImagePath = '/postgen-assets/'

# initialize argument parser
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--src', '-s', default=defaultPathSrc, help='path of source directory (default: "./")')
parser.add_argument('--dest', '-d', default=defaultPathDest,
                    help='path of destination directory (default: "./postgen")')
parser.add_argument('--assets', '-a', default=defaultPathAssets,
                    help='path of assets(not a md) destination directory (default: "./postgen")')
parser.add_argument('--image', '-i', default=defaultRelativeImagePath,
                    help='path of assets(not a md) destination directory (default: "./postgen")')

# parse arguments
args = parser.parse_args()
sourceDir = parser.parse_args()
src = os.path.abspath(sourceDir.src)
dest = os.path.abspath(sourceDir.dest)
asset = os.path.abspath(sourceDir.assets)
img = sourceDir.image

# data
directories = []
mdFiles = []
assetFiles = []


# customized copytree (overwrite support)
def copytree(_src, _dst, symlinks=False, ignore=None, copy_function=shutil.copy2):
    if not os.path.exists(_dst):
        os.makedirs(_dst)
        # shutil.copystat(_src, _dst)
    if os.path.isdir(_src):
        lst = os.listdir(_src)
        if ignore:
            excl = ignore(_src, lst)
            lst = [x for x in lst if x not in excl]
        for item in lst:
            s = os.path.join(_src, item)
            d = os.path.join(_dst, item)
            if symlinks and os.path.islink(s):
                if os.path.lexists(d):
                    os.remove(d)
                os.symlink(os.readlink(s), d)
                try:
                    st = os.lstat(s)
                    mode = stat.S_IMODE(st.st_mode)
                    os.lchmod(d, mode)
                except:
                    pass  # lchmod not available
            elif os.path.isdir(s):
                copytree(s, d, symlinks, ignore, copy_function=copy_function)
            else:
                copy_function(s, d)
    else:
        copy_function(_src, _dst)


# customized copy function for copy only markdown
def copy_only_markdown(_src, _dst):
    _ext = os.path.splitext(_src)[1]
    if _ext == '.md':
        shutil.copy2(_src, _dst)
    else:
        return


# string replace for correcting image resources' path
def replace_word(infile, imgPath):
    if not os.path.isfile(infile):
        print("Error on replace_word, not a regular file: " + infile)
        sys.exit(1)

    f1 = open(infile, 'r').read()
    f2 = open(infile, 'w')
    m = re.sub(r'!\[?(.*)\]\((.*)\)', r'![\1](%s\2)' % (imgPath), f1)
    f2.write(m)

# parse directory tree
for dirname, dirnames, filenames in os.walk(src):
    for subdirname in dirnames:
        path = os.path.join(dirname, subdirname)
        path = path.replace(src + '/', '')
        directories.append(path)

    for filename in filenames:
        path = os.path.join(dirname, filename)
        path = path.replace(src + '/', '')
        ext = os.path.splitext(os.path.join(dirname, filename))[1]
        if ext == '.md':
            path = os.path.join(dest, path)
            print('md file')
            print('filename:\t' + filename)
            print('documentName:\t' + os.path.splitext(filename)[0])
            print('dirname:\t' + dirname)
            documentName = os.path.splitext(filename)[0]
            print('lastdir:\t' + documentName)
            srcf = os.path.join(dirname, filename)
            desf = os.path.join(dest, documentName)
            print('source_path:\t' + srcf)
            print('destination:\t' + desf)
            copytree(srcf, desf)
            # mdFiles.append(path)
            # shutil.copy2(path, dest)
        else:
            path = os.path.join(asset, path)
            print('not md file')
            print('filename:\t' + filename)
            print('dirname:\t' + dirname)
            print('lastdir:\t' + os.path.basename(os.path.normpath(dirname)))
            srcf = os.path.join(dirname, filename)
            desf = os.path.join(dest, os.path.basename(dirname), os.path.basename(dirname))
            print('source_path:\t' + srcf)
            print('destination:\t' + desf)
            copytree(srcf, desf)
            # shutil.copy2(path, dest)
            # assetFiles.append(path)
            # shutil.copy2(path, os.path.join(asset, path, path))
    if '.git' in dirnames:
        dirnames.remove('.git')

print('Finished')
