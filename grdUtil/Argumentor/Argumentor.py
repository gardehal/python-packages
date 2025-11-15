from .ArgValue import ArgValue
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
            for commandAlias in prefixedCommandAlias:
                if(commandAlias not in input):
                    continue
                
                commandIndex = input.index(commandAlias)
                potentialArgs = input[commandIndex + 1:]
                
                argsEndIndex = self.__getLastArgIndex(potentialArgs)
                args = potentialArgs[:argsEndIndex]
                aliasArgsDict = self.__getAliasArgsDict(args)
                argValues, unhandledInputs = self.__validateArgs(command.argValues, aliasArgsDict)
                
                unnamedArgs = [e for e in args if(e.split(self.namedArgDelim)[0] not in list(aliasArgsDict.keys()))]
                for i in range(len(unnamedArgs)):
                    unnamedArg = unnamedArgs[i]
                    positionalArg = command.argValues[i] # Check i doesnt go outside bounds?
                    if(positionalArg.name in aliasArgsDict.keys()):
                        unhandledInputs.append(unnamedArg) # Arg already read as a named arg
                        continue
                    
                    argValues[positionalArg.name] = unnamedArg
                    
                # TODO
                # for each key in argValues dict, validate using input validators, try cast to type T, if not then discard, return results
                
                argResult = ArgResult(command.name, command.hitValue, commandIndex, argValues, unhandledInputs, potentialArgs[argsEndIndex:])
                result.append(argResult)
                
                # TODO remove
                print("debug")
                print(f"expected last arg: {args[argsEndIndex-1]}")
                print(f"argsEndIndex: {argsEndIndex}")
                print(f"args: {args}")
                print(f"input: {input}")
                print(f"unnamedArgs: {unnamedArgs}")
                print(f"argValues: {argValues}")
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
    
    def __getAliasArgsDict(self, args: list[str]) -> dict[str, str]:
        aliasArgs = [e for e in args if(self.namedArgDelim in e)]
        aliasArgsDict = {}
        for value in aliasArgs:
            key, value = value.split(self.namedArgDelim)
            aliasArgsDict[key] = value
            
        return aliasArgsDict
    
    def __validateArgs(self, argValues: list[ArgValue], aliasArgsDict: dict[str, str]) -> tuple[list[str], list[str]]:
        argValueAliasMap = {}
        for argValue in argValues:
            argValueAliasMap[argValue.name] = argValue.name
            for alias in argValue.alias:
                argValueAliasMap[alias] = argValue.name
            
        argValues = {}
        unhandledInputs = []
        for key in aliasArgsDict.keys():
            if(key not in argValueAliasMap.keys()):
                unhandledInputs.append(self.__formatArgErrorMessage(key, "Not a valid argument alias"))
                continue
            
            if(key in argValues.keys()):
                unhandledInputs.append(self.__formatArgErrorMessage(key, "Argument with this alias was already added"))
                continue
            
            argValues[argValueAliasMap[key]] = aliasArgsDict[key]
            
        return argValues, unhandledInputs
    
    def __formatArgErrorMessage(self, arg: str, error: str) -> str:
        return f"Argument \"{arg}\" not parsed: {error}"