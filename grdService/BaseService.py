import uuid
from datetime import datetime
from typing import Generic, List, TypeVar

from grdUtil.BashColor import BashColor
from grdUtil.LocalJsonRepository import LocalJsonRepository
from grdUtil.PrintUtil import printS

T = TypeVar("T")


class BaseService(Generic[T]):
    """
    Extend as:
    class MyService(BaseService[TypeT]):

    Initiate as:
    BaseService.__init__(self, DEBUG, STORAGE_PATH) # Storage Path, e.g. os.path.join(SETTINGS_PATH, ENTITY_NAME) 

    Overwrite fields with:
    self.debug = True

    Overwrite method with:
    def add(self, ...) ...:
        BaseService.add(self, ...)

    Args:
        Generic (TypeT): Entity object to store
    """
    
    storagePath: str = None
    debug: bool = None
    baseRepository: LocalJsonRepository = None

    def __init__(self, typeT: type, debug: bool, storagePath: str) -> None:
        """
        Init with arguments.

        Args:
            typeT (type): Type of entity for service, e.g. T.
            debug (bool): Should debug prints?
            storagePath (str): Full path to store entities in.
        """
        
        self.typeT = typeT 
        self.storagePath = storagePath
        self.debug = debug
        self.entityRepository: LocalJsonRepository = LocalJsonRepository(typeT, self.debug, self.storagePath)
        
    def add(self, entity: T) -> T:
        """
        Add a new entity T.

        Args:
            entity (T): Entity to add.

        Returns:
            T | None: T if success, else None.
        """

        entity = entity
        
        if(hasattr(entity, "id") and entity.id == None):
            entity.id = str(uuid.uuid4())
        if(hasattr(entity, "added") and entity.added == None):
            entity.added = datetime.now()
        if(hasattr(entity, "created") and entity.created == None):
            entity.created = datetime.now()
        if(hasattr(entity, "updated") and entity.updated == None):
            entity.updated = datetime.now()
        
        if(self.entityRepository.add(entity)):
            return entity
        else:
            return None

    def exists(self, id: str) -> bool:
        """
        Check if entity exists by ID.

        Args:
            id (str): id of entity to get

        Returns:
            bool: exists
        """

        return self.entityRepository.exists(id)
        
    def get(self, id: str, includeSoftDeleted: bool = False) -> T:
        """
        Get entity T by ID.

        Args:
            id (str): ID of entity to get.
            includeSoftDeleted (bool): should include soft-deleted entities.

        Returns:
            T: T from storage.
        """

        entity = self.entityRepository.get(id)
        
        if(not includeSoftDeleted and hasattr(entity, "deleted") and entity != None and entity.deleted != None):
            printS("DEBUG: get - Entity with ID ", entity.id, " was soft deleted.", color = BashColor.WARNING, doPrint = self.debug)
            return None
        else:
            return entity

    def getAll(self, includeSoftDeleted: bool = False) -> List[T]:
        """
        Get all entity Ts.

        Args:
            includeSoftDeleted (bool): should include soft-deleted entities.

        Returns:
            List[T]: Ts in storage.
        """

        entities = self.entityRepository.getAll()
        result = []
        
        for entity in entities:
            if(not includeSoftDeleted and hasattr(entity, "deleted") and entity.deleted != None):
                printS("DEBUG: getAll - Entity with ID ", entity.id, " was soft deleted.", color = BashColor.WARNING, doPrint = self.debug)
            else:
                result.append(entity)
            
        return result
        
    def getAllIds(self, includeSoftDeleted: bool = False) -> List[str]:
        """
        Get all IDs of entities.

        Args:
            includeSoftDeleted (bool): should include soft-deleted entities.

        Returns:
            List[str]: IDs as List[str] from storage.
        """
        
        all = self.getAll(includeSoftDeleted)
        return [entity.id for entity in all]

    def update(self, entity: T) -> T:
        """
        Update given entity T.

        Args:
            entity (T): Entity to update.

        Returns:
            T | None: T if success, else None.
        """

        if(hasattr(entity, "updated")):
            entity.updated = datetime.now()
        
        if(self.entityRepository.update(entity)):
            return entity
        else:
            return None

    def delete(self, id: str) -> T:
        """
        (Soft) Delete a entity T.

        Args:
            id (str): ID of entity to delete.

        Returns:
            T | None: T if success, else None.
        """

        entity = self.get(id)
        if(entity == None):
            return None

        if(hasattr(entity, "deleted")):
            entity.deleted = datetime.now()
            
        if(self.update(entity)):
            return entity
        else:
            return None
        
    def restore(self, id: str) -> T:
        """
        Restore a (soft) deleted Entity.

        Args:
            id (str): ID of Entity to restore.

        Returns:
            T | None: T if success, else None.
        """

        entity = self.get(id, includeSoftDeleted = True)
        if(entity == None):
            return None

        if(hasattr(entity, "deleted")):
            entity.deleted = None
        
        if(self.update(entity)):
            return entity
        else:
            return None
        
    def remove(self, id: str, includeSoftDeleted: bool = False) -> T:
        """
        Permanently remove an entity T by ID.

        Args:
            id (str): ID of entity to remove.
            includeSoftDeleted (bool): should include soft-deleted entities.

        Returns:
            T | None: T if success, else None.
        """

        entity = self.get(id, includeSoftDeleted)
        if(entity == None):
            return None
        
        if(self.entityRepository.remove(entity.id)):
            return entity
        else:
            return None

    def addOrUpdate(self, entity: T) -> T:
        """
        Add entity T if none exists, else update existing.

        Args:
            entity (T): Entity to add or update.

        Returns:
            T | None: T if success, else None.
        """

        if(self.get(entity.id) == None):
            return self.add(entity)

        return self.update(entity)
    