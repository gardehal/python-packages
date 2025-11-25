import os
import re

class FilePathObject():
    exists: bool = False
    isFile: bool = False
    fullPath: str = None
    directory: str = None
    relativePath: str = None
    fileLeaf: str = None
    filename: str = None
    fileRoot: str = None
    extension: str = None
    extensionWithDot: str = None
    inputPath: str = None
    inputPathClean: str = None
    inputPathSplit: list[str] = None

    def __init__(self, filePath: str, debug: bool = False):
        """
        Initialize FilePathObject, assigning all the path items.
        See help() for more naming details.

        Args:
            filePath (str): path to file, absolute or relative, can be a non-existent file, but if exists, must be a file.
            debug (bool, optional): Print debug data. Defaults to False.

        Returns:
            FilePathObject: FilePathObject
        """
        
        if(filePath == None):
            if(debug): print("FilePathObject: Argument path is None.")
            return None

        if(os.path.exists(filePath)):
            self.exists = True

        if(self.exists and os.path.isfile(filePath)):
            self.isFile = True

        pathSplit = list(filter(None, re.split(r"\\?\\|\/?\/", filePath)))
        sanitizedFilePath = os.path.sep.join(pathSplit)

        fullPath = None
        directory = None
        filename = None
        relativePath = None
        if(self.exists):
            if(os.path.isabs(sanitizedFilePath)):
                fullPath = sanitizedFilePath
                relativePath = os.path.realpath(fullPath)
            else:
                fullPath = os.path.abspath(sanitizedFilePath)
                relativePath = sanitizedFilePath
                
            directory = os.path.dirname(fullPath)
            filename = os.path.basename(fullPath)
        else:
            directory = pathSplit[-2] if len(pathSplit) > 1 else None 
            fullPath = sanitizedFilePath
            filename = pathSplit[-1]
        
        fileRoot, extension = os.path.splitext(filename)
        
        self.fullPath = fullPath
        self.directory = directory
        self.relativePath = relativePath
        self.fileLeaf = os.path.sep.join([self.directory, filename]) if self.directory else None
        self.filename = filename
        self.fileRoot = fileRoot
        self.extension = extension if extension else None
        self.extensionWithDot = self.extension.removeprefix(".") if self.extension else None
        self.inputPath = filePath
        self.inputPathClean = sanitizedFilePath
        self.inputPathSplit = pathSplit

        if(debug): 
            print("FilePathObject: End.")
    
    def toString(self):
        """
        Get a string with all object values. Mainly for debugging.
        """

        return f"""{self}
exists {self.exists}
isFile {self.isFile}
fullPath {self.fullPath}
directory {self.directory}
relativePath {self.relativePath}
fileLeaf {self.fileLeaf}
filename {self.filename}
fileRoot {self.fileRoot}
extension {self.extension}
extensionWithDot {self.extensionWithDot}
inputPath {self.inputPath}
inputPathClean {self.inputPathClean}
inputPathSplit {self.inputPathSplit}"""

    def help(self):
        """
        This function is part of documentation and returns None.\n\n

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
        - inputPathClean: str = input of "path" argument where separators like "/", "//", "\\\\" bas been replaces with system separator
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