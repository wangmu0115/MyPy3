from _interpreter import Lexer


def print_lexer_tokens(input: str):
    lexer = Lexer(input)
    print(f"{input}\n{'*' * 80}")
    for token in lexer:
        print(token)
    print("=" * 80)


if __name__ == "__main__":
    input = """let name = "Remilia Scarlet";
let integer = "hello world";"""
    print_lexer_tokens(input)

    input = '"$$#";'
    print_lexer_tokens(input)

    input = "0.123;0x12B;1e-6;1e+7 12;0.1E12;1e0.3;0x;1-6;1+6; 0.123e1e2"
    print_lexer_tokens(input)
