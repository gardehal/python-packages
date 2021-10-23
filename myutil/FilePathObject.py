import os
from posixpath import isabs

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

    def __init__(self, path):
        if(path == None):
            return None

        _fullPath = None
        _relativePath = None
        if(os.path.isabs(path)):
            _fullPath = path
            _relativePath = os.path.realpath(_fullPath)
        else:
            _fullPath = os.path.abspath(path)
            _relativePath = path
        
        self.fullPath = _fullPath
        self.directory = os.path.split(_fullPath)[0]
        self.relativePath = _relativePath
        self.fileLeaf = os.path.split(self.directory)[-1]
        self.filename = os.path.basename(_fullPath)
        self.fileroot = self.filename.split(".")[0]
        self.extension =  _fullPath.split(".")[-1] if ("." in _fullPath) else ""
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