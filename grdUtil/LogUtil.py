
import inspect
import os
import time
from datetime import date, datetime, timezone

from grdException.ArgumentException import ArgumentException
from grdException.WriteFileException import WriteFileException

from .FileUtil import mkdir
from .InputUtil import getEnumFromValueName
from .JsonUtil import toDict
from .LogLevel import LogLevel
from .PrintUtil import printS, printStack


class LogUtil():
    logDir: str
    debug: bool
    logLevel: LogLevel
    
    def __init__(self, logDir: str, debug: bool = True, logLevel: LogLevel = LogLevel.ERROR, logLevelString: str = None) -> None:
        """
        Initiate class for logging data to files named after date logged.

        Args:
            logDir (str): Path to directory for logs.
            debug (bool, optional): Should debug values be logged and printed? Defaults to True.
            logLevel (LogLevel, optional): Current LogLevel (e.g. setting set by user). Defaults to LogLevel.ERROR.
            logLevelString (str, optional): Current LogLevel as string (e.g. setting set by user). Defaults to ERROR.
        """
        
        if(logLevel == None and logLevelFromString == None):
            raise ArgumentException(f"__init__ - Arguments logLevel OR logLevelString must be set.")
        
        self.logDir = logDir
        self.debug = debug
        self.logLevel = logLevel
        
        if(logLevelString != None):
            logLevelFromString = getEnumFromValueName(LogLevel, logLevelString.upper())
            if(logLevelFromString != None):
                self.logLevel = logLevelFromString
            else:
                raise ArgumentException(f"__init__ - Argument logLevelString {logLevelString} was not a valid LogLevel value. Must be the name of any enum in LogLevel.")
        
        mkdir(logDir)
        
    def shouldLog(self, logLevel: LogLevel) -> bool:
        """
        Should items be logged/printed based on log level.

        Args:
            logLevel (LogLevel): Current LogLevel.

        Returns:
            bool: Items should be logged and printed.
        """
        
        return logLevel.value >= self.logLevel.value
        
    def validateLogLevel(self, logLevel: LogLevel) -> LogLevel:
        """
        Validate LogLevel from nullable args, returns self.logLevel if None.

        Args:
            logLevel (LogLevel): LogLevel to validate.

        Returns:
            LogLevel: Valid LogLevel.
        """
        
        return logLevel if(logLevel != None) else self.logLevel
        
    def logAsJson(self, object: any, logLevel: LogLevel = None, doPrint: bool = False) -> str:
        """
        Log argument object as JSON to file in path self.logDir.

        Args:
            object (any): Object to log. It is suggested to wrap your actual object in LogObject.
            logLevel (LogLevel, optional): LogLevel to log as. Defaults to None (will use self.logLevel).
            doPrint (bool, optional): Should log result be printed to print(). Defaults to False.

        Returns:
            str: Assembled string logged.
        """
        
        validLogLevel = self.validateLogLevel(logLevel)
        if(not self.shouldLog(validLogLevel)):
            return None
        
        # if(type(object) == LogLevel):
            # set datetime and loglevel fields
        
        log = toDict(object)
        logResult = self.writeJsonLog(log)
        if(not logResult):
            return None
        
        if(doPrint):
            printS(log)
            
        return log

    def logAsText(self, *args: any, logLevel: LogLevel = None, doPrint: bool = False) -> str:
        """
        Log arguments arg to file in path self.logDir.
        
        Format: LOGLEVEL    DATETIME    CALLING_FUNCTION    MESSAGE

        Args:
            *args (any): Data to log. These will be concat to a string.
            logLevel (LogLevel, optional): LogLevel to log as. Defaults to None (will use self.logLevel).
            doPrint (bool, optional): Should log result be printed to print(). Defaults to False.

        Returns:
            str: Assembled string logged.
        """
        
        validLogLevel = self.validateLogLevel(logLevel)
        if(not self.shouldLog(validLogLevel)):
            return None
        
        level = str(validLogLevel.name)
        now = datetime.utcnow().replace(tzinfo = timezone.utc).isoformat()
        caller = inspect.getframeinfo(inspect.stack()[1][0])
        logMessage = "".join([str(_) for _ in args])
        
        log = "".join([level, "\t", now, "\t", caller.filename, ":", str(caller.lineno), "\t", logMessage])
        logResult = self.writeTextLog(log)
        if(not logResult):
            # self.logAsText(args, logLevel = logLevel, doPrint = doPrint)
            return None
        
        if(doPrint):
            printS(log)
        
        return log
        
    def writeJsonLog(self, object: any, fileExtension: str = ".md", logTitle: str = "LOGLEVEL\tDATETIME\tCALLER\tMESSAGE") -> bool:
        """
        Log arguments object as JSON to file in path self.logDir.

        Args:
            object (any): JSON object to log.
            fileExtension (str): Extension of file. Defaults to .md.
            logTitle (str): Title that appears as the first line. Defaults to LOGLEVEL\tDATETIME\tCALLER\tMESSAGE.

        Returns:
            bool: Result of write.
        """
        
        dateNow = date.fromtimestamp(time.time()).isoformat()
        logFileName = "".join([dateNow, fileExtension])
        logPath = os.path.join(self.logDir, logFileName)
        
        if(not os.path.isfile(logPath)):
            file = open(logPath, "a")
            file.write(logTitle)
            file.close()
            
        try:
            file = open(logPath, "a")
            # dump, append as JSON list
            file.close()
            return True
        except:
            printStack(doPrint = self.debug)
            raise WriteFileException(f"Failed to write to file {logPath}.")
        
        return False
        
    def writeTextLog(self, text: str, fileExtension: str = ".md", logTitle: str = "LOGLEVEL\tDATETIME\tCALLER\tMESSAGE") -> bool:
        """
        Write text to file in logDir.

        Args:
            text (str): Text to log.
            fileExtension (str): Extension of file. Defaults to .md.
            logTitle (str): Title that appears as the first line. Defaults to LOGLEVEL\tDATETIME\tCALLER\tMESSAGE.

        Returns:
            bool: Result of write.
        """
        
        dateNow = date.fromtimestamp(time.time()).isoformat()
        logFileName = "".join([dateNow, fileExtension])
        logPath = os.path.join(self.logDir, logFileName)
        
        if(not os.path.isfile(logPath)):
            file = open(logPath, "a")
            file.write(logTitle)
            file.close()
            
        try:
            file = open(logPath, "a")
            file.write("".join(["\n", text]))
            file.close()
            return True
        except:
            printStack(doPrint = self.debug)
            raise WriteFileException(f"Failed to write to file {logPath}.")
        
        return False
