#===============================================================================
## \file fileutils.py
# \brief
# Class to manage temporary directory and file manipulation
# \author
# Marc Joos <marc.joos@gmail.com>
# \copyright
# Copyrights 2015, Marc Joos.
# This file is distributed under the CeCILL-A & GNU/GPL licenses, see
# <http://www.cecill.info/licences/Licence_CeCILL_V2.1-en.html> and
# <http://www.gnu.org/licenses/>
# \date
# \b created:          02-19-2015
# \b last \b modified: 02-19-2015

#===============================================================================
import os
import re

class FileTree:
    """Class to manage directory tree"""
    def __init__(self, inputDir="./", tmpRoot='./tmp', extension=['.f90', '.F90']):
        """Initialization method."""
        self.dir = inputDir
        self.tmpRoot = tmpRoot
        if self.tmpRoot:
            self.tmp = True
        else:
            self.tmp = False
        extLen = map(len, extension)
        extension = [item for (len_, item) in sorted(zip(extLen, extension))]
        self.extension = extension

    def listFiles(self):
        """List directory and files."""
        self.dirList = []
        self.fileList = []
        self._listIgnore = []
        dot = re.compile(r'\.[^\/]')
        for root, dirs, files in os.walk(self.dir):
            isdot = [dot.match(root.split('/')[-n]) for n in xrange(len(root.split('/')))]
            if not any(isdot):
                self._listFiles(root, files)
        self._cleanFiles()

    def _listFiles(self, root, files):
        """List files and files to ignore."""
        root = (root[:-1] if root[-1] == '/' else root)
        if root.split('/')[-1][0] != '.' or len(root.split('/')[-1]) == 1:
            if self._listIgnore:
                for ignore in self._listIgnore:
                    if root[:len(ignore)] == ignore:
                        return
                    else:
                        if files:
                            self.dirList.append(root)
                            self.fileList.append(files)
            else:
                if files:
                    self.dirList.append(root)
                    self.fileList.append(files)
        else:
            self._listIgnore.append(root)

    def _cleanFiles(self):
        """Clean directories and files to ignore."""
        if self.dirList:
            for i, fileList in enumerate(self.fileList):
                iterList = fileList.__iter__()
                filesToRemove = []
                filesToKeep = []
                for file_ in iterList:
                    for fileExt in self.extension:
                        if file_[-len(fileExt):] in fileExt:
                            filesToKeep.append(file_)
                    if file_[0] == '#':
                        print('Warning: you probably forgot to save ' + file_)
                        filesToRemove.append(file_)
                iterList = fileList.__iter__()
                for file_ in iterList:
                    if (file_ in filesToKeep) & (file_ in filesToRemove):
                        filesToRemove.remove(file_)
                    if file_ not in filesToKeep:
                        filesToRemove.append(file_)
                if filesToRemove:
                    for file_ in filesToRemove:
                        self.fileList[i].remove(file_)
            for i, fileList in enumerate(self.fileList):
                if not fileList: 
                    self.fileList.remove(self.fileList[i])
                    self.dirList.remove(self.dirList[i])

    def _removeTrailingDot(self, dirList):
        """Remove trailing dots in a given path."""
        cleanDirs = []
        trailingDot = re.compile(r'\.\.\/')
        for dir_ in dirList:
            cleanDirs.append(trailingDot.sub('', dir_))
        return cleanDirs
