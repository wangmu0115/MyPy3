from _interpreter import Token, TokenType


class Lexer:
    def __init__(self, input: str):
        self.input = input
        self.__tokentypes = {tt.value: tt for tt in TokenType}

    def __iter__(self):
        position = 0
        while position < len(self.input):
            ch = self.input[position]
            match ch:
                case " " | "\r" | "\n" | "\t":
                    pass  # 跳过空白字符
                case "=" | "!" | "<" | ">" | "+" | "-" | "*" | "/" | "&" | "|":
                    _op = _read_op(self.input, position)
                    position += len(_op) - 1
                    yield Token(self.__tokentypes[_op])
                case "," | ";" | "(" | ")" | "{" | "}":
                    yield Token(self.__tokentypes[ch])
                case _:
                    _literal, _type = ch, TokenType.ILLEGAL  # 默认非法字符
                    if _is_letter(ch):  # 提取标识符
                        _literal = _read_identifier(self.input, position)
                        _type = self.__tokentypes.get(_literal, TokenType.IDENTIFIER)  # 标识符或者关键字
                        position += len(_literal) - 1
                    elif _is_digit(ch):
                        _literal = _read_number(self.input, position)
                        _type = TokenType.INTEGER
                        position += len(_literal) - 1

                    yield Token(_type, _literal)
            position += 1


def _read_op(s: str, position: int) -> str:
    """提取运算符, s[position]是运算符, 进一步判断是否是就地赋值运算符"""
    if position >= len(s) - 1:
        return s[position]
    match s[position + 1]:
        case "=":
            return s[position : position + 2]
        case _:
            return s[position]


def _read_identifier(s: str, start_position: int) -> str:
    end_position = start_position + 1
    while end_position < len(s):
        ch = s[end_position]
        if _is_letter(ch) or _is_digit(ch):
            end_position += 1
        else:
            break
    return s[start_position:end_position]


def _read_number(s: str, start_position: int) -> str:
    end_position = start_position + 1
    while end_position < len(s):
        ch = s[end_position]
        if _is_digit(ch):
            end_position += 1
        else:
            break
    return s[start_position:end_position]


def _is_letter(ch: str) -> bool:
    # ord("a") = 97, ord("z") = 122, ord("A") = 65, ord("Z") = 90, ord("_") = 95
    ordinal = ord(ch)
    return (ordinal >= 65 and ordinal <= 90) or (ordinal >= 97 and ordinal <= 122) or ordinal == 95


def _is_digit(ch: str) -> bool:
    return ch in list("0123456789")
