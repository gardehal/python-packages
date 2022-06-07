import datetime

from DateTimeUtil import getDateTime
from LogLevel import LogLevel


class LogObject():
    def __init__(self,
                 object: any = None,
                 logLevel: LogLevel = None,
                 logged: datetime = getDateTime()):
        self.object: any = object
        self.logLevel: LogLevel = logLevel
        self.logged: datetime = logged
