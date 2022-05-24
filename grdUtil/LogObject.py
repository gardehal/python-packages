import datetime

from LogLevel import LogLevel

class LogObject():
    def __init__(self,
                 object: any = None,
                 logLevel: LogLevel = None,
                 logged: datetime = datetime.now()):
        self.object: any = object
        self.logLevel: LogLevel = logLevel
        self.logged: datetime = logged