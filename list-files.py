#!/usr/bin/python

import os
import operator
import sys
def get_file_size(path):
    st = os.lstat(path);
    return st.st_size;


def list_files(dirs):
    output = []
    for root in dirs:
        base = len(root[:root.rfind(os.path.sep)])
        for dir, dirs, files in os.walk(root):
            relative = dir[base:]
            for f in files:
                try:
                    row = (get_file_size(os.path.sep.join((dir, f))), os.path.sep.join((relative, f)))
                    output.append(row)
                except os.error:
                    pass
    output.sort(key=operator.itemgetter(0), reverse=True)
    for row in output:
        print "%12d %s" % row


#list_files(['/home/tech/python'])


if __name__ == "__main__":
    if (len(sys.argv) >= 2):
        list_files(sys.argv[1:])
    else:
        print "argv must >= 2"