from _interpreter import Lexer

if __name__ == "__main__":
    input = """
    let name = "Remilia Scarlet";
"""

    print(list(Lexer(input)))
