import sys
import os
import threading
import time

from myutil.ShellType import ShellType
from myutil.BashColor import BashColor
from myutil.ShellUtil import *

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

def wrapColor(text: str, color: BashColor, overrideColor: str = None) -> str:
    """
    NB: Will not work in non-compatible terminals like Windows CMD. If this is detected, this will return the text without color.
    Wraps text in ASCI colours for terminal usage.
    See colours in BashColor class, argument accepts ANCI code like "\\x1b[0;34;42m".

    Args:
        text (str): text to wrap
        color (BashColor): color to use
        overrideColor (str): a string with the color to use, custom set, like "\\x1b[0;34;42m"

    Returns:
        str: input text wrapped in the ASCII colours
    """
    
    if(getCurrentShellType() != ShellType.BASH):
        return text
    
    _color = color
    if(str(overrideColor[0]) == "\x1b"):
        _color = color

    return _color + str(text) + BashColor.ENDC

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

def printSpinner(pause: float = 0.2) -> None:
    """
    Print one rotation of a spinner to inform the user that the program is working. This method must be constantly called to keep the spinner going.
    
    Args:
        pause (float): Pause between between change in the spinner
    """
    
    print(" - ", end = "\r")
    sys.stdout.flush()
    time.sleep(pause)
    print(" \\ ", end = "\r")
    sys.stdout.flush()
    time.sleep(pause)
    print(" | ", end = "\r")
    sys.stdout.flush()
    time.sleep(pause)
    print(" / ", end = "\r")
    sys.stdout.flush()
    time.sleep(pause)

def printProgressBar(current: float, total: float, barLength: int = 20) -> None:
    """
    Print a progress bar.
    Source: https://stackoverflow.com/questions/6169217/replace-console-output-in-python

    Args:
        current (float): Current progress status
        total (float): Total progress goal
        barLength (int, optional): Total displayed length. Defaults to 20.
    """
    
    percent = float(current) * 100 / total
    arrow   = "-" * int(percent/100 * barLength - 1) + ">"
    spaces  = " " * (barLength - len(arrow))

    print(f"Progress: [{arrow}{spaces}] {int(percent)}%", end = "\r")
    sys.stdout.flush()
    
def printFinishedProgressBar(barLength: int = 20) -> None:
    """
    Print a finished progress bar for display purposes.
    Source: https://stackoverflow.com/questions/6169217/replace-console-output-in-python

    Args:
        barLength (int, optional): Total displayed length. Defaults to 20.
    """
    
    printProgressBar(100, 100, barLength)

def runFunctionWithSpinner(function: any, arguments: tuple[()]) -> None:
    """
    Run a function and display a spinner in the CLI.
    E.g.: asyncResult = runFunctionWithSpinner(function = countSeconds, arguments = (10, "Count seconds completed!"))

    Args:
        function (method): [description]
        arguments (tuple[): [description]
    """
    
    funcThread = threading.Thread(target = function, args = arguments)
    funcThread.start()
    
    while funcThread.is_alive():
        printSpinner()