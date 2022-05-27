from enum import IntEnum


class LogLevel(IntEnum):
    # Lower = log less
    NONE = 0
    CRITICAL = 100
    ERROR = 200
    WARNING = 300
    INFO = 400
    DEBUG = 500
    VERBOSE = 600
