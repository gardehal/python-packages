from typing import TypeVar, Type

T = TypeVar("T")

class ArgValue():
    """
    Designates values input as args to commands 
    eg. height in 
    $ -dimensions height:100
    """
    name: str
    order: int
    alias: list[str]
    typeT: Type[T]
    nullable: bool
    validators: int # func , things like min, max values, length etc.
    useDefaultValue: bool
    defaultValue: T
    
    def __init__(self, name: str, order: int, alias: list[str], type: Type[T], nullable: bool = False, validators: int = 0):
        self.name = name
        self.order = order
        self.alias = alias
        self.typeT = type
        self.nullable = nullable
        self.validators = validators
        # self.useDefaultValue = useDefaultValue
        # self.defaultValue = defaultValue
        
        # TODO check duplicates by name
        