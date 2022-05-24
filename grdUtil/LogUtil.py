
import inspect

from .BashColor import BashColor
from .LogLevel import LogLevel
from .PrintUtil import printS


class LogUtil():
    logPath: str
    debug: bool
    logLevel: LogLevel
    
    def __init__(self, logPath: str, debug: bool = True, logLevel: LogLevel = LogLevel.INFO) -> None:
        self.logPath = logPath
        self.debug = debug
        self.logLevel = logLevel
        
    def shouldLog(self, logLevel: LogLevel) -> bool:
        """
        Should items be logged/printed based on log level.

        Args:
            logLevel (LogLevel): current LogLevel.

        Returns:
            bool: items should be logged and printed
        """
        
        return logLevel > self.logLevel
        
    def printS(self, *args, color: BashColor = None, doPrint: bool = True) -> None:
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
        
        return printS(*args, color = color, doPrint = doPrint)
        
    def printD(self, *args, color: BashColor = BashColor.WARNING, debug: bool = True) -> None:
        """
        Concats all arguments and prints them as string (delim not included) in a DEBUG format.
        
        Format: "DEBUG: MethodName - Message."

        Args:
            color (BashColor, optional): Color from colors-dictionary. Defaults to None (normal color).
            doPrint (bool, optional): Should text be printed, useful for debug messages. Defaults to True.
        """
        
        # It loglevel not matched
        # if(???):
        #     return None
        
        currentFrame = inspect.currentframe()
        callerFrame = inspect.getouterframes(currentFrame, 2)
        parentMethodName = callerFrame[1][3]
        
        return printS("DEBUG: ", parentMethodName, " - ", *args, color = color, doPrint = debug)
        
    def logToJson(self, toLog: str, logLevel: LogLevel, doPrint: bool = False) -> bool:
        """
        Log a string to a file as JSON.
        """
        return True

    def logToFile(self, toLog: any, logLevel: LogLevel, doPrint: bool = False) -> bool:
        """
        Log a string to a file as plain text.
        """
        return True
