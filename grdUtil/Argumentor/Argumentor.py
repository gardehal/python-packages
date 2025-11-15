from .ArgResult import ArgResult
from .Command import Command

import re

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
        
        result = []
        for command in self.commands:
            prefixedCommandAlias = [f"{self.commandPrefix}{e}" for e in command.alias]
            for alias in prefixedCommandAlias:
                if(alias not in input):
                    continue
                
                commandIndex = input.index(alias)
                potentialArgs = input[commandIndex + 1:]
                
                argsEndIndex = self.__getLastArgIndex(potentialArgs)
                args = potentialArgs[:argsEndIndex]
                namedArgsDict = self.__getNamedArgsDict(args)
                unhandledInputs = []
                
                # TODO
                # for each in namedArgsDict, replace key with name of whatever argValue key is alias for
                # Dont like creating another dict here..
                # argValues = {}
                # for key in namedArgsDict.keys():
                #     if(key in alias of argsValue.alias):
                #         argValues[argsValue.name] = namedArgsDict[key]
                
                unnamedArgs = [e for e in args if(e.split(self.namedArgDelim)[0] not in list(namedArgsDict.keys()))]
                for i in range(len(unnamedArgs)):
                    unnamedArg = unnamedArgs[i]
                    positionalArg = command.argValues[i]
                    if(positionalArg.name in namedArgsDict.keys()):
                        unhandledInputs.append(unnamedArg)
                        continue
                    
                    namedArgsDict[positionalArg.name] = unnamedArg
                    
                # TODO
                # for each key in dict, validate, try cast to type T, if not then discard, return results
                
                argResult = ArgResult(command.name, command.hitValue, commandIndex, namedArgsDict, unhandledInputs, potentialArgs[argsEndIndex:])
                result.append(argResult)
                
                # TODO remove
                print("debug")
                print(f"expected last arg: {args[argsEndIndex-1]}")
                print(f"argsEndIndex: {argsEndIndex}")
                print(f"args: {args}")
                print(f"input: {input}")
                print(f"unnamedArgs: {unnamedArgs}")
                print(f"namedArgsDict: {namedArgsDict}")
                print(f"unhandledInputs: {unhandledInputs}")
                print("debug")
        
        return result
    
    def __getLastArgIndex(self, potentialArgs: list[str]) -> int:
        commandRegex = fr"^{self.commandPrefix}.*"
        for potentialArg in potentialArgs:
            if(re.search(commandRegex, potentialArg)):
                return (potentialArgs.index(potentialArg))
            
        # None found, default to end of list
        return len(potentialArgs)
    
    def __getNamedArgsDict(self, args: list[str]) -> dict[str, str]:
        namedArgs = [e for e in args if(self.namedArgDelim in e)]
        namedArgsDict = {}
        for value in namedArgs:
            key, value = value.split(self.namedArgDelim)
            namedArgsDict[key] = value
            
        return namedArgsDict