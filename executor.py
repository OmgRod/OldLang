from ast_nodes import *

class Executor:
    def __init__(self):
        self.env = {}

    def execute(self, ast):
        for node in ast:
            if isinstance(node, SetStatement):
                self.env[node.name] = node.value

            elif isinstance(node, IncrementStatement):
                if node.name not in self.env:
                    raise RuntimeError(f"Variable '{node.name}' not defined")
                self.env[node.name] += node.amount

            elif isinstance(node, WriteStatement):
                if node.name not in self.env:
                    raise RuntimeError(f"Variable '{node.name}' not defined")
                print(self.env[node.name])
