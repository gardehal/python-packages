import datetime

class DateTimeObject():
    defaultOffset = "02:00"
    def __init__(self, offset: str = defaultOffset):
        """
        Init a NOW/CURRENT TIME DateTimeObject with various fields for simpler handleing of time.
        
        Args:
            offset (str, optional): Time offset, hours of time from UTC.

        Returns:
            DateTimeObject: object with now, iso, isoAsNumber, isoWithMilli, isoWithMilliAsNumber
        """
        
        now = datetime.datetime.now()
        self.now = now
        self.iso = now.strftime("%Y-%m-%dT%H:%M:%S") + f"+{offset}" # https://en.wikipedia.org/wiki/ISO_8601
        self.isoAsNumber = now.strftime("%Y%m%d%H%M%S") + offset.replace(":", "")
        self.isoWithMilli = now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + f"+{offset}"
        self.isoWithMilliAsNumber = now.strftime("%Y%m%d%H%M%S%f")[:-3] # All but [0-9] removed
        
    def fromDatetime(self, customDatetime: datetime, offset: str = defaultOffset):
        """
        Init a DateTimeObject with various fields for simpler handleing of time.
        
        Args:
            customDatetime (datetime): datetime of time to set.
            offset (str, optional): Time offset, hours of time from UTC.

        Returns:
            DateTimeObject: object with now, iso, isoAsNumber, isoWithMilli, isoWithMilliAsNumber
        """
        
        self.now = customDatetime
        self.iso = customDatetime.strftime("%Y-%m-%dT%H:%M:%S") + f"+{offset}" # https://en.wikipedia.org/wiki/ISO_8601
        self.isoAsNumber = customDatetime.strftime("%Y%m%d%H%M%S") + offset.replace(":", "")
        self.isoWithMilli = customDatetime.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + f"+{offset}"
        self.isoWithMilliAsNumber = customDatetime.strftime("%Y%m%d%H%M%S%f")[:-3] # All but [0-9] removed
        
    def fromString(self, customDatetimeStr: str, offset: str = defaultOffset):
        """
        Init a DateTimeObject with various fields for simpler handleing of time.
        
        Args:
            customDatetime (str): str of time to set.
            offset (str, optional): Time offset, hours of time from UTC.

        Returns:
            DateTimeObject: object with now, iso, isoAsNumber, isoWithMilli, isoWithMilliAsNumber
        """
        
        _customDatetime = datetime.datetime.strptime(customDatetimeStr, "%Y-%m-%d %H:%M:%S")
        self.now = _customDatetime
        self.iso = _customDatetime.strftime("%Y-%m-%dT%H:%M:%S") + f"+{offset}" # https://en.wikipedia.org/wiki/ISO_8601
        self.isoAsNumber = _customDatetime.strftime("%Y%m%d%H%M%S") + offset.replace(":", "")
        self.isoWithMilli = _customDatetime.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + f"+{offset}"
        self.isoWithMilliAsNumber = _customDatetime.strftime("%Y%m%d%H%M%S%f")[:-3] # All but [0-9] removed