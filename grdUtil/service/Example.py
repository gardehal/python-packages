import uuid
from datetime import datetime


class Example():
    def __init__(self,
                 otherValues: str = None,
                 created: datetime = None,
                 updated: datetime = None,
                 deleted: datetime = None,
                 id: str = str(uuid.uuid4())):
        self.otherValues: str = otherValues
        self.created: datetime = created
        self.updated: datetime = updated
        self.deleted: datetime = deleted
        self.id: str = id

    def summaryString(self):
        return "".join(map(str, ["otherValues: ", self.otherValues, 
            ", id: ", self.id]))

    def detailsString(self, includeId: bool = True, includeDatetime: bool = True, includeListCount: bool = True):
        createdString = ", created: " + self.created if(includeDatetime) else ""
        updatedString = ", updated: " + self.updated if(includeDatetime) else ""
        deletedString = ", deleted: " + self.deleted if(includeDatetime) else ""
        idString = ", id: " + self.id if(includeId) else ""
        
        return "".join(map(str, ["otherValues: ", self.otherValues,
            createdString,
            updatedString,
            deletedString,
            idString]))
