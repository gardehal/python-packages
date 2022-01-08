import re
import sys
import os
import requests
import time
import validators
from enum import Enum
from furl import furl

def disablePrint():
    """
    Disable usage of print().
    """
    sys.stdout = open(os.devnull, 'w')

def enablePrint():
    """
    Restore usage of print().
    """
    sys.stdout = sys.__stdout__

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

def printS(*args, color = None, doPrint: bool = True) -> None:
    """
    Concats all arguments and prints them as string (delim not included).

    Args:
        color ([type], optional): Color from colors-dictionary. Defaults to None (normal color).
        doPrint (bool, optional): Should text be printed, useful for debug messages. Defaults to True.
    """
    
    if(not doPrint):
        return None
    
    _message = ""
    for _element in args:
        _message += str(_element)

    if(color):
        _message = wrapColor(_message, color)

    print(_message)
    return None

def wrapColor(text, color):
    """
    Wraps text in ASCI colours for terminal usage.
    see colours in Util.colors for simple selection, argument accepts ANCI code like "\\x1b[0;34;42m".
        See Util project Main class' printAllColours function for most or all styles.
    string text
    string/int color
    """
    colorArg = ""

    if(isNumber(str(color))):
        colorList = list(colors)
        if(int(color) < 0 or int(color) > len(colorList) - 1):
            return "Color index out of range (0 - " + str(len(colorList) - 1) + ")"

        colorArg = colors[colorList[int(color)]]
    elif(str(color[0]) == "\x1b"):
        colorArg = color
    else:
        colorArg = colors[str(color).upper()]

    return colorArg + str(text) + colors["ENDC"]

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

def asTableRow(dataArray, labels = None, minColWidth = 6, delim = " | ", startingDelim = False):
    """
    Returns a string row of values as a row in tables.\n\n

    Array of any dataArray (1D)
    Array of any labels (1D)
    int minColWidth
    string delim
    bool startingDelim
    """

    row = delim if startingDelim else ""
    for i in range(0, len(dataArray)):
        _minColWidth = minColWidth
        if(len(labels) > 0 and len(labels[i]) > 0):
            _minColWidth = len(str(labels[i])) if len(str(labels[i])) > minColWidth else minColWidth

        spacePadding = " " * (_minColWidth - len(str(dataArray[i])))
        row += str(dataArray[i]).replace("\n", "") + spacePadding + delim
        
    return row

def asTable(dataArray, labels = None, minColWidth = 6, delim = " | ", startingDelim = False):
    """
    Returns a string formatted as a table.\n\n

    Array of any dataArray (2D)
    Array of any labels (1D)
    int minColWidth
    string delim
    bool startingDelim
    """

    tableString = ""
    if(len(labels) > 0):
        labelRow = asTableRow(labels, labels, minColWidth, delim, startingDelim)
        tableString += labelRow + "\n"
        tableString += ("-" * len(labelRow)) + "\n"
        
    for i in range(0, len(dataArray)):
        line = asTableRow(dataArray[i], labels, minColWidth, delim, startingDelim) + "\n"
        tableString += line if i % 2 != 0 else wrapColor(line, "gray")
        
    return tableString 

def requestCallByUrl(url, verb, body = None, headers = None, retries = 4, timeout = 4, stream = False):
    """
    Make an request (module) call to {url}, using verb. Format params, header, and body like params = {"key1": "value1", "key2": "value2"}, 
    or body as just value. Retries default 4 times, waiting default 4 seconds after fail.
    """

    f = furl(url)
    return requestCall(f.origin, f.path, verb, params = f.query.params, body = body, headers = headers, retries = retries, timeout = timeout, stream = stream)

def requestCall(baseUrl, endpoint, verb, params = None, body = None, headers = None, retries = 4, timeout = 4, stream = False):
    """
    Make an request (module) call to {baseUrl}{endpoint}, using verb. Format params, header, and body like params = {"key1": "value1", "key2": "value2"}, 
    or body as just value. Retries default 4 times, waiting default 4 seconds after fail.
    """

    print(f"Making a web request to {baseUrl}{endpoint}...")

    response = None
    for i in range(retries):
        if(verb == HttpVerb.GET):
            response = requests.get(f"{baseUrl}{endpoint}", params = params, data = body, headers = headers, stream = stream)
        if(verb == HttpVerb.POST):
            response = requests.post(f"{baseUrl}{endpoint}", params = params, data = body, headers = headers, stream = stream)

        if(response.status_code >= 200 and response.status_code < 300):
            return response
        elif(response.status_code == 408 or response.status_code == 503):
            print(f"Request to {baseUrl}{endpoint} failed with code: {response.status_code}. Codes 408 and 503 are common for websites warming up. Retrying...")
            time.sleep(timeout)
        else:
            print(f"Request to {baseUrl}{endpoint} failed with code: {response.status_code}.")
            return response

    print(f"Web request to {baseUrl}{endpoint} failed all {retries} retries, after a minimum of {retries * timeout} seconds...")
    return response        

def arrayContains(arrayA, arrayB):
    """
    Return true if any element in arrayA a can be found in array arrayB, else false.
    """

    for a in arrayA:
        for b in arrayB:
            if(a == b):
                return True

    return False

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
            printS("There was a temporary error creating file ", filepath, ".", color=colors["ERROR"])
            continue

        file = open(filepath, "a")
        file.close()
    
    return True

def printSpinner():
    """
    Displays a small spinner.
    """
    
    print("spinner")

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
    
# https://stackoverflow.com/questions/287871/how-to-print-colored-text-to-the-terminal?rq=1
colors = {
    "": "",
    "GREY": "\x1b[1;30;40m",
    "HEADER": "\x1b[95m",
    "OKBLUE": "\x1b[94m",
    "OKGREEN": "\x1b[92m",
    "WARNING": "\x1b[93m",
    "FAIL": "\x1b[91m",
    "ERROR": "\x1b[91m",
    "ENDC": "\x1b[0m",
    
    "BOLD": "\x1b[1m",
    "ITALIC": "\x1b[3m",
    "URL": "\x1b[4m",
    "BLINK": "\x1b[5m",
    "BLINK2": "\x1b[6m",
    "SELECTED": "\x1b[7m",
    
    "BLACK": "\x1b[30m",
    "RED": "\x1b[31m",
    "GREEN": "\x1b[32m",
    "YELLOW": "\x1b[33m",
    "BLUE": "\x1b[34m",
    "VIOLET": "\x1b[35m",
    "TEAL": "\x1b[36m",
    "WHITE": "\x1b[37m",
    
    "BLACKBG": "\x1b[40m",
    "REDBG": "\x1b[41m",
    "GREENBG": "\x1b[42m",
    "YELLOWBG": "\x1b[43m",
    "BLUEBG": "\x1b[44m",
    "VIOLETBG": "\x1b[45m",
    "TEALBG": "\x1b[46m",
    "WHITEBG": "\x1b[47m",
    "GREYBG": "\x1b[100m"
}

class HttpVerb(Enum):
    GET = 0
    POST = 1
    PUT = 2
    PATCH = 3
    DELETE = 4