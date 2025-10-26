Symbol = str  # A Scheme Symbol is implemented as a Python str
Number = (int, float)  # A Scheme Number is implemented as a Python int or float
Atom = (Symbol, Number)  # A Scheme Atom is a Symbol or Number
List = list  # A Scheme List is implemented as a Python list
Exp = (Atom, List)  # A Scheme expression is an Atom or List
Env = dict  # A Scheme environment (defined below)
# is a mapping of {variable: value}


def tokenize(chars: str) -> list[str]:
    """Convert a string of characters into a list of tokens."""
    return chars.replace("(", " ( ").replace(")", " ) ").split()


def parse(program: str) -> Exp:
    return read_from_tokens(tokenize(program))


def read_from_tokens(tokens: list[str]) -> Exp:
    """Read an expression from a sequence of tokens."""
    if len(tokens) == 0:
        raise SyntaxError("unexcepted EOF")
    token = tokens.pop(0)
    if token == "(":
        L = []
        while tokens[0] != ")":
            L.append(read_from_tokens(tokens))
        tokens.pop(0)  # pop off `)`
        return L
    elif token == ")":
        raise SyntaxError("unexcepted )")
    else:
        return atom(token)


def atom(token: str) -> Atom:
    """Numbers become numbers; every other token is a symbol."""
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return Symbol(token)


if __name__ == "__main__":
    program = "(begin (define r 10) (* pi (* r r)))"
    print(tokenize(program))
    print(parse(program))
