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
        Commands and related arguments not in commands list will not be parsed.
        """
        
        if(len(input) == 0):
            return []
        
        # TODO: check duplicate command names/alias and argvalue/alias so it cant be -dimensions w:1 w:2 (width and weight)
        # Let user find out themselves? 
        # TODO reverse? as in get inputs with prefix, remove it, and match on alias, then find index again?
        # TODO what if an input should be something like "-1", means forced named arg?
        # TODO Main loop and handleing should be reworked, spinning up 15 vars and reassigning seems unnessecary
        # TODO rename things, argvalue is a really bad name, command and argumentor is good, argresult is passable
        
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
                argValues, errorMessages = self.__getNamedArgs(command.argValues, aliasArgs)
                self.__addPositionalArgs(args, argValues, errorMessages, command, aliasArgs)
                isValid = self.__argsAreValid(command, argValues, errorMessages)
                    
                argResult = None
                if(isValid):
                    argResult = ArgResult().createValid(command.name, command.hitValue, commandIndex, argValues, errorMessages, nextInputs)
                else:
                    argResult = ArgResult().createInvalid(command.name, commandIndex, errorMessages, nextInputs)
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
    
    def __addPositionalArgs(self, args: list[str], argValues: dict[str, str], errorMessages: list[str], command: Command, aliasArgs: dict[str, str]) -> tuple[list[str], list[str]]:
        unnamedArgs = [e for e in args if(e.split(self.namedArgDelim)[0] not in list(aliasArgs.keys()))]
        
        for i in range(len(unnamedArgs)):
            if(i >= len(command.argValues)):
                errorMessages.append(f"Received more arguments ({len(unnamedArgs)}) than expected ({len(command.argValues)})")
                for extraArg in unnamedArgs[i:]:
                    errorMessages.append(self.__formatArgErrorMessage(extraArg, f"Skipped, exceeds ArgValues length"))
                    
                break
            
            unnamedArg = unnamedArgs[i]
            positionalArg = command.argValues[i]
            if(positionalArg.name in aliasArgs.keys()):
                errorMessages.append(self.__formatArgErrorMessage(unnamedArg, f"Argument was already added as named argument {positionalArg.name}"))
                continue
            
            argValues[positionalArg.name] = unnamedArg
            
        return argValues, errorMessages
    
    def __argsAreValid(self, command: Command, argValues: dict[str, str], errorMessages: list[str]) -> bool:
        
        castDict: dict[str, object] = {}
        for key in argValues.keys():
            argValue = [e for e in command.argValues if e.name is key ][0]
            if(argValue is None):
                errorMessages.append(self.__formatArgErrorMessage(value, "No ArgValue found"))
                continue
            
            value = argValues[key]
            if(value is None and not argValue.nullable):
                if(argValue.useDefaultValue):
                    errorMessages.append(self.__formatArgErrorMessage(value, f"Argument for {key} was None and not nullable, default {argValue.defaultValue} was applied"))
                    castValue = argValue.defaultValue
                    continue
                else:
                    errorMessages.append(self.__formatArgErrorMessage(value, f"Critical error! Argument for {key} was None, and ArgValue is not nullable"))
                    return False
            
            castValue = None
            try:
                castValue = (argValue.typeT)(value)
            except:
                if(argValue.useDefaultValue):
                    errorMessages.append(self.__formatArgErrorMessage(value, f"Argument for {key} could not be cast, default {argValue.defaultValue} was applied"))
                    castValue = argValue.defaultValue
                    continue
                else:
                    errorMessages.append(self.__formatArgErrorMessage(value, f"Critical error! Argument for {key} could not be cast to {argValue.typeT}")) 
                    return False
        
            if(argValue.validators):
                resultValid = argValue.validators(castValue)
                if(not resultValid):
                    if(argValue.useDefaultValue):
                        errorMessages.append(self.__formatArgErrorMessage(value, f"Argument for {key} did not pass validation, default {argValue.defaultValue} was applied"))
                        castValue = argValue.defaultValue
                        continue
                    else:
                        errorMessages.append(self.__formatArgErrorMessage(value, f"Critical error! Argument for {key} did not pass validation"))
                        return False
        
            castDict[key] = castValue
        
        return True # TODO + castDict
    
    def __formatArgErrorMessage(self, arg: str, error: str) -> str:
        return f"Argument \"{arg}\" not parsed: {error}"
    