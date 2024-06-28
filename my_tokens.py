# Token types:
INTEGER = 'INTEGER'
REAL = 'REAL'
INTEGER_CONST = 'INTEGER_CONST'
REAL_CONST = 'REAL_CONST'
PLUS = 'PLUS'
MINUS = 'MINUS'
MULTIPLY = 'MULTIPLY'
INTEGER_DIV = 'INTEGER_DIV'
FLOAT_DIV = 'FLOAT_DIV'
LPARAN = 'LPAREN'
RPARAN = 'RPAREN'
ID = 'ID'
ASSIGN = 'ASSIGN'
BEGIN = 'BEGIN'
END = 'END'
SEMI = 'SEMI'
DOT = 'DOT'
PROGRAM = 'PROGRAM'
VAR = 'VAR'
COLON = 'COLON'
COMMA = 'COMMA'
EOF = 'EOF'


class Token(object):

    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        """String representation of the instance of class Token"""

        return 'Token({type}, {value})'.format(type=self.type, value=repr(self.value))

    def __repr__(self):
        """Returns the string representation of class instance Token"""
        return self.__str__()
