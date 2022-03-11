import os

class FilePathObject():
    def __init__(self, isFile: bool = False, fullPath: str = "", directory: str = "", relativePath: str = "", fileLeaf: str = "", filename: str = "", fileRoot: str = "", extension: str = "", extensionWithDot: str = ""):
        self.isFile: bool = isFile
        self.fullPath: str = fullPath
        self.directory: str = directory
        self.relativePath: str = relativePath
        self.fileLeaf: str = fileLeaf
        self.filename: str = filename
        self.fileRoot: str = fileRoot
        self.extension: str = extension
        self.extensionWithDot: str = extensionWithDot
        self.inputPath: str = fullPath
        self.inputPathClean: str = fullPath

    def __init__(self, path: str, debug: bool = False):
        if(path == None):
            if(debug): print("FilePathObject: Argument path is None.")
            self.isFile = False
            return None

        if(not os.path.isfile(path)):
            if(debug): print("FilePathObject: Argument path is not a dir or file.")
            self.isFile = False
            return None

        _path = path.replace(r"\\\\|\/\/|\/|\\", os.path.sep)

        _fullPath = None
        _relativePath = None
        if(os.path.isabs(_path)):
            if(debug): print("FilePathObject: Argument path is absolute.")
            _fullPath = _path
            _relativePath = os.path.realpath(_fullPath)
        else:
            if(debug): print("FilePathObject: Argument path is relative.")
            _fullPath = os.path.abspath(_path)
            _relativePath = _path
        
        self.isFile: bool = True
        self.fullPath: str = _fullPath
        self.directory: str = os.path.split(_fullPath)[0]
        self.relativePath: str = _relativePath
        self.fileLeaf: str = os.path.split(self.directory)[-1]
        self.filename: str = os.path.basename(_fullPath)
        self.fileRoot: str = ".".join(self.filename.split(".")[:-1])
        self.extension: str =  _fullPath.split(".")[-1] if ("." in _fullPath) else ""
        self.extensionWithDot: str = f".{self.extension}"
        self.inputPath: str = path
        self.inputPathClean: str = _path

        if(debug): print("FilePathObject: No errors.")

    def help():
        """
        This function is a developer help-workaround and returns None.\n\n

        myObject = FilePathObject(filePath) returns an object with various strings for values in a file URI (more info in file).\n
        Given URI: C:\\users\\OddThinking\\Documents\\My Source\\Widget\\foo.src
        - isFile: bool = whether path leads to a recognized file. False whenever something goes wrong.
        - fullPath: str = "C:\\users\\OddThinking\\Documents\\My Source\\Widget\\"\n
        - directory: str = "C:\\users\\OddThinking\\Documents\\My Source\\Widget\\foo.src"\n
        - relativePath: str = relative path from current directory\n
        - fileLeaf: str = "Widget\\foo.src"\n
        - filename: str = "foo.src"\n
        - fileRoot: str = "foo"\n
        - extension: str = ".src"\n
        - extensionWithDot: str = "src"\n
        - inputPath: str = input of "path" argument\n
        - inputPathClean: str = input of "path" argument where separators like "/", "//", "\\\\" bas been replaces with system separator\n
        """

        return None


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