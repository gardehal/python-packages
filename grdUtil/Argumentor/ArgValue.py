
class ArgValue():
    """
    Designates values input as args to commands 
    eg. height in 
    $ -dimensions height:100
    """
    name: str
    order: int
    alias: list[str]
    type: str # T
    nullable: bool
    validators: int # func , things like min, max values, length etc.
    
    def __init__(self, name: str, order: int, alias: list[str], type: str, nullable: bool, validators: int):
        self.name = name
        self.order = order
        self.alias = alias
        self.type = type
        self.nullable = nullable
        self.validators = validators