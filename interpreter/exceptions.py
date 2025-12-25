class InterpreterError(Exception):
    """Base class for all interpreter errors"""
    pass

class SyntaxError(InterpreterError):
    """Raised when the source code has invalid syntax"""
    pass

class RuntimeError(InterpreterError):
    """Raised when execution fails, e.g., undefined variable"""
    pass
