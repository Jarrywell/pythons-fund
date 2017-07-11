#!/usr/bin/python

import sys
import os
import shutil

BUFF_SIZE = 1024

def is_file_different(a, b):
    #print a, os.path.getsize(a), b, os.path.getsize(b)

    if (os.path.getsize(a) != os.path.getsize(b)):
        # If the file size is different, the content must be different.
        return True

    # Read the content of the files, and compare them.
    result = False

    fa = open(a, 'rb')
    fb = open(b, 'rb')

    while True:
        buff_a = fa.read(BUFF_SIZE)
        buff_b = fb.read(BUFF_SIZE)

        if (buff_a != buff_b):
            result = True
            break

        if len(buff_a) < BUFF_SIZE:
            #finished
            break

    fa.close()
    fb.close()

    return result



def copy_file(src, dest):
    if not os.path.exists(src):
        raise ValueError("Source file not found")

    #make parent directory (if necessary)
    destdir = os.path.dirname(dest)
    if not os.path.exists(destdir):
        try:
            os.makedirs(destdir)
        except ValueError, e:
            raise ValueError("Unable to create directory " + destdir)
    elif not os.path.isdir(destdir):
        raise ValueError(destdir + "is not a directory")

    if not os.path.exists(dest) or is_file_different(src, dest):
        # If the destination file does not exist or the source file is
        # different from the destination file, then we copy the file.
        shutil.copy(src, dest)

def main():
    if len(sys.argv) < 3:
        print >> sys.stderr, 'USAGE:', sys.argv[0], '<srcfile> <destfile>'
        sys.exit(1)
    srcfile = os.path.abspath(sys.argv[1])
    destfile = os.path.abspath(sys.argv[2])
    if (srcfile == destfile):
        print >> sys.stderr, 'WARNING: <srcfile> is equal to <destfile>'
    else:
        try:
            copy_file(srcfile, destfile)
        except ValueError, e:
            print sys.stderr, 'ERROR:', e
            sys.exit(1)


if __name__ == "__main__":
    main()
