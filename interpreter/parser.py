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

        def parse_value_tokens(tokens, start):
            # Collect tokens for a value expression (including + for concatenation/addition)
            value_tokens = []
            i = start
            while i < len(tokens):
                t = tokens[i]
                if t in ("NEWLINE", "end", "do", "then", "else", "to", "times"):  # statement boundaries, now includes 'to' and 'times'
                    break
                value_tokens.append(t)
                i += 1
            # Now join tokens for parse_value
            value_str = ' '.join(value_tokens)
            return parse_value(value_str), i

        def parse_value(tok):
            # String concatenation support: split by +, parse each part, then join if any part is a string
            if '+' in tok:
                parts = [p.strip() for p in tok.split('+')]
                parsed = [parse_value(p) for p in parts]
                if any(isinstance(x, str) for x in parsed):
                    return ''.join(str(x) for x in parsed)
                else:
                    # If all are numbers, do numeric addition
                    result = parsed[0]
                    for p in parsed[1:]:
                        result += p
                    return result
            # Boolean not support: 'not' keyword
            if tok.lower().startswith('not '):
                inner = tok[4:].strip()
                val = parse_value(inner)
                return not val
            # Strings
            if tok.startswith('"') and tok.endswith('"'):
                return tok[1:-1]
            # Booleans
            if tok.lower() == "true":
                return True
            if tok.lower() == "false":
                return False
            # Null/nothing
            if tok.lower() in ("null", "none", "nothing"):
                return None
            # Floats and ints
            try:
                if '.' in tok:
                    return float(tok)
                else:
                    return int(tok)
            except ValueError:
                # Allow variable names or expressions
                return tok

        def parse_block(tokens, start):
            ast = []
            i = start
            while i < len(tokens):
                token = tokens[i]


                if token == "set":
                    name = tokens[i + 1]
                    if tokens[i + 2] != "to":
                        raise Exception("Expected 'to' after variable name")
                    value, next_i = parse_value_tokens(tokens, i + 3)
                    ast.append(SetStatement(name, value))
                    i = next_i


                elif token == "change":
                    name = tokens[i + 1]
                    if tokens[i + 2] == "to":
                        value, next_i = parse_value_tokens(tokens, i + 3)
                        ast.append(ChangeStatement(name, value))
                        i = next_i
                    elif tokens[i + 2] == "by":
                        amount, next_i = parse_value_tokens(tokens, i + 3)
                        ast.append(IncrementStatement(name, amount))
                        i = next_i
                    else:
                        raise Exception("Expected 'to' or 'by' after variable name in change statement")


                elif token == "write" or token == "whisper":
                    name_token = tokens[i + 1]
                    # If the token is a quoted string, join tokens until the closing quote
                    if name_token.startswith('"') and not name_token.endswith('"'):
                        # Multi-token string literal
                        j = i + 2
                        name_parts = [name_token]
                        while j < len(tokens):
                            name_parts.append(tokens[j])
                            if tokens[j].endswith('"'):
                                break
                            j += 1
                        name = ' '.join(name_parts)
                        i = j + 1
                    else:
                        name = name_token
                        i += 2
                    if token == "write":
                        ast.append(WriteStatement(name))
                    else:
                        ast.append(WhisperStatement(name))


                elif token == "for":
                    if tokens[i+1] != "each":
                        raise Exception("Expected 'each' after 'for'")
                    var_name = tokens[i+2]
                    if tokens[i+3] != "from":
                        raise Exception("Expected 'from' after variable name in for loop")
                    start_val, next_i = parse_value_tokens(tokens, i+4)
                    if tokens[next_i] != "to":
                        raise Exception("Expected 'to' after start value in for loop")
                    end_val, next_i2 = parse_value_tokens(tokens, next_i+1)
                    if tokens[next_i2] != "do":
                        raise Exception("Expected 'do' after end value in for loop")
                    i = next_i2 + 1
                    body, i = parse_block(tokens, i)
                    if tokens[i] != "end":
                        raise Exception("Expected 'end' after for loop body")
                    ast.append(ForLoopStatement(var_name, start_val, end_val, body))
                    i += 1


                elif token == "while":
                    var_name = tokens[i+1]
                    if tokens[i+2] == "is" and tokens[i+3] == "less" and tokens[i+4] == "than":
                        op = "<"
                        value, next_i = parse_value_tokens(tokens, i+5)
                        do_idx = next_i
                    elif tokens[i+2] == "is" and tokens[i+3] == "greater" and tokens[i+4] == "than":
                        op = ">"
                        value, next_i = parse_value_tokens(tokens, i+5)
                        do_idx = next_i
                    elif tokens[i+2] == "is" and tokens[i+3] == "not":
                        op = "!="
                        value, next_i = parse_value_tokens(tokens, i+4)
                        do_idx = next_i
                    elif tokens[i+2] == "is":
                        op = "=="
                        value, next_i = parse_value_tokens(tokens, i+3)
                        do_idx = next_i
                    else:
                        raise Exception("Invalid while condition syntax")
                    if tokens[do_idx] != "do":
                        raise Exception("Expected 'do' after while condition")
                    cond_expr = f"{var_name} {op} {repr(value)}"
                    i = do_idx + 1
                    body, i = parse_block(tokens, i)
                    if tokens[i] != "end":
                        raise Exception("Expected 'end' after while loop body")
                    ast.append(WhileLoopStatement(cond_expr, body))
                    i += 1


                elif token == "repeat":
                    times, next_i = parse_value_tokens(tokens, i+1)
                    if tokens[next_i] != "times":
                        raise Exception("Expected 'times' after repeat count")
                    if tokens[next_i+1] != "do":
                        raise Exception("Expected 'do' after repeat times")
                    i = next_i + 2
                    body, i = parse_block(tokens, i)
                    if tokens[i] != "end":
                        raise Exception("Expected 'end' after repeat loop body")
                    ast.append(RepeatLoopStatement(times, body))
                    i += 1


                elif token == "test":
                    # test <left> is <right>
                    left_token = tokens[i+1]
                    if tokens[i+2] == "is":
                        if len(tokens) > i+3 and tokens[i+3] == "not":
                            op = "is not"
                            right, next_i = parse_value_tokens(tokens, i+4)
                            i = next_i
                        else:
                            op = "is"
                            right, next_i = parse_value_tokens(tokens, i+3)
                            i = next_i
                    else:
                        raise Exception("Invalid test statement syntax")
                    left = parse_value(left_token)
                    ast.append(TestStatement(left, op, right))


                elif token == "if":
                    # if <var> is <value> do ... else ... end
                    var_name = tokens[i+1]
                    if tokens[i+2] == "is" and tokens[i+3] == "not":
                        op = "!="
                        value, next_i = parse_value_tokens(tokens, i+4)
                        do_idx = next_i
                    elif tokens[i+2] == "is":
                        op = "=="
                        value, next_i = parse_value_tokens(tokens, i+3)
                        do_idx = next_i
                    else:
                        raise Exception("Invalid if condition syntax")
                    if tokens[do_idx] != "do":
                        raise Exception("Expected 'do' after if condition")
                    cond_expr = f"{var_name} {op} {repr(value)}"
                    i = do_idx + 1

                    if_body, i = parse_block(tokens, i)
                    # Skip NEWLINE tokens after block
                    while i < len(tokens) and tokens[i] == "NEWLINE":
                        i += 1
                    else_body = None
                    if i < len(tokens) and tokens[i] == "else":
                        i += 1
                        else_body, i = parse_block(tokens, i)
                        while i < len(tokens) and tokens[i] == "NEWLINE":
                            i += 1

                    if i >= len(tokens):
                        raise Exception("Expected 'end' after if/else body")
                    if tokens[i] == "end":
                        ast.append(IfElseStatement(cond_expr, if_body, else_body))
                        i += 1
                    else:
                        # Not 'end' or 'else', so return to parent block to handle next statement
                        ast.append(IfElseStatement(cond_expr, if_body, else_body))
                        return ast, i

                elif token == "NEWLINE":
                    i += 1

                elif token == "end":
                    break

                else:
                    # If we return from a nested block, propagate the updated index
                    return ast, i
            return ast, i

        ast, _ = parse_block(tokens, 0)
        return ast
