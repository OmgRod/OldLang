from ast_nodes import *

class Executor:
    def __init__(self):
        self.env = {}

    def execute(self, ast):
        for node in ast:
            if isinstance(node, TestStatement):
                left = node.left
                if isinstance(left, str) and left in self.env:
                    left = self.env[left]
                right = node.right
                passed = False
                if node.op == "is":
                    passed = (left == right)
                elif node.op == "is not":
                    passed = (left != right)
                print(f"Test: {left} {node.op} {right} -> {'PASS' if passed else 'FAIL'}")

            elif isinstance(node, IfElseStatement):
                if node.condition(self.env):
                    self.execute(node.if_body)
                elif node.else_body is not None:
                    self.execute(node.else_body)
            elif isinstance(node, SetStatement):
                value = node.value
                # If value is a variable name, resolve it
                if isinstance(value, str) and value in self.env:
                    value = self.env[value]
                # Try to parse as int, float, bool, or None if possible
                if isinstance(value, str):
                    v = value.lower()
                    if v == "true":
                        value = True
                    elif v == "false":
                        value = False
                    elif v in ("null", "none", "nothing"):
                        value = None
                    else:
                        try:
                            value = float(value) if '.' in value else int(value)
                        except Exception:
                            pass
                # Always assign/override the variable
                self.env[node.name] = value


            elif isinstance(node, ChangeStatement):
                if node.name not in self.env:
                    raise RuntimeError(f"Variable '{node.name}' not defined")
                value = node.value
                if isinstance(value, str) and value in self.env:
                    value = self.env[value]
                if isinstance(value, str):
                    v = value.lower()
                    if v == "true":
                        value = True
                    elif v == "false":
                        value = False
                    elif v in ("null", "none", "nothing"):
                        value = None
                    else:
                        try:
                            value = float(value) if '.' in value else int(value)
                        except Exception:
                            pass
                self.env[node.name] = value


            elif isinstance(node, IncrementStatement):
                if node.name not in self.env:
                    raise RuntimeError(f"Variable '{node.name}' not defined")
                val = self.env[node.name]
                amt = node.amount
                # If amt is a variable name, resolve it
                if isinstance(amt, str):
                    if amt in self.env:
                        amt = self.env[amt]
                    else:
                        v = amt.lower()
                        if v == "true":
                            amt = True
                        elif v == "false":
                            amt = False
                        elif v in ("null", "none", "nothing"):
                            amt = None
                        else:
                            try:
                                amt = float(amt) if '.' in amt else int(amt)
                            except Exception:
                                raise RuntimeError(f"Cannot increment by non-numeric value '{node.amount}'")
                if isinstance(val, (int, float)) and isinstance(amt, (int, float)):
                    self.env[node.name] = val + amt
                else:
                    raise RuntimeError(f"Cannot increment non-numeric variable '{node.name}'")


            elif isinstance(node, WriteStatement) or isinstance(node, WhisperStatement):
                # If the name is a string literal, print it directly
                if isinstance(node.name, str) and node.name.startswith('"') and node.name.endswith('"'):
                    val = node.name[1:-1]
                elif node.name in self.env:
                    val = self.env[node.name]
                    if val is True:
                        val = "true"
                    elif val is False:
                        val = "false"
                    elif val is None:
                        val = "nothing"
                else:
                    raise RuntimeError(f"Variable '{node.name}' not defined")
                if isinstance(node, WriteStatement):
                    print(val)
                else:
                    print(val, end="")

            elif isinstance(node, ForLoopStatement):
                for i in range(node.start, node.end + 1):
                    self.env[node.var_name] = i
                    self.execute(node.body)

            elif isinstance(node, WhileLoopStatement):
                while node.condition(self.env):
                    self.execute(node.body)


            elif isinstance(node, RepeatLoopStatement):
                for _ in range(node.times):
                    self.execute(node.body)

            elif isinstance(node, RepeatUntilLoopStatement):
                while True:
                    self.execute(node.body)
                    if self.env.get(node.var_name) == node.value:
                        break
