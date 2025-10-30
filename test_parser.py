from _interpreter.lexer import Lexer
from _interpreter.parser import Parser

if __name__ == "__main__":
    input = """
let x = 5;
let y = 10;
let foobar = 838383;
"""
    lexer = Lexer(input)
    for tok in lexer:
        print(tok)
    parser = Parser(lexer)
    program = parser.parse()
    for stmt in program.statements:
        print(stmt)
