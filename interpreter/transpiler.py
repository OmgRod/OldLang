"""
Transpiler for OldLang to Python
- Converts OldLang AST to Python code
- Usage: Transpiler.transpile(ast) returns Python code as a string
"""
from ast_nodes import *

class Transpiler:
    @staticmethod
    def transpile(ast):
        lines = []
        for stmt in ast:
            lines.extend(Transpiler.transpile_stmt(stmt, indent=0))
        return '\n'.join(lines)

    @staticmethod
    def transpile_stmt(stmt, indent=0):
        IND = '    ' * indent
        lines = []
        if isinstance(stmt, WhisperStatement):
            lines.append(f"{IND}print({Transpiler.transpile_value(stmt.name)}, end=\"\")")
            return lines
        IND = '    ' * indent
        lines = []
        if isinstance(stmt, SetStatement):
            lines.append(f"{IND}{stmt.name} = {Transpiler.transpile_value(stmt.value)}")
        elif isinstance(stmt, ChangeStatement):
            lines.append(f"{IND}{stmt.name} = {stmt.name} + {Transpiler.transpile_value(stmt.value)}")
        elif isinstance(stmt, IncrementStatement):
            lines.append(f"{IND}{stmt.name} = {stmt.name} + {Transpiler.transpile_value(stmt.amount)}")
        elif isinstance(stmt, WriteStatement):
            lines.append(f"{IND}print({Transpiler.transpile_value(stmt.name)})")
        elif isinstance(stmt, TestStatement):
            lines.append(f"{IND}assert {Transpiler.transpile_value(stmt.left)} == {Transpiler.transpile_value(stmt.right)}")
        elif isinstance(stmt, IfElseStatement):
            cond = stmt.condition_str if hasattr(stmt, 'condition_str') and stmt.condition_str else stmt.condition
            lines.append(f"{IND}if {cond}:")
            for s in stmt.if_body:
                lines.extend(Transpiler.transpile_stmt(s, indent+1))
            if stmt.else_body:
                lines.append(f"{IND}else:")
                for s in stmt.else_body:
                    lines.extend(Transpiler.transpile_stmt(s, indent+1))
        elif isinstance(stmt, ForLoopStatement):
            # Make the for-loop inclusive: range(start, end + 1)
            lines.append(f"{IND}for {stmt.var_name} in range({Transpiler.transpile_value(stmt.start)}, {Transpiler.transpile_value(stmt.end)} + 1):")
            for s in stmt.body:
                lines.extend(Transpiler.transpile_stmt(s, indent+1))
        elif isinstance(stmt, WhileLoopStatement):
            cond = stmt.condition_str if hasattr(stmt, 'condition_str') and stmt.condition_str else stmt.condition
            lines.append(f"{IND}while {cond}:")
            for s in stmt.body:
                lines.extend(Transpiler.transpile_stmt(s, indent+1))
        elif isinstance(stmt, RepeatLoopStatement):
            lines.append(f"{IND}for _ in range({Transpiler.transpile_value(stmt.times)}):")
            for s in stmt.body:
                lines.extend(Transpiler.transpile_stmt(s, indent+1))
        return lines

    @staticmethod
    def transpile_value(val):
        from ast_nodes import StringLiteral
        if isinstance(val, StringLiteral):
            # Emit as Python string literal
            return repr(str(val))
        if isinstance(val, str):
            # If it's a quoted string, emit as Python string literal
            if val.startswith('"') and val.endswith('"'):
                return repr(val[1:-1])
            # If it's a valid identifier, treat as variable (no quotes)
            if val.isidentifier():
                return val
            else:
                return repr(val)
        elif isinstance(val, bool):
            return 'True' if val else 'False'
        elif val is None:
            return 'None'
        elif isinstance(val, (int, float)):
            return str(val)
        elif isinstance(val, list):
            # For block/compound values
            return '[' + ', '.join(Transpiler.transpile_value(v) for v in val) + ']'
        else:
            return str(val)
