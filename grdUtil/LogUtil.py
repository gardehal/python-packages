
from .LogLevel import LogLevel


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
        
    def logAsJson(self, object: any, logLevel: LogLevel = self.logLevel, doPrint: bool = False) -> str:
        """
        Log argument object as JSON to file in path self.logPath.

        Args:
            object (any): Object to log. Suggested to wrap your actual object in LogObject.
            logLevel (LogLevel, optional): LogLevel to log as. Defaults to self.logLevel.
            doPrint (bool, optional): Should log result be printed to print(). Defaults to False.

        Returns:
            str: Assembled string logged.
        """
        return None

    def logAsText(self, *args: any, logLevel: LogLevel = self.logLevel, doPrint: bool = False) -> str:
        """
        Log arguments arg to file in path self.logPath.

        Args:
            *args (any): Object to log. These will be concat to a string.
            logLevel (LogLevel, optional): LogLevel to log as. Defaults to self.logLevel.
            doPrint (bool, optional): Should log result be printed to print(). Defaults to False.

        Returns:
            str: Assembled string logged.
        """
        return None
