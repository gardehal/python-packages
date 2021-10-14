import datetime

class DateTimeObject():
    def __init__(self, offset = "02:00"):
        now = datetime.datetime.now()
        self.now = now
        self.iso = now.strftime("%Y-%m-%dT%H:%M:%S") + f"+{offset}" # https://en.wikipedia.org/wiki/ISO_8601
        self.isoAsNumber = now.strftime("%Y%m%d%H%M%S") + offset.replace(":", "") # All but [0-9] removed
        self.isoWithMilli = now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + f"+{offset}"
        self.isoWithMilliAsNumber = now.strftime("%Y%m%d%H%M%S%f")[:-3] # All but [0-9] removed