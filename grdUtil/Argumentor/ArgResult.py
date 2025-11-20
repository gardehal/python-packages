
class ArgResult():
    """
    Returns of validate, with info of what command was hit, what values was added, where it was in the input string, what to parse next for the caller
    """
    
    isValid: bool
    commandName: str
    commandHitValue: object
    commandIndex: int
    argValues: dict[str, object]
    errorMessages: list[str]
    nextInputs: list[str]
    
    def createValid(self, commandName: str, commandHitValue: object, commandIndex: int, argValues: dict[str, object], errorMessages: list[str], nextInputs: list[str]):
        self.isValid = True
        self.commandName = commandName
        self.commandHitValue = commandHitValue
        self.commandIndex = commandIndex
        self.argValues = argValues
        self.errorMessages = errorMessages
        self.nextInputs = nextInputs
        
        return self
    
    def createInvalid(self, commandName: str, commandIndex: int, errorMessages: list[str], nextInputs: list[str]):
        self.isValid = False
        self.commandName = commandName
        self.commandHitValue = None
        self.commandIndex = commandIndex
        self.argValues = None
        self.errorMessages = errorMessages
        self.nextInputs = nextInputs
        
        return self
        
    def toString(self) -> str:
        return f"""
            isValid: {self.isValid},
            commandName: {self.commandName},
            commandHitValue: {self.commandHitValue},
            commandIndex: {self.commandIndex},
            argValues: {self.argValues},
            errorMessages: {self.errorMessages},
            nextInputs: {self.nextInputs},
            """
