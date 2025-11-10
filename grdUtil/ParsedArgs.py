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
                    args = potentialArgs[:nextCommandIndex]
                    
                    argResult = ArgResult(command.name, command.hitValue, commandIndex, [], [], inputSplit[nextCommandIndex:])
                    namedArgs = {}
                    for argValue in command.argValues:
                        # for argument in arguments, intersect with command.argValues + self.namedArgDelim
                        # if match, add to namedArgs dict as argValue.name: argument.split(self.namedArgDelim)[1], if empty, use None? assume next arg is value?
                        
                        argAlias = [f"{e}{self.namedArgDelim}" for e in argValue.alias]
                        argKeys = [e for e in args if(e.__contains__(self.namedArgDelim))]
                        for key in argKeys:
                            print(key)
                            if(key in argAlias):
                                namedArgs[key.split(self.namedArgDelim)[0]: args[args.index(key) + 1]] # awful
                        
                        #find positional arguments, prioritized - ignore named args? include named args in position? 
                        # - get and removed named, then check positional
                        #find named arguments
                        # argResult.argValues.append()
                        # argResult.unhandledInputs.append()
                        
                    result.append(argResult)
        
        return result
    
class Commands():
    """
    Designates commands
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
    Designates values input as args to commands 
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
    Returns of validate, with info of what command was hit, what values was added, where it was in the input string, what to parse next for the caller
    """
    commandName: str
    hitValue: str # any
    commandIndex: int
    argValues: list[ArgValue] # struct? str:any?
    unhandledInputs: list[str]
    nextInput: str

    def __init__(self, commandName: str, hitValue: str, commandIndex: int, argValues: list[ArgValue], unhandledInputs: list[str], nextInput: str):
        self.commandName = commandName
        self.hitValue = hitValue
        self.commandIndex = commandIndex
        self.argValues = argValues
        self.unhandledInputs = unhandledInputs
        self.nextInput = nextInput
