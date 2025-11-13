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
        Validate input and return list of ArgResults found, with arguments, if any are found.
        """
        
        if(len(input) == 0):
            return []
        
        # TODO reduce foreaches
        
        commandRegex = fr"{self.commandPrefix}.*"
        result = []
        for command in self.commands:
            prefixedAlias = [f"{self.commandPrefix}{e}" for e in command.alias]
            for alias in prefixedAlias:
                if(alias not in input):
                    continue
                
                commandIndex = input.index(alias)
                potentialArgs = input[commandIndex + 1:]
                nextCommandIndex = 0
                if(commandRegex in input):
                    nextCommandIndex = potentialArgs.index(commandRegex)
                    
                argResult = ArgResult(command.name, command.hitValue, commandIndex)
                
                args = potentialArgs[:nextCommandIndex - 1]
                namedArgs = [e for e in args if(self.namedArgDelim in e)]
                namedArgsDict = {}
                for value in namedArgs:
                    key, value = value.split(self.namedArgDelim)
                    namedArgsDict[key] = value
                
                print("debug")
                print(input)
                print(commandIndex)
                print(potentialArgs)
                print(nextCommandIndex)
                print(args)
                print(namedArgs)
                print(namedArgsDict)
                print("debug")
                resolvedArgValues = {}
                unhandledInputs = []
                for argValue in command.argValues:
                    foundNamedArgs = list(set(argValue.alias) & set([namedArgsDict.keys]))
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
                argResult.nextInput = potentialArgs[nextCommandIndex:]
                result.append(argResult)
        
        return result