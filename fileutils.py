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
        # Reorder extensions by character length
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
                for file_ in iterList:
                    if not(file_[-4:] in ['.f90', '.F90'] or \
                       file_[-2:] in ['.f', '.F']):
                        filesToRemove.append(file_)
                    if file_[0] == '#':
                        print('Warning: you probably forgot to save ' + file_)
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
