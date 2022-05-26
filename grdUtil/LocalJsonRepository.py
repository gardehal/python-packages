import glob
import os
import sys
from typing import Generic, List, TypeVar

from .BashColor import BashColor
from .FileUtil import mkdir
from .JsonUtil import fromJson, toDict
from .PrintUtil import printS, printStack

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
            entity (T): entity to add

        Returns:
            bool: success = True
        """

        _entity = self.get(entity.id)
        if(_entity != None):
            if(self.debug): printS("Error adding ", entity.id, ", ID already exists", color = BashColor.FAIL)
            return False

        try:
            _newEntityDict = toDict(entity)
            _filename = entity.id + ".json"
            _path = os.path.join(self.storagePath, _filename)
            with open(_path, "a") as file:
                json.dump(_newEntityDict, file, indent=4, default=str)

            return True
        except Exception:
            if(self.debug): printS(sys.exc_info(), color = BashColor.WARNING)
            printS("Error adding ", entity.id, color = BashColor.FAIL)
            return False

    def exists(self, id: str) -> bool:
        """
        Check if entity exists by ID.

        Args:
            id (str): id of entity to get

        Returns:
            bool: exists
        """

        try:
            filename = "".join(id, ".json")
            return os.path.isfile(os.path.join(self.storagePath, filename))
        except Exception:
            printStack(doPrint = self.debug)
            return False

    def get(self, id: str) -> T:
        """
        Get entity using local JSON files for storage.

        Args:
            id (str): id of entity to get

        Returns:
            T: entity if any, else None
        """

        try:
            _filename = id + ".json"
            _path = os.path.join(self.storagePath, _filename)
            if(not os.path.isfile(_path)):
                return None

            _fileContent = None
            with open(_path, "r") as file:
                _fileContent = file.read()
            
            if(len(_fileContent) < 2):
                return None
            else:
                return fromJson(_fileContent, self.typeT)
        except Exception:
            if(self.debug): printS(sys.exc_info(), color = BashColor.WARNING)
            printS("Error getting", color = BashColor.FAIL)
            return None

    def getAll(self) -> List[T]:
        """
        Get all entities using local JSON files for storage.

        Returns:
            List[T]: entities if any, else empty list
        """

        try:
            _all = []
            _globPath = glob.glob(f"{self.storagePath}/*.json")
            for _path in _globPath:
                _fileContent = None
                with open(_path, "r") as file:
                    _fileContent = file.read()

                if(len(_fileContent) > 2):
                    _all.append(fromJson(_fileContent, self.typeT))
            
            return _all
        except Exception:
            if(self.debug): printS(sys.exc_info(), color = BashColor.WARNING)
            printS("Error getting all", color = BashColor.FAIL)
            return List[T]

    def update(self, entity: T) -> bool:
        """
        Update entity using local JSON files for storage.

        Args:
            entity (T): entity to update

        Returns:
            bool: success = True
        """

        _entity = self.get(entity.id)
        if(_entity == None):
            printS("Error updating ", entity.id, ", entity does not exist", color = BashColor.FAIL)
            return False

        try:
            _updatedEntityDict = toDict(entity)
            _filename = _entity.id + ".json"
            _path = os.path.join(self.storagePath, _filename)
            with open(_path, "w") as file:
                json.dump(_updatedEntityDict, file, indent=4, default=str)
            
            return True
        except Exception:
            if(self.debug): printS(sys.exc_info(), color = BashColor.WARNING)
            printS("Error updating ", entity.id, color = BashColor.FAIL)
            return False

    def remove(self, id: str) -> bool:
        """
        Remove entity using local JSON files for storage.

        Args:
            id (str): id of entity to remove

        Returns:
            bool: success = True
        """

        _entity = self.get(id)
        if(_entity == None):
            printS("Error removeing ", id, ", entity does not exist", color = BashColor.FAIL)
            return False

        try:
            _filename = _entity.id + ".json"
            path = os.path.join(self.storagePath, _filename)
            os.remove(path)
            
            return True
        except Exception:
            if(self.debug): printS(sys.exc_info(), color = BashColor.WARNING)
            printS("Error removing ", id, color = BashColor.FAIL)
            return False
