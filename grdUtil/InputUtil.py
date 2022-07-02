import os
import re
from enum import Enum

import validators
from grdException.ArgumentException import ArgumentException

from .BashColor import BashColor
from .PrintUtil import printS


def extractArgs(currentArgsIndex: int, args: list[str], numbersOnly: bool = False, pathsOnly: bool = False, urlsOnly: bool = False, flagIndicator: str = "-") -> list[str]:
    """
    Extract non-flag arguments from array of args, options to only accept numbers, paths, urls.

    Args:
        currentArgsIndex (int): Index for argument args. Will only look in args after this index.
        args (list[str]): Arguments to sift though.
        numbersOnly (bool, optional): Only accept numbers? Defaults to False.
        pathsOnly (bool, optional): Only accept (file) paths? Defaults to False.
        urlsOnly (bool, optional): Only accept URLs? Defaults to False.
        flagIndicator (str, optional): Indicator for new arguments, eg. new set of arguments unrelated to argument args. Defaults to "-".

    Returns:
        list[str]: Arguments extracted.
    """
    
    result = []
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

        result.append(arg)
    return result

def getIdsFromInput(args: list[str], existingIds: list[str], indexList: list[any], limit: int = None, returnOnNonIds: bool = False, setDefaultId: bool = True, debug: bool = False) -> list[str]:
    """
    Get IDs from a list of inputs, whether they are raw IDs that must be checked via the database or indices (formatted "i[index]") of a list. 
    This defaults to the first element in existingIds if input is empty if setDefaultId is True.

    Args:
        args (List[str]): Args if IDs/indices.
        existingIds (List[str]): Existing IDs to compare with.
        indexList (List[any]): List of object (must have field "id") to index from.
        limit (int): Limit the numbers of arguments to parse.
        returnOnNonIds (bool): Return valid input IDs if the current input is no an ID, to allow input from user to be something like \"id id id bool\" which allows unspecified IDs before other arguments.
        setDefaultId (bool): Should a default ID be picked (first)?
        debug (bool): Should debug-information be printed?

    Returns:
        list[str]: List of existing IDs for input which can be found.
    """
    
    if(len(existingIds) == 0 or len(indexList) == 0):
        printS("DEBUG: getIdsFromInput - Length of input \"existingIds\" (", len(existingIds), ") or \"indexList\" (", len(indexList), ") was 0.", color = BashColor.WARNING, doPrint = debug)
        return []

    result = []
    
    if(setDefaultId and len(args) == 0):
        result.append(existingIds[0])
        return result

    for i, arg in enumerate(args):
        if(limit != None and i >= limit):
            printS("DEBUG: getIdsFromInput - Returning data before input ", arg, ", limit (", limit, ") reached.", color = BashColor.WARNING, doPrint = debug)
            break
        
        if(arg[0] == "i"):  # Starts with "i", like index of "i2" is 2, "i123" is 123 etc.
            if(not isNumber(arg[1:])):
                if(returnOnNonIds):
                    return result
                
                printS("Argument ", arg, " is not a valid index format, must be \"i\" followed by an integer, like \"i0\". Argument not processed.", color = BashColor.FAIL)
                continue

            index = int(float(arg[1:]))
            indexedEntity = getIfExists(indexList, index)

            if(indexedEntity != None):
                result.append(indexedEntity.id)
            else:
                if(returnOnNonIds):
                    return result
                
                printS("Failed to get data for index ", index, ", it is out of bounds.", color = BashColor.FAIL)
        else:  # Assume args is ID if it's not, users problem. Could also check if ID in getAllIds()
            if(arg in existingIds):
                result.append(arg)
            else:
                if(returnOnNonIds):
                    return result
                
                printS("Failed to add playlist with ID \"", arg, "\", no such entity found in database.", color = BashColor.FAIL)
                continue

    return result

# https://note.nkmk.me/en/python-check-int-float/
def isNumber(n: any, intOnly: bool = False) -> bool:
    """
    Try parse n as float or inter, return true/false.

    Args:
        n (any): Value to check.
        intOnly (bool, optional): Should number be validated as an integer? Defaults to False.

    Returns:
        bool: Result.
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

def getIfExists(array: list[any], index: int, default: any = None) -> any:
    """
    Get the element at index from array, if the length of the array is greater or equal to the index + 1.

    Args:
        array (list[any]): List to get from.
        index (int): Index to get.
        default (any, optional): Default value if item does not exist. Defaults to None.

    Returns:
        any: Index of list if exists, else default.
    """
    return array[index] if len(array) >= index + 1 else default

def sanitize(*args, mode: int = 1) -> str:
    """
    Sanitize a series of values and return them as a single string.
    Modes:
    0 - replace everything except latin alphanumerical symbols and space
    1 - replace everything except latin alphanumerical symbols, whitespace (\\s) 
    2 - replace everything except latin alphanumerical symbols, whitespace (\\s), and common symbols like < > , . _ - : ; * ^ ! " ' # % & /   (  ) [ ] = + ?
    TODO - replace commonly known escape characters
    TODO - replace only worst of escape characters

    Args:
        args (*args): Any values to sanitize and return as string.
        mode (int, optional): Mode to use. Defaults to 1.

    Returns:
        str: Concatenated, sanitized result.
    """
    
    string = joinAsString(*args)
    if(mode == 0):
        return re.sub("[^a-zA-Z0-9]", "", string)
    if(mode == 1):
        return re.sub("[^a-zA-Z0-9\s]", "", string)
    if(mode == 2):
        return re.sub("[^a-zA-Z0-9\s\<\>\,\.\_\-\:\;\*\^\!\"\'\#\%\&\/\\\(\)\[\]\=\+\?]", "", string)
            
    return string

def getEnumFromValueName(enumType: Enum, valueName: str) -> Enum:
    """
    Convert the value name as string to a corresponding Enum for argument enumType.
    Not ideal to use generic Enum instead of something like a generic type T, but it works.
    
    Inspired by: https://stackoverflow.com/a/56567247

    Args:
        enumType (Enum): Enum to convert to.
        valueName (str): String of value name to get from argument enumType. Case sensitive.

    Raises:
        ArgumentException: valueName not found in enumType.

    Returns:
        Enum: The entry of enumType with the value valueName.
    """
    
    for k, v in enumType.__members__.items():
        if(k == valueName):
            return v
    else:
        raise ArgumentException(f"{valueName} is not a valid {enumType.__name__} option.")

def joinAsString(*args) -> str:
    """
    Join all args as string and return the resulting single string.
    
    Args:
        args (*args): Any values to stringify.

    Returns:
        str: Joined string of all args.
    """

    result = ""
    for a in args:
        print(a)
        if(isinstance(a, list)):
            a = joinAsString(*a)
        
        print(a)
        result += str(a)
    
    return result