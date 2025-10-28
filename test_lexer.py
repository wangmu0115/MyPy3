from _interpreter import Lexer, Token, TokenType

if __name__ == "__main__":
    l = Lexer("     =+ab_1*=;>,!=,12;     ")

    for t in l:
        print(t)

    # tok: Token = l.next_token()
    # while not tok.is_end():
    #     print(tok)
    #     tok = l.next_token()
    print("-" * 50)

    s = "*="
