import os
import sys
import threading
import time
from typing import List
from grdExceptions.ArgumentException import ArgumentException

from grdUtil.BashColor import BashColor
from grdUtil.ShellType import ShellType
from grdUtil.ShellUtil import *


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
    
    _color = color.value
    if(overrideColor != None and str(overrideColor[0]) == "\x1b"):
        _color = color

    return _color + str(text) + BashColor.ENDC.value

def asTableRow(dataArray: List[str], templateRow: List[str] = [], minColWidth: int = 6, delim: str = " | ", edgeDelim: bool = True) -> str:
    """
    Returns a string row of values as a row in tables, using labels to make the cell width.
    
    Args:
        dataArray (List[List[str]]): 1D List of data to put in row.
        templateRow (List[str], optional): 1D List used as template for width of columns. Defaults to [].
        minColWidth (int, optional): Mimimum column width. Defaults to 6.
        delim (str, optional): Deliminator or columns. Defaults to " | ".
        edgeDelim (bool, optional): Should include startin deliminator? Defaults to False.

    Returns:
        str: dataArray as a row
    """
    
    if(not isinstance(dataArray, List)):
        raise ArgumentException("asTableRow - argument dataArray was not a valid list of list of strings.")
    if(not isinstance(templateRow, List)):
        raise ArgumentException("asTableRow - argument templateRow was not a valid list of strings.")

    row = delim if edgeDelim else ""
    for i, data in enumerate(dataArray):
        data = str(data)
        label = templateRow[i] if len(templateRow) >= i + 1 else None
        _minColWidth = minColWidth
        if(len(templateRow) > 0 and len(str(label)) > 0):
            _minColWidth = len(str(label)) if len(str(label)) > minColWidth else minColWidth

        spacePadding = " " * (_minColWidth - len(str(data)))
        value = data if(data != None, len(data) > 0) else ""
        row += str(value).replace("\n", "") + spacePadding + delim
        
    return row

def getRowSpacer(templateRow: List[str], corner: str = " + ", edgeDelim: bool = True) -> str:
    """
    Returns a string row of values as a row in tables, using labels to make the cell width.
    
    Args:
        templateRow (List[str]): 1D List used as template for width of columns.
        corner (str, optional): Corner symbol of a cell. Defaults to " + ".
        edgeDelim (bool, optional): Should include startin deliminator? Defaults to False.

    Returns:
        str: row spacer
    """
    
    if(not isinstance(templateRow, List)):
        raise ArgumentException("getRowSpacer - argument templateRow was not a valid list of strings.")

    row = corner if edgeDelim else ""
    for i, template in enumerate(templateRow):
        row += ("-" * len(template)) + "\n"
        
    row += corner if edgeDelim else ""
    return row

# TODO sep. method for table by columns

def asTable(dataArray: List[List[str]], labels: List[str], minColWidth: int = 6, delim: str = " | ", 
            edgeDelim: bool = True, includeRowDividers: bool = False, alternateRowColor: BashColor = BashColor.NONE) -> str:
    """
    Returns a string formatted as a table.

    Args:
        dataArray (List[List[str]]): sD List of Lists of data to put in table.
        labels (List[str], optional): 1D List of labels per column, also used as template for width of columns.
        minColWidth (int, optional): Mimimum column width. Defaults to 6.
        delim (str, optional): Deliminator or columns. Defaults to " | ".
        edgeDelim (bool, optional): Should include start and end deliminator? Defaults to False.
        includeRowDividers(bool, optional): Should string include dividers between each row? Defaults to False.
        alternateRowColor(bool, optional): BashColor to use on alternate rows. Defaults to BashColor.NONE.

    Returns:
        str: dataArray and labels as a table
    """
    
    if(not isinstance(dataArray, List) or not isinstance(dataArray[0], List)):
        raise ArgumentException("asTable - argument dataArray was not a valid list of list of strings.")
    if(not isinstance(labels, List)):
        raise ArgumentException("asTable - argument labels was not a valid list of strings.")

    tableString = ""
    if(labels != None and len(labels) > 0):
        labelRow = asTableRow(labels, labels, minColWidth, delim, edgeDelim)
        tableString += labelRow + "\n"
        tableString += ("-" * len(labelRow)) + "\n"
        
    for i, data in enumerate(dataArray):
        line = asTableRow(data, labels, minColWidth, delim, edgeDelim) + "\n"
        tableString += line if i % 2 != 0 else wrapColor(line, color = alternateRowColor)
        
    return tableString 

def printLists(data: List[List[str]], titles: List[str]) -> bool:
    """
    Prints all lists in data, with title before corresponding list.

    Args:
        data (List[List[str]]): List if Lists to print
        titles (List[str]): List of titles, index 0 is title for data List index 0 etc.

    Returns:
        bool: true = success
    """
    
    for i, dataList in enumerate(data):
        printS("\n", titles[i], color = BashColor.BOLD)
        printS("No data.", color = BashColor.WARNING, doPrint = len(dataList) == 0) 
        
        for j, entry in enumerate(dataList):
            _color = "WHITE" if j % 2 == 0 else "GREYBG"
            printS(entry, color = BashColor[_color]) 
            
    return True

def printSpinner(pause: float = 0.2) -> None:
    """
    Print one rotation of a spinner to inform the user that the program is working. This method must be constantly called to keep the spinner going.
    
    Args:
        pause (float): Pause between between change in the spinner in seconds
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
