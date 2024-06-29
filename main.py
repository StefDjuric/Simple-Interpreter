import interpreter
import lexer
from lexer import Lexer
import sys


def main():
    text = """
    program SymTab4;
        var x, y : integer;

    begin
        x := x + y;
    end.
    """
    my_lexer = Lexer(text)
    parser = interpreter.Parser(my_lexer)
    tree = parser.parse()

    semantic_analyzer = interpreter.SemanticAnalyzer()
    semantic_analyzer.visit(tree)

    print(semantic_analyzer.symtab)


if __name__ == '__main__':
    main()
