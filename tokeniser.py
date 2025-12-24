class Tokeniser:
    def tokenise(code):
        tokens = []
        lines = code.splitlines()
        for line in lines:
            words = line.split()
            tokens.extend(words)
            tokens.append("NEWLINE")
        return tokens