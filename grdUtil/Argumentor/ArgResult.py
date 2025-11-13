
class ArgResult():
    """
    Returns of validate, with info of what command was hit, what values was added, where it was in the input string, what to parse next for the caller
    """
    commandName: str
    hitValue: object
    commandIndex: int
    argValues: dict[str, object]
    unhandledInputs: list[str]
    nextInput: str

    def __init__(self, commandName: str, hitValue: object, commandIndex: int):
        self.commandName = commandName
        self.hitValue = hitValue
        self.commandIndex = commandIndex
        self.argValues = {}
        self.unhandledInputs = []
        self.nextInput = []
