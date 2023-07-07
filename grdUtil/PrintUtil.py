import inspect
import os
import sys
import threading
import time
import traceback
from typing import Iterable, List

from grdException.ArgumentException import ArgumentException

from .BashColor import BashColor
from .ShellType import ShellType
from .ShellUtil import getCurrentShellType


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

def printS(*args: any, color: BashColor = None, doPrint: bool = True, enableStyle: bool = True, end: str = "\n") -> None:
    """
    Concat all arguments and prints them as string (delim not included).

    Args:
        args (any): Items to print.
        color (BashColor, optional): Color from colors-dictionary. Defaults to None (no color).
        doPrint (bool, optional): Should text be printed, useful for debug messages. Defaults to True.
        enableStyle (bool, optional): Should style (coloured text, background colours etc.). Defaults to True.
    """
    
    if(not doPrint):
        return None
    
    message = "".join([str(m) for m in args])
    if(color and enableStyle):
        message = wrapColor(message, color)

    print(message, end = end)
    sys.stdout.flush()
    return None
        
def printD(*args, color: BashColor = BashColor.WARNING, debug: bool = True, enableStyle: bool = True) -> None:
    """
    Concat all arguments and prints them as string (delim not included) in a DEBUG format.
    
    Format: "DEBUG: MethodName - My Message."

    Args:
        color (BashColor, optional): Color from colors-dictionary. Defaults to None (no color).
        doPrint (bool, optional): Should text be printed, useful for debug messages. Defaults to True.
        enableStyle (bool, optional): Should style (coloured text, background colours etc.). Defaults to True.
    """
    
    currentFrame = inspect.currentframe()
    callerFrame = inspect.getouterframes(currentFrame, 2)
    parentMethodName = callerFrame[1][3]
    
    return printS("DEBUG: ", parentMethodName, " - ", *args, color = color, doPrint = debug, enableStyle = enableStyle)

def wrapColor(text: str, color: BashColor, overrideColor: str = None) -> str:
    """
    NB: Will not work in non-compatible terminals like Windows CMD. If this is detected, this will return the text without color.
    Wraps text in ASCI colours for terminal usage.
    See colours in BashColor class, argument accepts ANCI code like "\\x1b[0;34;42m".

    Args:
        text (str): Text to wrap.
        color (BashColor): Color to use.
        overrideColor (str): A string with the color to use, custom set, like "\\x1b[0;34;42m".

    Returns:
        str: Input text wrapped in the ASCII colors.
    """
    
    if(getCurrentShellType() != ShellType.BASH):
        return text
    
    color = color.value
    if(overrideColor != None and str(overrideColor[0]) == "\x1b"):
        color = color

    return color + str(text) + BashColor.ENDC.value

def getMaxColumWidth(dataArray: List[List[str]], labels: List[str], paddingSpace: int = 2) -> List[int]:
    """
    Get maximum width of a colum given a 2D array.

    Args:
        dataArray (List[List[str]]): 2D List of Lists of data to put in table.
        labels (List[str]): 1D List of labels.
        paddingSpace (int): Length of padding space to take into account, eg. "foo" = 0, " bar " = 2.

    Returns:
        List[int]: Widths of the widest strings per column.
    """
    
    if(not isinstance(dataArray, List) or not isinstance(dataArray[0], List)):
        raise ArgumentException("getMaxColumWidth - argument templateRow was not a valid List of strings.")
    if(not isinstance(labels, List)):
        raise ArgumentException("getMaxColumWidth - argument labels was not a valid List of strings.")
    if(len(labels) != len(dataArray[0])):
        raise ArgumentException("getMaxColumWidth - argument labels and dataArray[0] (and other instances in dataArray?) does not match in length.")
    
    result = []
    for label in labels:
        result.append(len(str(label)) + paddingSpace)
        
    for row in dataArray:
        for i, data in enumerate(row):
            updated = len(str(data)) + paddingSpace
            if(updated > result[i]):
                result[i] = updated
                
    return result
    
