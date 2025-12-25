class Tokeniser:
    def tokenise(code):
        tokens = []
        lines = code.splitlines()
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            words = line.split()
            tokens.extend(words)
            tokens.append("NEWLINE")
        return tokens