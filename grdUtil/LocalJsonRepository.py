import glob
import json
import os
from typing import List, Generic, TypeVar

from .FileUtil import mkdir
from .JsonUtil import fromJson, toDict
from .PrintUtil import printD, printStack

T = TypeVar("T")

class LocalJsonRepository(Generic[T]):
    debug: bool = False
    storagePath: str = "."

    def __init__(self,
                 typeT: type,
                 debug: bool = False,
                 storagePath: str = "."):
        self.typeT: type = typeT
        self.debug: bool = debug
        self.storagePath: str = storagePath

        mkdir(storagePath)

    def add(self, entity: T) -> bool:
        """
        Add a new entity using local JSON files for storage.

        Args:
            entity (T): Entity to add.

        Returns:
            bool: Result.
        """

        entityExists = self.exists(entity.id)
        if(entityExists):
            printD("Error adding ", entity.id, ", ID already exists", debug = self.debug)
            return False

        try:
            newEntityDict = toDict(entity)
            fileName = "".join([entity.id, ".json"])
            filePath = os.path.join(self.storagePath, fileName)
            with open(filePath, "a") as file:
                json.dump(newEntityDict, file, indent=4, default=str)

            return True
        except Exception:
            printStack(doPrint = self.debug)
            return False

    def exists(self, id: str) -> bool:
        """
        Check if entity exists by ID.

        Args:
            id (str): ID of entity to check.

        Returns:
            bool: Exists.
        """

        try:
            filename = "".join([id, ".json"])
            return os.path.isfile(os.path.join(self.storagePath, filename))
        except Exception:
            printStack(doPrint = self.debug)
            return False

    def get(self, id: str) -> T:
        """
        Get entity using local JSON files for storage.

        Args:
            id (str): ID of entity to get.

        Returns:
            T: Entity if any, else None.
        """

        try:
            fileName = "".join([id, ".json"])
            filePath = os.path.join(self.storagePath, fileName)
            if(not os.path.isfile(filePath)):
                return None

            fileContent = None
            with open(filePath, "r") as file:
                fileContent = file.read()
            
            if(len(fileContent) < 2):
                return None
            else:
                return fromJson(fileContent, self.typeT)
        except Exception:
            printStack(doPrint = self.debug)
            return None

    def getAll(self) -> List[T]:
        """
        Get all entities using local JSON files for storage.

        Returns:
            List[T]: Entities if any, else empty list.
        """

        try:
            all = []
            globPath = glob.glob(f"{self.storagePath}/*.json")
            for filePath in globPath:
                fileContent = None
                with open(filePath, "r") as file:
                    fileContent = file.read()

                if(len(fileContent) > 2):
                    all.append(fromJson(fileContent, self.typeT))
            
            return all
        except Exception:
            printStack(doPrint = self.debug)
            return List[T]

    def update(self, entity: T) -> bool:
        """
        Update entity using local JSON files for storage.

        Args:
            entity (T): Entity to update.

        Returns:
            bool: Result.
        """

        entityExists = self.exists(entity.id)
        if(not entityExists):
            printD("Error updating ", entity.id, ", entity does not exist.", debug = self.debug)
            return False

        try:
            updatedEntityDict = toDict(entity)
            fileName = "".join([entity.id, ".json"])
            filePath = os.path.join(self.storagePath, fileName)
            with open(filePath, "w") as file: # w truncates
                json.dump(updatedEntityDict, file, indent=4, default=str)
            
            return True
        except Exception:
            printStack(doPrint = self.debug)
            return False

    def remove(self, id: str) -> bool:
        """
        Remove entity using local JSON files for storage.

        Args:
            id (str): ID of entity to remove.

        Returns:
            bool: Result.
        """

        entityExists = self.exists(id)
        if(not entityExists):
            printD("Error removing ", id, ", entity does not exist", debug = self.debug)
            return False

        try:
            fileName = "".join([id, ".json"])
            path = os.path.join(self.storagePath, fileName)
            os.remove(path)
            
            return True
        except Exception:
            printStack(doPrint = self.debug)
            return False