def getRowSpacer(templateArray: List[int], corner: str = "+", spacer: str = "-", edgeDelim: bool = True) -> str:
    """
    Returns a string row of values as a row in tables, using labels to make the cell width.
    
    Args:
        templateArray (List[int]): List used as template for width of columns.
        corner (str, optional): Corner symbol of a cell. Defaults to "+".
        spacer (str, optional): Main symbol of the spacer. Defaults to "-".
        edgeDelim (bool, optional): Should include starting deliminator? Defaults to False.

    Returns:
        str: Row spacer.
    """

    row = corner if edgeDelim else ""
    for i, width in enumerate(templateArray):
        row += (spacer * width)
        row += corner if(i + 1 < len(templateArray)) else ""
        
    row += corner if edgeDelim else ""
    return row

def asTableRow(dataArray: List[str], templateArray: List[int], delim: str = " | ", edgeDelim: bool = True) -> str:
    """
    Returns a string row of values as a row in tables, using labels to make the cell width.
    
    Args:
        dataArray (List[List[str]]): 1D List of data to put in row.
        templateArray (List[int]): List used as template for width of columns.
        delim (str, optional): Deliminator or columns. Defaults to " | ".
        edgeDelim (bool, optional): Should include starting deliminator? Defaults to False.

    Returns:
        str: dataArray as a row.
    """
    
    row = delim if edgeDelim else ""
    for i, data in enumerate(dataArray):
        data = str(data).replace("\n", "")
        spacePaddingBefore = " "
        spacePaddingAfter = " " * (templateArray[i] - len(data) - 1)
        value = data if(data != None, len(data) > 0) else ""
        row += spacePaddingBefore + value + spacePaddingAfter
        row += delim if(i + 1 < len(templateArray)) else ""
        
    row += delim if edgeDelim else ""
    return row

def asTable(dataArray: List[List[str]], labels: List[str], delim: str = "|",
            edgeDelim: bool = True, includeRowDividers: bool = False, alternateRowColor: BashColor = BashColor.NONE) -> str:
    """
    Returns a string formatted as a table.

    Args:
        dataArray (List[List[str]]): 2D List of Lists of rows to put in table.
        labels (List[str], optional): 1D List of labels per column, also used as template for width of columns.
        minColWidth (int, optional): Minimum column width. Defaults to 6.
        delim (str, optional): Deliminator or columns. Defaults to " | ".
        edgeDelim (bool, optional): Should include start and end deliminator? Defaults to False.
        includeRowDividers(bool, optional): Should string include dividers between each row? Defaults to False.
        alternateRowColor(bool, optional): BashColor to use on alternate rows. Defaults to BashColor.NONE.

    Returns:
        str: dataArray and labels as a table.
    """
    
    if(not isinstance(dataArray, List) or not isinstance(dataArray[0], List)):
        raise ArgumentException("asTable - argument dataArray was not a valid List of List of strings.")
    if(not isinstance(labels, List)):
        raise ArgumentException("asTable - argument labels was not a valid List of strings.")

    template = getMaxColumWidth(dataArray, labels)
    rowSpacer = getRowSpacer(template)
    tableString = ""
    
    # Label row
    labelRow = asTableRow(labels, template, delim, edgeDelim)
    tableString += (rowSpacer + "\n") if includeRowDividers else ""
    tableString += labelRow + "\n"
    tableString += rowSpacer + "\n"
    
    # Data rows
    for i, data in enumerate(dataArray):
        line = asTableRow(data, template, delim, edgeDelim) + "\n"
        tableString += line if i % 2 != 0 else wrapColor(line, color = alternateRowColor)
        tableString += (rowSpacer + "\n") if includeRowDividers else ""
        
    return tableString

