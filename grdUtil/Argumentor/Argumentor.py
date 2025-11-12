from ArgsResult import ArgsResult
from Commands import Command

class Argumentor():
    """
    Holder of all commands and args
    """
    
    commands: list[Command]
    commandPrefix: str
    namedArgDelim: str
    argDelim: str
    
    def __init__(self, commands: list[Command], commandPrefix: str = "-", namedArgDelim: str = ":", argDelim: str = " "):
        self.commands = commands
        self.commandPrefix = commandPrefix
        self.namedArgDelim = namedArgDelim
        self.argDelim = argDelim
    
    def validate(self, input: str) -> list[ArgsResult]:
        """
        Validate input and return list of ArgResults found, with arguments.
        """
        
        result = []
        
        # TODO reduce foreaches
        inputSplit = input.split(self.argDelim)
        for command in self.commands.alias:
            prefixedAlias = [f"{self.commandPrefix}{e}" for e in command.alias]
            for alias in prefixedAlias:
                commandIndex = inputSplit.index(alias)
                if(commandIndex):
                    potentialArgs = inputSplit[commandIndex+1:]
                    nextCommandIndex = potentialArgs.index(fr"{self.argDelim}{self.commandPrefix}.*")
                    argResult = ArgsResult(command.name, command.hitValue, commandIndex, None, None, inputSplit[nextCommandIndex:])
                    
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