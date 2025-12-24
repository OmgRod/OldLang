class ASTNode:
    pass

class SetStatement(ASTNode):
    def __init__(self, name: str, value: int):
        self.name = name
        self.value = value

class WriteStatement(ASTNode):
    def __init__(self, name: str):
        self.name = name

class IncrementStatement(ASTNode):
    def __init__(self, name: str, amount: int):
        self.name = name
        self.amount = amount
