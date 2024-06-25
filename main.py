import interpreter
from lexer import Lexer


def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue

        lexer = Lexer(text)
        interpret = interpreter.Interpreter(lexer)
        result = interpret.expression()
        print(result)


if __name__ == '__main__':
    main()
