import os
import uuid
from datetime import datetime
from typing import List

from dotenv import load_dotenv
from grdUtil.BashColor import BashColor
from grdUtil.LocalJsonRepository import LocalJsonRepository
from grdUtil.PrintUtil import printS

load_dotenv()
# DEBUG = eval(os.environ.get("DEBUG"))
# LOCAL_STORAGE_PATH = os.environ.get("LOCAL_STORAGE_PATH")
DEBUG = False
LOCAL_STORAGE_PATH = "."

T = Example

class ExampleService():
    """
        Service for Example, with basic CRUD.
    """
    
    storagePath: str = LOCAL_STORAGE_PATH
    exampleRepository: LocalJsonRepository = None

    def __init__(self):
        self.exampleRepository: LocalJsonRepository = LocalJsonRepository(T, DEBUG, os.path.join(self.storagePath, "Example"))

    def add(self, example: T) -> T:
        """
        Add a new Example.

        Args:
            Example (Example): Example to add

        Returns:
            Example | None: returns Example if success, else None
        """

        entity = example
        entity.updated = datetime.now()
        entity.id = str(uuid.uuid4())
        
        result = self.exampleRepository.add(entity)
        if(result):
            return entity
        else:
            return None

    def get(self, id: str, includeSoftDeleted: bool = False) -> T:
        """
        Get Example by ID.

        Args:
            id (str): ID of Example to get
            includeSoftDeleted (bool): should include soft-deleted entities

        Returns:
            Example: Example if any, else None
        """

        entity = self.exampleRepository.get(id)
        
        if(entity != None and entity.deleted != None and not includeSoftDeleted):
            printS("DEBUG: get - Example with ID ", entity.id, " was soft deleted.", color = BashColor.WARNING, doPrint = DEBUG)
            return None
        else:
            return entity

    def getAll(self, includeSoftDeleted: bool = False) -> List[T]:
        """
        Get all Examples.

        Args:
            includeSoftDeleted (bool): should include soft-deleted entities

        Returns:
            List[Example]: list of Examples
        """

        entities = self.exampleRepository.getAll()
        result = []
        
        for entity in entities:
            if(entity.deleted != None and not includeSoftDeleted):
                printS("DEBUG: getAll - Example with ID ", entity.id, " was soft deleted.", color = BashColor.WARNING, doPrint = DEBUG)
            else:
                result.append(entity)
            
        return result
        
    def getAllIds(self, includeSoftDeleted: bool = False) -> List[str]:
        """
        Get all IDs of Examples.

        Args:
            includeSoftDeleted (bool): should include soft-deleted entities

        Returns:
            List[Example]: list of soft deleted Examples
        """
        
        entities = self.getAll(includeSoftDeleted)
        return [example for example in entities]
        
    def getAllSoftDeleted(self) -> List[T]:
        """
        Get all soft deleted Examples.

        Returns:
            List[str]: Examples IDs if any, else empty list
        """
        
        entities = self.getAll()
        result = []
        
        for entity in entities:
            if(entity.deleted != None):
                result.append(entity)
            
        return result

    def update(self, example: T) -> T:
        """
        Update Example.

        Args:
            Example (Example): Example to update

        Returns:
            Example | None: returns Example if success, else None
        """

        entity = example
        entity.updated = datetime.now()
        result = self.exampleRepository.update(entity)
        if(result):
            return entity
        else:
            return None

    def delete(self, id: str) -> T:
        """
        (Soft) Delete a Example.

        Args:
            id (str): ID of Example to delete

        Returns:
            Example | None: returns Example if success, else None
        """

        entity = self.get(id)
        if(entity == None):
            return None

        entity.deleted = datetime.now()
        result = self.update(entity)
        if(result):
            return entity
        else:
            return None
        
    def restore(self, id: str) -> T:
        """
        Restore a (soft) deleted Example.

        Args:
            id (str): ID of Example to restore

        Returns:
            Example | None: returns Example if success, else None
        """

        entity = self.get(id, includeSoftDeleted = True)
        if(entity == None):
            return None

        entity.deleted = None
        result = self.update(entity)
        if(result):
            return entity
        else:
            return None
        
    def remove(self, id: str, includeSoftDeleted: bool = False) -> T:
        """
        Permanently remove a Example.

        Args:
            id (str): ID of Example to remove
            includeSoftDeleted (bool): should include soft-deleted entities

        Returns:
            Example | None: returns Example if success, else None
        """

        entity = self.get(id, includeSoftDeleted)
        if(entity == None):
            return None
        
        result = self.exampleRepository.remove(entity.id)
        if(result):
            return entity
        else:
            return None

    def addOrUpdate(self, example: T) -> T:
        """
        Add Example if none exists, else update existing.

        Args:
            example (Example): Example to add or update

        Returns:
            Example | None: returns Example if success, else None
        """

        if(self.get(example.id) == None):
            return self.add(example)

        return self.update(example)
    