import interpreter
from lexer import Lexer
import sys


def main():
    text = open(sys.argv[1], 'r').read()

    my_lexer = Lexer(text)
    parser = interpreter.Parser(my_lexer)
    this_interpreter = interpreter.Interpreter(parser)
    result = this_interpreter.interpret()

    for k, v in sorted(this_interpreter.GLOBAL_SCOPE.items()):
        print('{} = {}'.format(k, v))


if __name__ == '__main__':
    main()
