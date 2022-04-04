import uuid
from datetime import datetime


class BaseEntity():
    def __init__(self,
                 created: datetime = datetime.now(),
                 updated: datetime = datetime.now(),
                 deleted: datetime = None,
                 id: str = str(uuid.uuid4())):
        self.created: datetime = created
        self.updated: datetime = updated
        self.deleted: datetime = deleted
        self.id: str = id

    def summaryString(self):
        return "".join(map(str, ["ID: ", self.id]))

    def detailsString(self, includeId: bool = True, includeDatetime: bool = True, includeList: bool = True):
        idString = ", id: " + self.id if(includeId) else ""
        createdString = ", created: " + self.created if(includeDatetime) else ""
        updatedString = ", updated: " + self.updated if(includeDatetime) else ""
        deletedString = ", deleted: " + self.deleted if(includeDatetime) else ""
        
        return "".join(map(str, [createdString,
            updatedString,
            deletedString,
            idString]))
