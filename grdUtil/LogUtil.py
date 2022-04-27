
from BashColor import BashColor
from build.lib.grdUtil.PrintUtil import printS
from grdUtil.ShellUtil import *
from LogLevel import LogLevel

class FileLogger():
    logPath: str
    debug: bool
    logLevel: LogLevel
    
    def __init__(self, logPath: str, debug: bool = True, logLevel: LogLevel = LogLevel.INFO) -> None:
        self.logPath = logPath
        self.debug = debug
        self.logLevel = logLevel
        
    def printS(*args, color: BashColor = None, doPrint: bool = True) -> None:
        """
        Concats all arguments and prints them as string (delim not included).

        Args:
            args (any): Items to print.
            color (BashColor, optional): Color from colors-dictionary. Defaults to None (normal color).
            doPrint (bool, optional): Should text be printed, useful for debug messages. Defaults to True.
        """
        
        # It loglevel not matched
        # if(???): 
        #     return None
        
        return printS(args, color = color, doPrint = doPrint)
        
    def printD(*args, color: BashColor = BashColor.WARNING, debug: bool = True) -> None:
        """
        Concats all arguments and prints them as string (delim not included) in a DEBUG format.

        Args:
            color (BashColor, optional): Color from colors-dictionary. Defaults to None (normal color).
            doPrint (bool, optional): Should text be printed, useful for debug messages. Defaults to True.
        """
        
        # It loglevel not matched
        # if(???):
        #     return None
        
        # TODO get method name of caller
        return printS("DEBUG: ", args, color = color, doPrint = debug)
        
    def logToJson(toLog: str, logLevel: LogLevel, doPrint: bool = False) -> bool:
        """
        Log a string to a file as JSON.
        """
        return True

    def logToFile(toLog: any, logLevel: LogLevel, doPrint: bool = False) -> bool:
        """
        Log a string to a file as plain text.
        """
        return True
