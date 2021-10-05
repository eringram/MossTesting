#!/usr/bin/env python

import zipfile
import tarfile
import sys
import os
import itertools
import shutil

# The current bblearn format dictates that the username is surrounded by a leading and 
# trailing underscore. Therefore, based on the current format, we will assume that the 
# username can be found between the first and second underscore
def extractAndRenameZips(zipFileRoot):
    directories = []
    os.chdir(zipFileRoot)
    # For each file in the zip root dir (should all be zip files...)
    for zippy in sorted(os.listdir(os.getcwd())):
        # Rar files will be responsible for the eventual death of the human race
        if not zippy.endswith(".zip") and not zippy.endswith("tar.gz"):
            print("Some asshole probably submitted a rar file")
            print("Here's the file: " + zippy)
            continue

        # Make sure we have a file
        if not os.path.isfile(zippy):
            print("Something here is not what it should be")
            continue

        # Figure out the username so we know what to call the extracted directory
        unzippedDirNamePart1 = zippy.split('_', 1)[-1]
        unzippedDirName = unzippedDirNamePart1.split('_', 1)[0]
        directories.append(unzippedDirName)

        # See the ... above, double check that they're all zip files
        if zippy.endswith(".zip"):
            try:
                theZip = zipfile.ZipFile(zippy, 'r')
                theZip.extractall(unzippedDirName)
                theZip.close()
                os.remove(zippy)
            except: 
                print("Failed to unzip: " + zippy)
                pass
        
        # Not supposed to use tar files, but I'm not about to fault a *nix user
        if zippy.endswith(".tar.gz"):
            try:
                tar = tarfile.open(zippy, "r:gz")
                tar.extractall(unzippedDirName)
                tar.close()
                os.remove(zippy)
            except:
                print("Failed to untar: " + zippy)
                pass

    # Move back out to the root dir
    os.chdir("..")
    return directories

# Now all of the java files need to be pulled to the root of the unzipped directory. Moss only looks
# inside 1 level of directory, it doesn't do much good to have the code all organized in packages.
def moveFiles(root):
    # Get a list of all subdirectories (i.e. all users)
    subdirs = filter(os.path.isdir, [os.path.join(root, path) for path in os.listdir(root)])
    # Extension types we want to preserve
    extensions = [".py", ".java", ".cpp", ".h", ".json"]

    # Try to remove the common files before pulling out the src files
    for common in subdirs:
        for root, dirs, files in os.walk(common, topdown=False):
            for folder in dirs:
                if folder.endswith("ommon"):
                    commonPath = os.path.join(root, folder)
                    shutil.rmtree(commonPath)
                if folder.endswith("OSX"):
                    osxPath = os.path.join(root, folder)
                    shutil.rmtree(osxPath)

    # For each submission, find all of the source files and move them to the userdir root
    for userdir in subdirs:
        for root, dirs, files in os.walk(userdir, topdown=False):
            for srcfile in files:
                # If file has no extension, might be Python script
                shebang = ""
                if "." not in srcfile:
                    with open(os.path.join(root, srcfile)) as openFile:
                        shebang = openFile.readline().rstrip()
                # Make sure to only move the source files
                # Include common file types since language is student's choice, also check for Python shebang
                if any(ext in srcfile for ext in extensions) or \
                    ("#!/usr/bin/env python3" in shebang) or ("#!/usr/bin/env python" in shebang):
                    try:
                        shutil.move(os.path.join(root, srcfile), os.path.join(userdir, srcfile))
                        print("Moved file: " + srcfile)
                    except OSError:
                        print("Failed to move: " + srcfile)
                        pass

    # Time to go through and remove anything that is a directory or not a source file
    for userdir in subdirs:
        for item in sorted(os.listdir(userdir)): 
            deletePath = userdir + "/" + item
            # Delete any directories, all sources should have already been pulled out
            if os.path.isdir(deletePath):
                shutil.rmtree(deletePath)
            if os.path.isfile(deletePath):
                # Get shebang again
                shebang = ""
                if "." not in deletePath:
                    with open(deletePath) as openFile:
                        shebang = openFile.readline().rstrip()
                # Delete any non source files. I don't want class and jars getting sent to moss
                if not (any(ext in deletePath for ext in extensions) or \
                    ("#!/usr/bin/env python3" in shebang) or ("#!/usr/bin/env python" in shebang)):
                    os.remove(deletePath)
                    print("Deleted " + deletePath)

if __name__ == "__main__":
    learnZipRoot = "zipsFromLearn"
    directories = extractAndRenameZips(learnZipRoot)
    #NOTE:  For some reason moveFiles does not function properly with Python 3. I have not
    #NOTE:  taken the time to figure out why. 
    moveFiles(learnZipRoot)

