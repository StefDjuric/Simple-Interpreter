
# Token types:
INTEGER, PLUS, EOF, MINUS = 'INTEGER', 'PLUS', 'EOF', 'MINUS'


class Token(object):

    def __init__(self, type, value):
        self.type = type
        # Value can be 0-9 or PLUS or None
        self.value = value

    def __str__(self):
        """String representation of the instance of class Token"""

        return 'Token({type}, {value})'.format(type=self.type, value=repr(self.value))

    def __repr__(self):
        """Returns the string representation of class instance Token"""
        return self.__str__()


