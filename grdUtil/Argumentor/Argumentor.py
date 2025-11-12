from .ArgResult import ArgResult
from .Command import Command

class Argumentor():
    """
    Holder of all commands and args
    """
    
    commands: list[Command]
    commandPrefix: str
    namedArgDelim: str
    inputDelim: str
    
    def __init__(self, commands: list[Command], commandPrefix: str = "-", namedArgDelim: str = ":", inputDelim: str = " "):
        self.commands = commands
        self.commandPrefix = commandPrefix
        self.namedArgDelim = namedArgDelim
        self.inputDelim = inputDelim
    
        
    def validate(self, input: str) -> list[ArgResult]:
        return self.validate(input.split(self.inputDelim))
        
    def validate(self, input: list[str]) -> list[ArgResult]:
        """
        Validate input and return list of ArgResults found, with arguments.
        """
        
        # TODO reduce foreaches
        result = []
        for command in self.commands:
            prefixedAlias = [f"{self.commandPrefix}{e}" for e in command.alias]
            for alias in prefixedAlias:
                commandIndex = input.index(alias)
                if(commandIndex):
                    potentialArgs = input[commandIndex+1:]
                    nextCommandIndex = potentialArgs.index(fr"{self.inputDelim}{self.commandPrefix}.*")
                    argResult = ArgResult(command.name, command.hitValue, commandIndex, None, None, input[nextCommandIndex:])
                    
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
                        
                        foundNamedArg = foundNamedArgs[0]
                        value = namedArgsDict[foundNamedArg]
                        # validate using argValue.validators
                        
                        # try cast value to argValue.type T
                        castValue = value
                        # if(cast_failed):
                        #     argResult.unhandledInputs.append(foundNamedArg)
                        #     continue
                        
                        argResult.argValues[argValue.name] = castValue
                    
                    # deal with positional
                    # positionalArgs = [e for e in args if(self.namedArgDelim not in e)]
                    # can fold into argValues loop?
                    
                    argResult.argValues = resolvedArgValues
                    argResult.unhandledInputs = unhandledInputs
                    result.append(argResult)
        
        return result