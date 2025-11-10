from _interpreter.environment import standard_env
from _interpreter.evaluator import evaluate
from _interpreter.lexer import Lexer
from _interpreter.parser import Parser

if __name__ == "__main__":
    # input = """5 + 5 + 5 + 5 - 10;
    # 2 * 2 * 2 * 2 * 2;
    # -50 + 100 + -50;
    # 5 * 2 + 10;
    # 5 + 2 * 10;
    # 20 + 2 * -10;
    # 50 / 2 * 2 + 10;
    # 2 * (5 + 10);
    # 3 * 3 * 3 + 10;
    # 3 * (3 * 3) + 10;
    # (5 + 10 * 2 + 15 / 3) * 2 + -10;
    # 50 / 3 * 2 + 10;
    # """
    # input = """True;
    # False;
    # 1 < 2;
    # 1 <= 2;
    # 1 > 2;
    # 1 >= 2;
    # 1 < 1;
    # 1 <= 1;
    # 1 > 1;
    # 1 >= 1;
    # 1 == 1;
    # 1 != 1;
    # 1 == 2;
    # 1 != 2;
    # True == True;
    # True == False;
    # False == False;
    # False == True;
    # True != True;
    # True != False;
    # False != False;
    # False != True;
    # """
    # input = """(1 < 2) == True;
    # 1 < 2 == True;
    # """
    # input = """
    # if (5 * 5 + 10 > 34) { 99; } else { 100; };
    # if (1 > 2) { 10; };
    # if (1 < 2) { 10; };
    # """
    # input = """
    # {return 10;}
    # {return 10; 9;}
    # {return 2 * 5; 9;}
    # {9; return 2 * 5; 9;}
    # if (10 > 1) { if (10 > 1) { return 10; }; return 1; };
    # """
    # input = """
    #     let x = if (10 > 1) { if (10 > 1) { return 10; }; return 1; };
    #     let y = 20;
    #     x + y;
    # """
    # input = "if (10 > 1) { if (10 > 1) { return 10; }; return 1; };"
    #     input = """
    #     let a = 5;
    #     let b = a > 3;
    #     let c = a * 99;
    #     if (b) { 10; } else { 1; };
    #     let d = if (c > a) { 99; } else { 100; };
    #     d * c * a;
    # """
    # input = """
    # let add = fn(a, b, c, d) { return a + b + c + d; };
    # add(1, 2, 3, 4);
    # let multiply = fn(x, y) { x * y;};
    # multiply(50 / 2, 1 * 2);
    # fn(x) { x == 10; }(5);
    # """
    input = """
    let newAdder = fn(x) {fn(y) { x + y ;};};
    let addTwo = newAdder(2);
    addTwo(3);
    """
    env = standard_env()
    program = Parser(Lexer(input)).parse(False)
    print(f"{program!r}")
    # print("-" * 80)
    print(evaluate(program, env))
    print("-" * 80)
    for stmt in program.statements:
        print(evaluate(stmt))
