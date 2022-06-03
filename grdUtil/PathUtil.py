import os

# def __init__(self, isFile: bool = False, fullPath: str = "", directory: str = "", relativePath: str = "", fileLeaf: str = "", filename: str = "", fileRoot: str = "", extension: str = "", extensionWithDot: str = ""):
#     self.isFile: bool = isFile
#     self.fullPath: str = fullPath
#     self.directory: str = directory
#     self.relativePath: str = relativePath
#     self.fileLeaf: str = fileLeaf
#     self.filename: str = filename
#     self.fileRoot: str = fileRoot
#     self.extension: str = extension
#     self.extensionWithDot: str = extensionWithDot
#     self.inputPath: str = fullPath
#     self.inputPathClean: str = fullPath

# def __init__(self, filePath: str, debug: bool = False):
#     if(filePath == None):
#         if(debug): print("FilePathObject: Argument path is None.")
#         self.isFile = False
#         return None

#     if(not os.path.isfile(filePath)):
#         if(debug): print("FilePathObject: Argument path is not a dir or file.")
#         self.isFile = False
#         return None

#     sanitizedFilePath = filePath.replace(r"\\\\|\/\/|\/|\\", os.path.sep)

#     fullPath = None
#     relativePath = None
#     if(os.path.isabs(sanitizedFilePath)):
#         if(debug): print("FilePathObject: Argument path is absolute.")
#         fullPath = sanitizedFilePath
#         relativePath = os.path.realpath(fullPath)
#     else:
#         if(debug): print("FilePathObject: Argument path is relative.")
#         fullPath = os.path.abspath(sanitizedFilePath)
#         relativePath = sanitizedFilePath
    
#     self.isFile: bool = True
#     self.fullPath: str = fullPath
#     self.directory: str = os.path.split(fullPath)[0]
#     self.relativePath: str = relativePath
#     self.fileLeaf: str = os.path.split(self.directory)[-1]
#     self.filename: str = os.path.basename(fullPath)
#     self.fileRoot: str = ".".join(self.filename.split(".")[:-1])
#     self.extension: str =  fullPath.split(".")[-1] if ("." in fullPath) else ""
#     self.extensionWithDot: str = f".{self.extension}"
#     self.inputPath: str = sanitizedFilePath
#     self.inputPathClean: str = sanitizedFilePath

#     if(debug): print("FilePathObject: No errors.")

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