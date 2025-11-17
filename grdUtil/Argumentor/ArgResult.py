
class ArgResult():
    """
    Returns of validate, with info of what command was hit, what values was added, where it was in the input string, what to parse next for the caller
    """
    isValid: bool
    commandName: str
    hitValue: object
    commandIndex: int
    argValues: dict[str, object]
    errorMessages: list[str]
    nextInputs: list[str]

    def __init__(self, isValid: bool, commandName: str, hitValue: object, commandIndex: int, argValues: dict[str, object], errorMessages: list[str], nextInputs: list[str]):
        self.isValid = isValid
        self.commandName = commandName
        self.hitValue = hitValue
        self.commandIndex = commandIndex
        self.argValues = argValues
        self.errorMessages = errorMessages
        self.nextInputs = nextInputs
        
    # def __init__(self, commandName: str, hitValue: object, commandIndex: int):
    #     self.isValid = False
    #     self.commandName = commandName
    #     self.hitValue = hitValue
    #     self.commandIndex = commandIndex
    #     self.argValues = {}
    #     self.errorMessages = []
    #     self.nextInputs = []
