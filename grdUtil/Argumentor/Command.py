from ArgValue import ArgValue

class Command():
    """
    Designates commands
    eg. dimensions in 
    $ -dimensions value:100
    """
    name: str
    order: int
    alias: list[str]
    hitValue: str # any
    argValues: list[ArgValue]
    
    def __init__(self, name: str, order: int, alias: list[str], hitValue: str, argValues: list[ArgValue] = []):
        self.name = name
        self.order = order
        self.alias = alias
        self.hitValue = hitValue
        self.argValues = argValues
        