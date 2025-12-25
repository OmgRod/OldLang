
class ASTNode:
    pass

# Loop and control flow AST nodes (restored)
class ForLoopStatement(ASTNode):
    def __init__(self, var_name: str, start: int, end: int, body: list):
        self.var_name = var_name
        self.start = start
        self.end = end
        self.body = body

class WhileLoopStatement(ASTNode):
    def __init__(self, condition_callable, body: list, condition_str=None):
        self.condition = condition_callable
        self.body = body
        self.condition_str = condition_str

class RepeatLoopStatement(ASTNode):
    def __init__(self, times: int, body: list):
        self.times = times
        self.body = body

class RepeatUntilLoopStatement(ASTNode):
    def __init__(self, body: list, var_name: str, value):
        self.body = body
        self.var_name = var_name
        self.value = value

# Wrapper to distinguish string literals from variable names
class StringLiteral(str):
    pass

class ASTNode:
    pass

class TestStatement(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class IfElseStatement(ASTNode):
    def __init__(self, condition_callable, if_body, else_body=None, condition_str=None):
        self.condition = condition_callable
        self.if_body = if_body
        self.else_body = else_body
        self.condition_str = condition_str


class SetStatement(ASTNode):
    def __init__(self, name: str, value):
        self.name = name
        self.value = value

class ChangeStatement(ASTNode):
    def __init__(self, name: str, value):
        self.name = name
        self.value = value

class WriteStatement(ASTNode):
    def __init__(self, name: str):
        self.name = name

class IncrementStatement(ASTNode):
    def __init__(self, name: str, amount: int):
        self.name = name
        self.amount = amount

# WhisperStatement for print-without-newline
class WhisperStatement(ASTNode):
    def __init__(self, name: str):
        self.name = name


