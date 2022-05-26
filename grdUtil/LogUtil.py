
import inspect
from datetime import date, datetime, timezone
import os
import time

from .FileUtil import mkdir
from .JsonUtil import JsonUtil
from .LogLevel import LogLevel


class LogUtil():
    logDir: str
    debug: bool
    logLevel: LogLevel
    
    def __init__(self, logDir: str, debug: bool = True, logLevel: LogLevel = LogLevel.ERROR) -> None:
        """
        Initiate class for logging data to files named after date logged.

        Args:
            logDir (str): Path to directory for logs.
            debug (bool, optional): Should debug values be logged and printed? Defaults to True.
            logLevel (LogLevel, optional): Current LogLevel (e.g. level set by user). Defaults to LogLevel.ERROR.
        """
        self.logDir = logDir
        self.debug = debug
        self.logLevel = logLevel
        
        mkdir(logDir)
        
    def writeLog(self, text: str, fileExtension: str = ".md", logTitle: str = "LOGLEVEL\tDATETIME\tCALLING_FUNCTION\tMESSAGE") -> bool:
        """
        Write text to file in logDir.

        Args:
            text (str): Text to log.
            fileExtension (str): Extension of file. Defaults to .md.
            logTitle (str): Title that appears as the first line. Defaults to LOGLEVEL\tDATETIME\tCALLING_FUNCTION\tMESSAGE.

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
            return False
        
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
        
    def logAsJson(self, entity: any, logLevel: LogLevel = None, doPrint: bool = False) -> str:
        """
        Log argument object as JSON to file in path self.logDir.

        Args:
            entity (any): Object to log. Suggested to wrap your actual object in LogObject.
            logLevel (LogLevel, optional): LogLevel to log as. Defaults to None (will use self.logLevel).
            doPrint (bool, optional): Should log result be printed to print(). Defaults to False.

        Returns:
            str: Assembled string logged.
        """
        
        validLogLevel = self.validateLogLevel(logLevel)
        if(not self.shouldLog(validLogLevel)):
            return None
        
        log = JsonUtil.toDict(entity)
        logResult = self.writeLog(log)
        if(not logResult):
            return None
        
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
        logMessage = "".join([str(_) for _ in args])
        
        currentFrame = inspect.currentframe()
        callerFrame = inspect.getouterframes(currentFrame, 2)
        parentMethodName = callerFrame[1][3]
        
        log = "".join([level, "\t", now, "\t", parentMethodName, "\t", logMessage])
        logResult = self.writeLog(log)
        if(not logResult):
            return None
        
        return log
