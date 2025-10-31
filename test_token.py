from _interpreter.tokens import Token, TokenType

if __name__ == "__main__":
    tk = Token(TokenType.IDENTIFIER, "name")

    print(tk)
    print(tk.type)
    print(tk.literal)

    tk.type = TokenType.ADD
