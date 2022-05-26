
from datetime import datetime
from .FileUtil import mkdir

from .LogLevel import LogLevel
from .JsonUtil import toDict


class LogUtil():
    logDir: str
    debug: bool
    logLevel: LogLevel
    
    def __init__(self, logDir: str, debug: bool = True, logLevel: LogLevel = LogLevel.ERROR) -> None:
        """
        Init class for logging data to files named after date logged.

        Args:
            logDir (str): Path to directory for logs.
            debug (bool, optional): Should debug values be logged and printed? Defaults to True.
            logLevel (LogLevel, optional): Current LogLevel (e.g. level set by user). Defaults to LogLevel.ERROR.
        """
        self.logDir = logDir
        self.debug = debug
        self.logLevel = logLevel
        
        mkdir(logDir)
        
    def writeLog(self, text: str) -> bool:
        """
        Write text to file in logDir.

        Args:
            text (str): Text to log.

        Returns:
            bool: Result of write.
        """
        
        try:
            # TODO
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
        
        return logLevel > self.logLevel
        
    def validateLogLevel(self, logLevel: LogLevel) -> LogLevel:
        """
        Validate LogLevel from nullable args, returns self.logLevel if None.

        Args:
            logLevel (LogLevel): LogLevel to validate.

        Returns:
            LogLevel: Valid LogLevel.
        """
        
        return logLevel > self.logLevel
        
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
        
        log = toDict(entity)
        logResult = self.writeLog(log)
        if(not logResult):
            return None
        
        return log

    def logAsText(self, *args: any, logLevel: LogLevel = None, doPrint: bool = False) -> str:
        """
        Log arguments arg to file in path self.logDir.

        Args:
            *args (any): Object to log. These will be concat to a string.
            logLevel (LogLevel, optional): LogLevel to log as. Defaults to None (will use self.logLevel).
            doPrint (bool, optional): Should log result be printed to print(). Defaults to False.

        Returns:
            str: Assembled string logged.
        """
        
        validLogLevel = self.validateLogLevel(logLevel)
        if(not self.shouldLog(validLogLevel)):
            return None
        
        level = str(validLogLevel.value)
        now = str(datetime.now)
        logMessage = [str(_) for _ in args]
        # LOGLEVEL  DATETIME    MESSAGE
        log = "".join(level, "\t", now, "\t", logMessage)
        logResult = self.writeLog(log)
        if(not logResult):
            return None
        
        return log
