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
                aliasArgs = self.__getAliasArgs(args)
                argValues, errorMessages = self.__getNamedArgs(command.argValues, aliasArgs)
                self.__addPositionalArgs(args, argValues, errorMessages, command, aliasArgs)
                    
                # TODO
                # for each key in argValues dict, validate using input validators and nullable, try cast to type T, if not then discard, return results
                
                argResult = ArgResult(command.name, command.hitValue, commandIndex, argValues, errorMessages, potentialArgs[argsEndIndex:])
                result.append(argResult)
        
        return result
    
    def __getLastArgIndex(self, potentialArgs: list[str]) -> int:
        commandRegex = fr"^{self.commandPrefix}.*"
        for potentialArg in potentialArgs:
            if(re.search(commandRegex, potentialArg)):
                return (potentialArgs.index(potentialArg))
            
        # None found, default to end of list
        return len(potentialArgs)
    
    def __getAliasArgs(self, args: list[str]) -> dict[str, str]:
        inputAliasArgs = [e for e in args if(self.namedArgDelim in e)]
        aliasArgs = {}
        for value in inputAliasArgs:
            key, value = value.split(self.namedArgDelim)
            aliasArgs[key] = value
            
        return aliasArgs
    
    def __getNamedArgs(self, argValues: list[ArgValue], aliasArgs: dict[str, str]) -> tuple[list[str], list[str]]:
        argValueAliasMap = {}
        for argValue in argValues:
            argValueAliasMap[argValue.name] = argValue.name
            for alias in argValue.alias:
                argValueAliasMap[alias] = argValue.name
            
        argValues = {}
        unhandledInputs = []
        for key in aliasArgs.keys():
            if(key not in argValueAliasMap.keys()):
                unhandledInputs.append(self.__formatArgErrorMessage(key, "Not a valid argument alias"))
                continue
            
            if(key in argValues.keys()):
                unhandledInputs.append(self.__formatArgErrorMessage(key, "Argument with this alias was already added"))
                continue
            
            argValues[argValueAliasMap[key]] = aliasArgs[key]
            
        return argValues, unhandledInputs
    
    def __addPositionalArgs(self, args: list[str], argValues: list[str], errorMessages: list[str], command: Command, aliasArgs: dict[str, str]) -> tuple[list[str], list[str]]:
        unnamedArgs = [e for e in args if(e.split(self.namedArgDelim)[0] not in list(aliasArgs.keys()))]
        for i in range(len(unnamedArgs)):
            unnamedArg = unnamedArgs[i]
            positionalArg = command.argValues[i] # Check i doesnt go outside bounds?
            if(positionalArg.name in aliasArgs.keys()):
                errorMessages.append(self.__formatArgErrorMessage(unnamedArg, f"Argument was already added as named argument {positionalArg.name}"))
                continue
            
            argValues[positionalArg.name] = unnamedArg
                    
            # TODO if length of positional args exceed expected argValues, add remaining as unhandled
    
    def __formatArgErrorMessage(self, arg: str, error: str) -> str:
        return f"Argument \"{arg}\" not parsed: {error}"