from .Argument import Argument
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
        Commands and related arguments not in commands list will not be parsed.
        """
        
        if(len(input) == 0):
            return []
        
        # TODO: check duplicate command names/alias and argument/alias so it cant be -dimensions w:1 w:2 (width and weight)
        # Let user find out themselves? 
        # TODO reverse? as in get inputs with prefix, remove it, and match on alias, then find index again?
        # TODO Main loop and handleing should be reworked, spinning up 15 vars and reassigning seems unnessecary
        # TODO rename things, argument is a really bad name, command and argumentor is good, argresult is passable
        # TODO error messages should be improved, shorter, more concise
        
        result = []
        nextInputs = []
        for command in self.commands:
            prefixedCommandAlias = [f"{self.commandPrefix}{e}" for e in command.alias]
            for commandAlias in prefixedCommandAlias:
                if(commandAlias not in input):
                    continue
                
                commandIndex = input.index(commandAlias)
                potentialArgs = input[commandIndex + 1:]
                argsEndIndex = self.__getLastArgIndex(potentialArgs)
                nextInputs = potentialArgs[argsEndIndex:]
                
                args = potentialArgs[:argsEndIndex]
                aliasArgs = self.__getAliasArgs(args)
                arguments, errorMessages = self.__getNamedArgs(command.arguments, aliasArgs)
                self.__addPositionalArgs(args, arguments, errorMessages, command, aliasArgs)
                castArguments = self.__argsAreValid(command, arguments, errorMessages)
                    
                isValid = castArguments != None
                argResult = ArgResult(isValid, command.name, command.hitValue, commandIndex, castArguments, errorMessages, nextInputs)
                result.append(argResult)
        
        if(nextInputs):
            result.extend(self.validate(nextInputs))
    
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
    
    def __getNamedArgs(self, arguments: list[Argument], aliasArgs: dict[str, str]) -> tuple[list[str], list[str]]:
        argumentAliasMap = {}
        for argument in arguments:
            argumentAliasMap[argument.name] = argument.name
            for alias in argument.alias:
                argumentAliasMap[alias] = argument.name
            
        argumentsDict = {}
        unhandledInputs = []
        for key in aliasArgs.keys():
            if(key not in argumentAliasMap.keys()):
                unhandledInputs.append(self.__formatArgErrorMessage(key, "Not a valid argument alias"))
                continue
            
            if(key in argumentsDict.keys()):
                unhandledInputs.append(self.__formatArgErrorMessage(key, "Alias was already added"))
                continue
            
            argumentsDict[argumentAliasMap[key]] = aliasArgs[key]
            
        return argumentsDict, unhandledInputs
    
    def __addPositionalArgs(self, args: list[str], arguments: dict[str, str], errorMessages: list[str], command: Command, aliasArgs: dict[str, str]) -> tuple[list[str], list[str]]:
        unnamedArgs = [e for e in args if(e.split(self.namedArgDelim)[0] not in list(aliasArgs.keys()))]
        
        for i in range(len(unnamedArgs)):
            if(i >= len(command.arguments)):
                errorMessages.append(f"Received more arguments ({len(unnamedArgs)}) than expected ({len(command.arguments)})")
                for extraArg in unnamedArgs[i:]:
                    errorMessages.append(self.__formatArgErrorMessage(extraArg, f"Skipped, exceeds Arguments length"))
                    
                break
            
            unnamedArg = unnamedArgs[i]
            positionalArg = command.arguments[i]
            if(positionalArg.name in aliasArgs.keys()):
                errorMessages.append(self.__formatArgErrorMessage(unnamedArg, f"Already added as named argument {positionalArg.name}"))
                continue
            
            arguments[positionalArg.name] = unnamedArg
            
        return arguments, errorMessages
    
    def __argsAreValid(self, command: Command, arguments: dict[str, str], errorMessages: list[str]) -> dict[str, object]:
        
        castDict: dict[str, object] = {}
        for key in arguments.keys():
            argument = [e for e in command.arguments if e.name is key ][0]
            if(argument is None):
                errorMessages.append(self.__formatArgErrorMessage(value, "No Argument found"))
                continue
            
            value = arguments[key]
            if(value is None and not argument.nullable):
                if(argument.useDefaultValue):
                    errorMessages.append(self.__formatArgErrorMessage(value, f"{key} was None and not nullable, default {argument.defaultValue} was applied"))
                    castValue = argument.defaultValue
                    continue
                else:
                    errorMessages.append(self.__formatArgErrorMessage(value, f"Critical error! {key} was None, and Argument is not nullable"))
                    return None
            
            castValue = None
            try:
                castValue = (argument.typeT)(value)
            except:
                if(argument.useDefaultValue):
                    errorMessages.append(self.__formatArgErrorMessage(value, f"{key} could not be cast, default {argument.defaultValue} was applied"))
                    castValue = argument.defaultValue
                    continue
                else:
                    errorMessages.append(self.__formatArgErrorMessage(value, f"Critical error! {key} could not be cast to {argument.typeT}")) 
                    return None
        
            if(argument.validators):
                resultValid = argument.validators(castValue)
                if(not resultValid):
                    if(argument.useDefaultValue):
                        errorMessages.append(self.__formatArgErrorMessage(value, f"{key} did not pass validation, default {argument.defaultValue} was applied"))
                        castValue = argument.defaultValue
                        continue
                    else:
                        errorMessages.append(self.__formatArgErrorMessage(value, f"Critical error! {key} did not pass validation"))
                        return FaNonelse
        
            castDict[key] = castValue
        
        return castDict
    
    def __formatArgErrorMessage(self, arg: str, error: str) -> str:
        return f"Argument \"{arg}\" error: {error}"
    