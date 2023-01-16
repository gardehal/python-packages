import enum
import json
from typing import List, TypeVar, _GenericAlias

T = TypeVar("T")

def toDict(obj: object) -> dict:
    """
    Converts objects to dictionaries.
    
    Source: https://www.codegrepper.com/code-examples/whatever/python+nested+object+to+dict

    Args:
        obj (object): Object to convert.

    Returns:
        dict: Dictionary of input object.
    """
    
    if(obj == None or not hasattr(obj, "__dict__")):
        return obj
    
    result = {}
    for key, val in obj.__dict__.items():
        if(key.startswith("_")):
            continue
        
        element = []
        if(isinstance(val, _GenericAlias)): # E.g. List[str]
            element = []
        elif(isinstance(val, List)):
            for item in val:
                element.append(toDict(item))
        elif(isinstance(val, enum.Enum)):
            element = val.value
        else:
            element = toDict(val)
            
        result[key] = element
        
    return result

def toJson(obj: object) -> str:
    """
    Converts objects to JSON though dictionaries.

    Args:
        obj (object): Object to convert.

    Returns:
        str: JSON string.
    """
    
    dict = toDict(obj)
    return json.dumps(dict, default = str)

def writeToJsonFile(filepath: str, obj: object) -> bool:
    """
    Writes object obj to a JSON format in file from filepath.

    Args:
        filepath (str): Path to file to store JSON in.
        obj (object): Object to save.

    Returns:
        bool: Result.
    """
    
    asDict = toDict(obj)
    with open(filepath, "w") as file:
        json.dump(asDict, file, indent = 4, default = str)
        
    return True

def readJsonFile(filepath: str, typeT: T) -> T:
    """
    Opens and reads a JSON formatted file, returning object of type T.

    Args:
        filepath (str): Path to file to read JSON from.
        typeT (T): Type to convert to.

    Returns:
        T: T of object if any, else None.
    """
    
    fileContent = open(filepath, "r").read()
    if(len(fileContent) < 2):
        return None
    else:
        return fromJson(fileContent, typeT)

def fromJson(jsonStr: str, typeT: T) -> T:
    """
    Converts JSON to an object T.

    Args:
        str (str): String to convert.
        typeT (T): Type to convert to.

    Returns:
        T: T of object from JSON.
    """
    # https://pynative.com/python-serialize-datetime-into-json/ ?
    
    jsonDict = json.loads(jsonStr)
    asObj = typeT(**jsonDict)

    for fieldName in dir(asObj):
        # Skip default fields and functions
        if(fieldName.startswith('__') or callable(getattr(asObj, fieldName))):
            continue

        field = getattr(asObj, fieldName)
        fieldType = type(field)

        if("uuid" in str(fieldType) or "datetime" in str(fieldType)):
            continue

    return asObj
