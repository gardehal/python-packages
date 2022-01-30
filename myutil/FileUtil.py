import os

from myutil.PrintUtil import *

def mkdir(dirPath):
    """
    Make directories if none exist. Recursive, will create all parent folders in path.
    """
    os.makedirs(dirPath, exist_ok=True)

def makeFiles(*args) -> bool:
    """
    Create local files used for storing settings, video ques, sources etc.

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
            printS("There was a temporary error creating file ", filepath, ".", color = BashColors.ERROR)
            continue

        file = open(filepath, "a")
        file.close()
    
    return True