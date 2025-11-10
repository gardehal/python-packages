import os

class ArgHead():
    """
    Holder of all commands and args
    """
    
    commands: list[Commands]
    commandPrefix: str
    namedArgDelim: str
    argDelum: str
    
    def __init__(self, commands: list[Commands], commandPrefix: str = "-", namedArgDelim: str = ":", argDelum: str = " "):
        self.commands = commands
        self.commandPrefix = commandPrefix
        self.namedArgDelim = namedArgDelim
        self.argDelum = argDelum
    
    def validate(self, input: str) -> list[ArgsResult]:
        """
        Validate input and return list of ArgResults found, with arguments.
        """
        
        result = []
        
        # TODO reduce foreaches
        inputSplit = input.split(self.argDelum)
        for command in self.commands.alias:
            prefixedAlias = [f"{self.commandPrefix}{e}" for e in command.alias]
            for alias in prefixedAlias:
                commandIndex = inputSplit.index(alias)
                if(commandIndex):
                    potentialArgs = inputSplit[commandIndex+1:]
                    nextCommandIndex = potentialArgs.index(fr"{self.argDelim}{self.commandPrefix}.*")
                    argResult = ArgResult(command.name, command.hitValue, commandIndex, None, None, inputSplit[nextCommandIndex:])
                    
                    # Most of this in funcs(s)
                    args = potentialArgs[:nextCommandIndex]
                    namedArgs = [e for e in args if(self.namedArgDelim in e)]
                    namedArgsDict = {}
                    for value in namedArgs:
                        key, value = value.split(self.namedArgDelim)
                        namedArgsDict[key] = value
                    
                    resolvedArgValues = {}
                    unhandledInputs = []
                    for argValue in command.argValues:
                        foundNamedArgs = list(set(argValue.alias) & set(namedArgsDict.keys))
                        if(not foundNamedArgs):
                            continue
                    result.append(argResult)
        
        return result
    
class Commands():
    """
    Designates commands
    eg. dimensions in 
    $ -dimensions value:100
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
    Designates values input as args to commands 
    eg. height in 
    $ -dimensions height:100
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
    Returns of validate, with info of what command was hit, what values was added, where it was in the input string, what to parse next for the caller
    """
    commandName: str
    hitValue: str # any
    commandIndex: int
    argValues: dict[str, any]
    unhandledInputs: list[str]
    nextInput: str

    def __init__(self, commandName: str, hitValue: str, commandIndex: int, argValues: dict[str, any], unhandledInputs: list[str], nextInput: str):
        self.commandName = commandName
        self.hitValue = hitValue
        self.commandIndex = commandIndex
        self.argValues = argValues
        self.unhandledInputs = unhandledInputs
        self.nextInput = nextInput
