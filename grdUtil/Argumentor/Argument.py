from typing import TypeVar, Type, Callable

T = TypeVar("T")

class Argument():
    """
    Designates values input as arguments after commands 
    eg. height in 
    $ -dimensions height:100
    """
    
    name: str
    order: int
    alias: list[str]
    typeT: Type[T]
    castFunc: Callable[[str], T]
    nullable: bool
    validateFunc: Callable[[T], bool]
    useDefaultValue: bool
    defaultValue: T
    description: str
    
    def __init__(self, name: str, 
                 order: int, 
                 alias: list[str], 
                 type: Type[T], 
                 castFunc: Callable[[str], T] = None, 
                 nullable: bool = False, 
                 validateFunc: Callable[[T], bool] = None, 
                 useDefaultValue: bool = False, 
                 defaultValue: T = None, 
                 description: str = None):
        self.name = name
        self.order = order
        self.alias = alias
        self.typeT = type
        self.castFunc = castFunc
        self.nullable = nullable
        self.validateFunc = validateFunc
        self.useDefaultValue = useDefaultValue
        self.defaultValue = defaultValue
        self.description = description
                