# Token types:
(INTEGER, PLUS, EOF, MINUS,
 DIVIDE, MULTIPLY,
 LPARAN, RPARAN, BEGIN,
 END, DOT, ASSIGN,
 SEMI, ID, PROGRAM, VAR, INTEGER_DIV,
 FLOAT_DIV, COLON, COMMA,
 REAL, INTEGER_CONST, REAL_CONST,) = ('INTEGER', 'PLUS', 'EOF', 'MINUS', 'DIVIDE',
                                      'MULTIPLY', '(', ')', 'BEGIN',
                                      'END', 'DOT', 'ASSIGN', 'SEMI', 'ID', 'PROGRAM',
                                      'VAR', 'INTEGER_DIV', 'FLOAT_DIV', 'COLON', 'COMMA', 'REAL', 'INTEGER_CONST',
                                      'REAL_CONST')


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
