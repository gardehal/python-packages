import os

from .BashColor import BashColor
from .PrintUtil import printS


def mkdir(dirPath) -> None:
    """
    Make directories, given a path that does not exist, that path and parent directories will be created.

    Args:
        dirPath (str): path of directories
    """
    
    os.makedirs(dirPath, exist_ok = True)

def makeFiles(*args) -> bool:
    """
    Create local files given by list of args.

    Args:
        args (list): paths+filenames to create

    Returns:
        bool: success = true
    """

    for filepath in args:
        try:
            if(not os.path.exists(os.path.dirname(filepath))):
                os.makedirs(os.path.dirname(filepath))
        except OSError as exc: # Guard against race condition
            printS("There was a temporary error creating file ", filepath, ".", color = BashColor.ERROR)
            continue

        file = open(filepath, "a")
        file.close()
    
    return True
