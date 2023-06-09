import os
import re
from enum import Enum
from typing import List

import validators
from grdException.ArgumentException import ArgumentException

from .BashColor import BashColor
from .PrintUtil import printS
from .StrUtil import joinAsString


def extractArgs(currentArgsIndex: int, args: List[str], numbersOnly: bool = False, pathsOnly: bool = False, urlsOnly: bool = False, flagIndicator: str = "-") -> List[str]:
    """
    Extract non-flag arguments from array of args, options to only accept numbers, paths, urls.

    Args:
        currentArgsIndex (int): Index for argument args. Will only look in args after this index.
        args (List[str]): Arguments to sift though.
        numbersOnly (bool, optional): Only accept numbers? Defaults to False.
        pathsOnly (bool, optional): Only accept (file) paths? Defaults to False.
        urlsOnly (bool, optional): Only accept URLs? Defaults to False.
        flagIndicator (str, optional): Indicator for new arguments, eg. new set of arguments unrelated to argument args. Defaults to "-".

    Returns:
        List[str]: Arguments extracted.
    """
    
    result = []
    for arg in args[currentArgsIndex + 1:]:
        if(arg.startswith(flagIndicator)):
            break
        if(numbersOnly and not isNumber(arg)):
            printS("Argument ", arg, " is not a number.", color = BashColor.FAIL)
            continue
        if(pathsOnly and not os.path.exists(arg)):
            printS("Argument ", arg, " is not a file path.", color = BashColor.FAIL)
            continue
        if(urlsOnly and not validators.url(arg)):
            printS("Argument ", arg, " is not a url.", color = BashColor.FAIL)
            continue
        
        if(arg == "None" or arg == "Null"):
            arg = None

        result.append(arg)
    return result

def getIdsFromInput(args: List[str], existingIds: List[str], indexList: List[any], limit: int = None, returnOnNonIds: bool = False, setDefaultId: bool = True, startAtZero: bool = True, debug: bool = False) -> List[str]:
    """
    Get IDs from a List of inputs, whether they are raw IDs that must be checked via the database or indices (formatted "i[index]") of a List. 
    This defaults to the first element in existingIds if input is empty if setDefaultId is True.

    Args:
        args (List[str]): Args if IDs/indices.
        existingIds (List[str]): Existing IDs to compare with.
        indexList (List[any]): List of object (must have field "id") to index from.
        limit (int): Limit the numbers of arguments to parse.
        returnOnNonIds (bool): Return valid input IDs if the current input is no an ID, to allow input from user to be something like \"id id id bool\" which allows unspecified IDs before other arguments.
        setDefaultId (bool): Should a default ID be picked (first)?
        startAtZero (bool): Should indices start at zero? If False, first element in indexList will be i1, if True, it will be i0, etc.
        debug (bool): Should debug-information be printed?

    Returns:
        List[str]: List of existing IDs for input which can be found.
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
            if(not startAtZero):
                index = index - 1 if index > 0 else 0
                
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
                
                printS("Failed to add playList with ID \"", arg, "\", no such entity found in database.", color = BashColor.FAIL)
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

def getIfExists(array: List[any], index: int, default: any = None) -> any:
    """
    Get the element at index from array, if the length of the array is greater or equal to the index + 1.

    Args:
        array (List[any]): List to get from.
        index (int): Index to get.
        default (any, optional): Default value if item does not exist. Defaults to None.

    Returns:
        any: Index of List if exists, else default.
    """
    return array[index] if len(array) >= index + 1 else default

def sanitize(*args, mode: int = 1, subValue: str = "") -> str:
    """
    Sanitize a series of values and return them as a single string.
    Modes:
    0 - replace everything except latin alphanumerical symbols and space
    1 - replace everything except latin alphanumerical symbols, whitespace (\\s) 
    2 - replace everything except latin alphanumerical symbols, whitespace (\\s), and common symbols like < > , . _ - : ; * ^ ! " ' # % & /   (  ) [ ] = + ?
    3 - replace everything not allowed in Windows path names

    Args:
        args (*args): Any values to sanitize and return as string.
        mode (int, optional): Mode to use. Defaults to 1.
        subValue (str, optional): Value to replace bad characters with. Defaults to "".

    Returns:
        str: Concatenated, sanitized result.
    """
    
    okArgs = []
    try:
        for arg in args:
            joinAsString(arg) # TODO need a better check if arg is OK
            okArgs.append(arg)
    except Exception as e:
        printS(f"There was a character in this argument that could not be decoded: {e}", BashColor.ERROR)
    
    string = joinAsString(okArgs)
    if(mode == 0):
        return re.sub(r"""[^a-zA-Z0-9]""", subValue, string)
    elif(mode == 1):
        return re.sub(r"""[^a-zA-Z0-9\s]""", subValue, string)
    elif(mode == 2):
        return re.sub(r"""[^a-zA-Z0-9\s\<\>\,\.\_\-\:\;\*\^\!\"\'\#\%\&\/\\\(\)\[\]\=\+\?]""", subValue, string)
    elif(mode == 3):
        return re.sub(r"""[<>:"\/\|?*]""", subValue, string)
            
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

# Being moved to StrUtil...
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
        if(isinstance(a, List)):
            a = joinAsString(*a)
        
        result += str(a)
    
    return result
