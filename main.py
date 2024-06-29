import interpreter
from lexer import Lexer
import sys


def main():
    text = open(sys.argv[1], 'r').read()

    my_lexer = Lexer(text)
    my_parser = interpreter.Parser(my_lexer)
    tree = my_parser.parse()
    symtab_builder = interpreter.SymbolTableBuilder()
    symtab_builder.visit(tree)
    print('')
    print('Symbol Table contents:')
    print(symtab_builder.symbol_table)

    my_interpreter = interpreter.Interpreter(tree)
    result = my_interpreter.interpret()

    print('')
    print('Run-time GLOBAL_MEMORY contents:')
    for k, v in sorted(my_interpreter.GLOBAL_MEMORY.items()):
        print('{} = {}'.format(k, v))


if __name__ == '__main__':
    main()