def printLists(data: List[List[str]], titles: List[str]) -> bool:
    """
    Prints all Lists in data, with title before corresponding List.

    Args:
        data (List[List[str]]): List if Lists to print
        titles (List[str]): List of titles, index 0 is title for data List index 0 etc.

    Returns:
        bool: Result.
    """
    
    for i, dataList in enumerate(data):
        printS("\n", titles[i], color = BashColor.BOLD)
        printS("No data.", color = BashColor.WARNING, doPrint = len(dataList) == 0) 
        
        for j, entry in enumerate(dataList):
            _color = "WHITE" if j % 2 == 0 else "GREYBG"
            printS(entry, color = BashColor[_color]) 
            
    return True

def printSpinner(pause: float = 0.2, color: BashColor = None) -> None:
    """
    Print one rotation of a spinner to inform the user that the program is working. This method must be constantly called to keep the spinner going.
    
    Args:
        pause (float): Pause between between change in the spinner in seconds
    """
    
    # TODO will complete one rotation every time called, should be some abort or return callback to stop spinning when async task finishes
    printS(" - ", color = color, end = "\r")
    time.sleep(pause)
    printS(" \\ ", color = color, end = "\r")
    time.sleep(pause)
    printS(" | ", color = color, end = "\r")
    time.sleep(pause)
    printS(" / ", color = color, end = "\r")
    time.sleep(pause)

def printProgressText(text: str, pause: float = 0.5, color: BashColor = None) -> None:
    """
    Print one rotation of a spinner to inform the user that the program is working. This method must be constantly called to keep the spinner going.
    
    Args:
        pause (float): Pause between between change in the spinner in seconds
    """
    
    printS(text, color = color, end = "\r")
    time.sleep(pause)
    printS(text, ".", color = color, end = "\r")
    time.sleep(pause)
    printS(text, "..", color = color, end = "\r")
    time.sleep(pause)
    printS(text, "...", color = color, end = "\r")
    time.sleep(pause)

def printProgressBar(current: float, total: float, barLength: int = 20, color: BashColor = None) -> None:
    """
    Print a progress bar.
    Source: https://stackoverflow.com/questions/6169217/replace-console-output-in-python

    Args:
        current (float): Current progress status.
        total (float): Total progress goal.
        barLength (int, optional): Total displayed length. Defaults to 20.
    """
    
    percent = float(current) * 100 / total
    arrow   = "-" * int(percent / 100 * barLength - 1) + ">"
    spaces  = " " * (barLength - len(arrow))

    printS(f"Progress: [{arrow}{spaces}] {int(percent)}%", color = color, end = "\r")
    
def printFinishedProgressBar(barLength: int = 20, color: BashColor = None) -> None:
    """
    Print a finished progress bar for display purposes.
    Source: https://stackoverflow.com/questions/6169217/replace-console-output-in-python

    Args:
        barLength (int, optional): Total displayed length. Defaults to 20.
    """
    
    printProgressBar(100, 100, barLength, color)

def runFunctionWithSpinner(function: any, arguments: Iterable[any], color: BashColor = None) -> None:
    """
    Run a function and display a spinner in the CLI.
    E.g.: asyncResult = runFunctionWithSpinner(function = countSeconds, arguments = [10, "Count seconds completed!"]).

    Args:
        function (any): Function to run.
        arguments (Iterable[any]): Iterable of arguments to pass to function, positional.
    """
    
    funcThread = threading.Thread(target = function, args = arguments)
    funcThread.start()
    
    while funcThread.is_alive():
        printSpinner(color = color)
        
    printS("   ")

def printStack(color: BashColor = BashColor.WARNING, doPrint: bool = True) -> None:
    """
    Prints traceback.format_exec() in a wrapper. Used to print error inside try/except except. 
    If used outside an except block, it will print "NoneType = None\n\n".

    Args:
        color (BashColor): BashColor to use for print. Default BashColor.WARNING.
        doPrint (bool): Should print? E.g. if debug == True. Default True.
    """
    
    printS(traceback.format_exc(), color = color, doPrint = doPrint)
