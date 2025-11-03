from _interpreter.lexer import Lexer
from _interpreter.parser import Parser
from _interpreter.tokens import Token, TokenType


def show_parsed_program(input: str):
    parser = Parser(Lexer(input))
    for stmt in parser.parse().statements:
        print(stmt)
        print(f"{stmt!r}")
    print(parser.parse())


if __name__ == "__main__":
    #     input = """
    # let x = 5;
    # let y = 10;
    # let foobar = 838383;
    # """
    #     show_parsed_program(input)
    #     input2 = """
    # return 5;
    # return 10;
    # return 993 322;
    # """
    #     show_parsed_program(input2)

    # show_parsed_program("foobar;")

    # print(parse_integer_literal(Token(TokenType.INTEGER, "0x12b")))
    show_parsed_program("-5;")
