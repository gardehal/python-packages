import os

class ArgHead():
    """
    Holder of all flags and args
    """
    
    flags: list[Flag]
    flagPrefix: str
    namedArgDelim: str
    argDelum: str
    
    def __init__(self, flags: list[Flag], flagPrefix: str = "-", namedArgDelim: str = ":", argDelum: str = " "):
        self.flags = flags
        self.flagPrefix = flagPrefix
        self.namedArgDelim = namedArgDelim
        self.argDelum = argDelum
    
    def validate(self, input: str) -> list[ArgsResult]:
        
        result = []
        
        inputSplit = input.split(self.argDelum)
        for flag in self.flags.alias:
            prefixedAlias = [f"{self.flagPrefix}{e}" for e in flag.alias]
            for alias in prefixedAlias:
                flagIndex = inputSplit.index(alias)
                if(flagIndex):
                    potentialArguments = inputSplit[flagIndex+1:]
                    nextFlagIndex = potentialArguments.index(fr"{self.argDelum}{self.flagPrefix}.*")
                    arguments = potentialArguments[:nextFlagIndex]
                    
                    argResult = ArgResult(flag.name, flag.hitValue, flagIndex, [], [], inputSplit[nextFlagIndex:])
                    for argument in arguments:
                        print(argument)
                        #find positional arguments, prioritized - ignore named args? include named args in position? 
                        #find named arguments
                        # argResult.argValues.append()
                        # argResult.unhandledInputs.append()
                        
                    result.append(argResult)
        
        return result
    
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
    
    def __init__(self, name: str, order: int, alias: list[str], hitValue: str):
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
    hitValue: str # any
    flagIndex: int
    argValues: list[ArgValue] # struct? str:any?
    unhandledInputs: list[str]
    nextInput: str

    def __init__(self, flagName: str, hitValue: str, flagIndex: int, argValues: list[ArgValue], unhandledInputs: list[str], nextInput: str):
        self.flagName = flagName
        self.hitValue = hitValue
        self.flagIndex = flagIndex
        self.argValues = argValues
        self.unhandledInputs = unhandledInputs
        self.nextInput = nextInput
