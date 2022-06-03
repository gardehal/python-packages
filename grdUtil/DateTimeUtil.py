from datetime import datetime, timezone
import re
    
def getDateTime(asUtc: bool = True) -> datetime:
    """
    Get datetime as ISO format, with option to get as UTC.

    Args:
        asUtc (bool, optional): Get as UTC? Defaults to True.

    Returns:
        datetime: Result.
    """
    
    if(asUtc):
        return datetime.utcnow().replace(tzinfo = timezone.utc).isoformat()
    
    return datetime.now().isoformat()

def getDateTimeAsNumber(asUtc: bool = True) -> int:
    """
    Get numbers only from datetime as ISO format, with option to get as UTC.

    Args:
        asUtc (bool, optional): Get as UTC? Defaults to True.

    Returns:
        int: Result.
    """
    
    return int(re.sub("[^0-9]", "", str(getDateTime(asUtc))))

def stringToDatetime(toConvert: str, format: str = "%Y-%m-%d %H:%M:%S.%f") -> datetime:
    """
    Parses string to datetime.

    Args:
        toConvert (str): String of date or time or datetime to convert.
        format (str, optional): DateTime format to use. Defaults to %Y-%m-%d %H:%M:%S.%f e.g. 2020-12-31 23:59:59.999999, same format as datetime.now().

    Returns:
        datetime: Datetime result.
    """
    
    return datetime.strptime(toConvert, format)

def datetimeToString(toConvert: datetime, format: str = "%Y-%m-%d %H:%M:%S.%f") -> str:
    """
    Parses datetime to string.

    Args:
        toConvert (datetime): String of date or time or datetime to convert.
        format (str, optional): DateTime format to use. Defaults to %Y-%m-%d %H:%M:%S.%f e.g. 2020-12-31 23:59:59.999999, same format as datetime.now().

    Returns:
        datetime: Datetime result.
    """
    
    return toConvert.strftime(format)
