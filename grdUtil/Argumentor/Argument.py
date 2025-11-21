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
    nullable: bool
    validators: Callable[[T], bool]
    useDefaultValue: bool
    defaultValue: T
    
    def __init__(self, name: str, order: int, alias: list[str], type: Type[T], nullable: bool = False, validators: Callable[[T], bool] = None, useDefaultValue: bool = False, defaultValue: T = None):
        self.name = name
        self.order = order
        self.alias = alias
        self.typeT = type
        self.nullable = nullable
        self.validators = validators
        self.useDefaultValue = useDefaultValue
        self.defaultValue = defaultValue
                