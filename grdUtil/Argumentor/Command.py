from .Argument import Argument

class Command():
    """
    Designates commands
    eg. dimensions in 
    $ -dimensions value:100
    """
    
    name: str
    order: int
    alias: list[str]
    hitValue: object
    arguments: list[Argument]
    description: str
    
    def __init__(self, name: str, 
                 order: int, 
                 alias: list[str], 
                 hitValue: object, 
                 arguments: list[Argument], 
                 description: str = None):
        self.name = name
        self.order = order
        self.alias = alias
        self.hitValue = hitValue
        self.arguments = arguments 
        self.description = description
        
        self.arguments.sort(key=lambda x: x.order)
        