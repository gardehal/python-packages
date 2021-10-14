import os

class FilePathObject():
    def __init__(self, fullPath = "", directory = "", relativePath = "", fileLeaf = "", filename = "", fileroot = "", extension = "", extensionWithDot = ""):
        self.fullPath = fullPath
        self.directory = directory
        self.relativePath = relativePath
        self.fileLeaf = fileLeaf
        self.filename = filename
        self.fileroot = fileroot
        self.extension = extension
        self.extensionWithDot = extensionWithDot

    def __init__(self, relativePath = None, fullPath = None):
        if(relativePath == None and fullPath == None):
            return None

        _fullPath = os.path.abspath(relativePath)
        self.fullPath = _fullPath
        self.directory = os.path.split(_fullPath)[0]
        self.relativePath = relativePath # TODO like ., .., ..\\..\\.. fullpath minus current directory?
        self.fileLeaf = os.path.split(self.directory)[-1]
        self.filename = os.path.basename(relativePath)
        self.fileroot = self.filename.split(".")[0]
        self.extension = relativePath.split(".")[-1]
        self.extensionWithDot = f".{self.extension}"

    # https://stackoverflow.com/questions/2235173/what-is-the-naming-standard-for-path-components
    # Consider the URI:
    # C:\users\OddThinking\Documents\My Source\Widget\foo.src

    # A) foo
    # Vim calls it file root (:help filename-modifiers)

    # B) foo.src
    # file name or base name

    # C) src (without dot)
    # file/name extension

    # D) .src (with dot)
    # also file extension. Simply store without the dot, if there is no dot on a file, it has no extension

    # E) C:\users\OddThinking\Documents\My Source\
    # top of the tree
    # No convention, git calls it base directory

    # F) Widget\foo.src
    # path from top of the tree to the leaf
    # relative path

    # G) Widget
    # one node of the tree
    # no convention, maybe a simple directory

    # H) C:\users\OddThinking\Documents\My Source\Widget\
    # dir name

    # I) C:\users\OddThinking\Documents\My Source\Widget\foo.src
    # full/absolute path