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
        shutil.copystat(_src, _dst)
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


print('======================================================================')
print('Source Directory : ', sourceDir.src)
print('Destination Directory : ', sourceDir.dest)
print('Assets Destination Directory : ', sourceDir.assets)
print('full path of source : ', src)
print('full path of destination : ', dest)
print('full path of assets : ', dest)
print('relative image path: ', img)
print('======================================================================')

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
            mdFiles.append(path)
        else:
            path = os.path.join(asset, path)
            assetFiles.append(path)
    if '.git' in dirnames:
        dirnames.remove('.git')

# copy files
copytree(sourceDir.src, sourceDir.assets, ignore=shutil.ignore_patterns('*.md'))
copytree(sourceDir.src, sourceDir.dest, copy_function=copy_only_markdown)

# confirm
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
print('======================================================================')

# mutate target file (replace image resource path)
for idx, md in enumerate(mdFiles):
    filename = os.path.basename(md)
    postpath = md
    postpath = postpath.replace(dest, '')
    postpath = postpath.replace(filename, '')
    appendpath = img + postpath + '/'
    replace_word(md, appendpath)

print('Finished')
