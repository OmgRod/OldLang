from executor import Executor
from tokeniser import Tokeniser
from parser import Parser

with open("test.old", "r") as f:
    code = f.read()
    tokens = Tokeniser.tokenise(code)
    ast = Parser.parse(tokens)
    exe = Executor()
    exe.execute(ast)