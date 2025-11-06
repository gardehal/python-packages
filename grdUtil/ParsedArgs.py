import os

class ArgHead():
    """
    Holder of all flags and args
    """
    
    flagPrefix: str
    namedArgDelim: str
    flags: list[Flag]
    
    def __init__(self, flagPrefix: str = "-", namedArgDelim: str = ":", flags: list[Flag] = []):
        self.flagPrefix = flagPrefix
        self.namedArgDelim = namedArgDelim
        self.flags = flags
    
    def validate(self, input: str) -> ArgsResult:
        # combine prefix and flag aliases
        # find positional and named argvalues
        # combine and return ArgsResult
        
        return ArgsResult()
    
class Flag():
    """
    Designates flags
    eg. height in 
    $ -height value:100
    """
    name: str
    order: int
    alias: list[str]
    argValues: list[ArgValue]
    hitValue: str # any
    
    def __init__(self, name: str, order: int, alias: list[str], argValues: list[ArgValue], hitValue: str):
        self.name = name
        self.order = order
        self.alias = alias
        self.hitValue = hitValue
        
class ArgValue():
    """
    Designates values input as args to flags 
    eg. value in 
    $ -height value:100
    """
    name: str
    order: int
    alias: list[str]
    type: str # T
    nullable: bool
    validators: int # func , things like min, max values, length etc.
    
    def __init__(self, name: str, order: int, alias: list[str], type: str, nullable: bool, validators: int):
        self.name = name
        self.order = order
        self.alias = alias
        self.type = type
        self.nullable = nullable
        self.validators = validators

class ArgsResult():
    """
    Returns of validate, with info of what flag was hit, what values was added, where it was in the input string, what to parse next for the caller
    """
    flagName: str
    flagIndex: int
    hitValue: str # any
    argValues: list[ArgValue] # struct? str:any?
    nextInput: str

    def __init__(self, flagName: str, flagIndex: int, hitValue: str, argValues: list[ArgValue], nextInput: str):
        self.flagName = flagName
        self.flagIndex = flagIndex
        self.hitValue = hitValue
        self.argValues = argValues
        self.nextInput = nextInput
