from _interpreter.lexer import Lexer
from _interpreter.parser import Parser


def show_parsed_program(input: str, debug: bool = True):
    parser = Parser(Lexer(input))
    # for stmt in parser.parse().statements:
    #     print(stmt)
    #     print(f"{stmt!r}")
    p = parser.parse(debug)
    # print(BlockStatement(p.statements))
    print(p)
    # print(f"{p!r}")


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
    input = """
    let add = fn(a,){return x + y + z;};
    add(1,);
    a + add(b * c) + d;
    add(a, b, 1, 2 * 3, 4 + 5, add(6, 7 * 8));
    add(a + b + c * d / f + g);
"""
    # parser = Parser(Lexer(input))
    # program = parser.parse()
    # print(BlockStatement(*program.statements))
    # print(BlockStatement())
    # print("\n  ".join([str(stmt) for stmt in program.statements]))

    show_parsed_program(input, False)
