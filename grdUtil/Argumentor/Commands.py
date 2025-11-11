from ArgValue import ArgValue

class Commands():
    """
    Designates commands
    eg. dimensions in 
    $ -dimensions value:100
    """
    name: str
    order: int
    alias: list[str]
    argValues: list[ArgValue]
    hitValue: str # any
    
    def __init__(self, name: str, order: int, alias: list[str], hitValue: str):
        self.name = name
        self.order = order
        self.alias = alias
        self.hitValue = hitValue
        