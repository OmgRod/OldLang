from ast_nodes import *

"""
KEYWORDS LIST:
set - sets/defines a new variable
to - same as using `=`. used when defining a new variable
increment - increments a value by a set amount. can also be negative to decrement
by - same as using `+=` in many languages. used alongside `increment`.
write - same as using the `print` function in python.
"""

class Parser:
    @staticmethod
    def parse(tokens):
        ast = []
        i = 0
        while i < len(tokens):
            token = tokens[i]

            if token == "set":
                name = tokens[i + 1]
                if tokens[i + 2] != "to":
                    raise Exception("Expected 'to' after variable name")
                value = int(tokens[i + 3])
                ast.append(SetStatement(name, value))
                i += 4

            elif token == "write":
                name = tokens[i + 1]
                ast.append(WriteStatement(name))
                i += 2

            elif token == "increment":
                name = tokens[i + 1]
                if tokens[i + 2] != "by":
                    raise Exception("Expected 'by' after variable name")
                amount = int(tokens[i + 3])
                ast.append(IncrementStatement(name, amount))
                i += 4

            elif token == "NEWLINE":
                i += 1

            else:
                raise Exception(f"Unknown token: {token}")

        return ast
