import os
import re
from typing import List

import validators

from grdUtil.BashColor import BashColor
from grdUtil.PrintUtil import printS


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

def getIdsFromInput(input: List[str], existingIds: List[str], indexList: List[any], limit: int = None, returnOnNonIds: bool = False, debug: bool = False) -> List[str]:
    """
    Get IDs from a list of inputs, whether they are raw IDs that must be checked via the database or indices (formatted "i[index]") of a list. This defaults to the first element in existingIds if input is empty.

    Args:
        input (List[str]): input if IDs/indices
        existingIds (List[str]): existing IDs to compare with
        indexList (List[any]): List of object (must have field "id") to index from
        limit (int): limit the numbers of arguments to parse
        returnOnNonIds (bool): return valid input IDs if the current input is no an ID, to allow input from user to be something like \"id id id bool\" which allows unspecified IDs before other arguments
        debug (bool): should debug-information be printed

    Returns:
        List[str]: List of existing IDs for input which can be found
    """
    
    if(len(existingIds) == 0 or len(indexList) == 0):
        printS("DEBUG: getIdsFromInput - Length of input \"existingIds\" (", len(existingIds), ") or \"indexList\" (", len(indexList), ") was 0.", color = BashColor.WARNING, doPrint = debug)
        return []

    _result = []
    
    if(len(input) == 0):
        _result.append(existingIds[0])
        return _result

    for i, _string in enumerate(input):
        if(limit != None and i >= limit):
            printS("DEBUG: getIdsFromInput - Returning data before input ", _string, ", limit (", limit, ") reached.", color = BashColor.WARNING, doPrint = debug)
            break
        
        if(_string[0] == "i"):  # Starts with "i", like index of "i2" is 2, "i123" is 123 etc.
            if(not isNumber(_string[1:])):
                if(returnOnNonIds):
                    return _result
                
                printS("Argument ", _string, " is not a valid index format, must be \"i\" followed by an integer, like \"i0\". Argument not processed.", color = BashColor.FAIL)
                continue

            _index = int(float(_string[1:]))
            _indexedEntity = indexList[_index]

            if(_indexedEntity != None):
                _result.append(_indexedEntity.id)
            else:
                if(returnOnNonIds):
                    return _result
                
                printS("Failed to get data for index ", _index, ", it is out of bounds.", color = BashColor.FAIL)
        else:  # Assume input is ID if it's not, users problem. Could also check if ID in getAllIds()
            if(_string in existingIds):
                _result.append(_string)
            else:
                if(returnOnNonIds):
                    return _result
                
                printS("Failed to add playlist with ID \"", _string, "\", no such entity found in database.", color = BashColor.FAIL)
                continue

    return _result

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
