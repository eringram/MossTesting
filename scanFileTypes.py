#!/usr/bin/env python3

import os
import unzipAndOrganize430

def scanFileTypes(root):
    # Get a list of all subdirectories (i.e. all users)
    subdirs = filter(os.path.isdir, [os.path.join(root, path) for path in os.listdir(root)])

    # For each submission tally up file types
    extensions = {}
    for userdir in subdirs:
        for root, dirs, files in os.walk(userdir, topdown=False):
            for srcfile in files:
                # Get extension
                filename, ext = os.path.splitext(srcfile)
                # Check if python script with no extension
                if "." not in srcfile:
                    with open(os.path.join(root, srcfile)) as openFile:
                        try:
                            shebang = openFile.readline().rstrip()
                            if ("#!/usr/bin/env python3" in shebang) or ("#!/usr/bin/env python" in shebang):
                                ext = ".py"
                        except:
                            # File is probably a binary executable
                            print("Failed to read file: " + os.path.join(root, srcfile))
                            pass
                if ext in extensions:
                    extensions[ext] += 1
                else:
                    extensions[ext] = 1

    print(extensions)

if __name__ == "__main__":
    learnZipRoot = "zipsFromLearn"
    directories = unzipAndOrganize430.extractAndRenameZips(learnZipRoot)
    scanFileTypes(learnZipRoot)
