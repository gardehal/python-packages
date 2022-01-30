import re
import os
import validators

from myutil.PrintUtil import printS

def extractArgs(currentArgsIndex, args, numbersOnly = False, pathsOnly = False, urlsOnly = False, flagIndicator = "-"):
    """
    Extract non-flag arguments from array of args, options to only accept numbers, paths, urls.\n\n
    int currentArgsIndex
    array of strings args
    bool numbersOnly
    bool pathsOnly
    bool urlsOnly
    """
    _args = []
    for arg in args[currentArgsIndex + 1:]:
        if(arg.startswith(flagIndicator)):
            break
        if(numbersOnly and not isNumber(arg)):
            printS("Argument ", arg, " is not a number.")
            continue
        if(pathsOnly and not os.path.exists(arg)):
            printS("Argument ", arg, " is not a file path.")
            continue
        if(urlsOnly and not validators.url(arg)):
            printS("Argument ", arg, " is not a url.")
            continue

        _args.append(arg)
    return _args

# https://note.nkmk.me/en/python-check-int-float/
def isNumber(n, intOnly = False):
    """
    Try parse n as float or inter, return true/false.\n\n
    any n
    """
    try:
        float(n)
    except ValueError:
        return False
    else:
        if(intOnly):
            return float(n).is_integer
        else:
            return True

def getIfExists(array, index):
    """
    Get the element at index from array, if the length of the array is greater or equal to the index + 1.
    """
    return array[index] if len(array) >= index + 1 else None

def sanitize(*args, mode: int = 1) -> str:
    """
    Sanitize a series of values and return them as a single string.
    Modes:
    0 - replace everything except latin alphanumerical symbols and space
    1 - replace everything except latin alphanumerical symbols, whitespace (\\s) 
    2 - replace everything except latin alphanumerical symbols, whitespace (\\s), and common symbols like < > , . _ - : ; * ^ ! " ' # % & /   (  ) [ ] = + ?
    TODO - replace commonly known escape characters
    TODO - replace only worst of escape charaters

    Args:
        args (*args): any values to sanitize and return as string
        mode (int, optional): Mode to use. Defaults to 0.

    Returns:
        str: concatinated, sanitized result
    """
    
    _result = ""
    for element in args:
        _element = str(element)
        
        if(mode == 0):
            _result += re.sub("[^a-zA-Z0-9]", "", _element)
        if(mode == 1):
            _result += re.sub("[^a-zA-Z0-9\s]", "", _element)
        if(mode == 2):
            _result += re.sub("[^a-zA-Z0-9\s\<\>\,\.\_\-\:\;\*\^\!\"\'\#\%\&\/\\\(\)\[\]\=\+\?]", "", _element)
            
    return _result
