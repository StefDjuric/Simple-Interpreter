import interpreter
from lexer import Lexer


def main():
    while True:
        try:
            text = input('spi> ')
        except EOFError:
            break
        if not text:
            continue

        lexer = Lexer(text)
        parser = interpreter.Parser(lexer)
        this_interpreter = interpreter.Interpreter(parser)
        this_interpreter.interpret()
        print(this_interpreter.GLOBAL_SCOPE)


if __name__ == '__main__':
    main()
