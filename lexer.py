import my_tokens

RESERVED_KEYWORDS = {
    'PROGRAM': my_tokens.Token('PROGRAM', 'PROGRAM'),
    'VAR': my_tokens.Token('VAR', 'VAR'),
    'DIV': my_tokens.Token('INTEGER_DIV', 'DIV'),
    'INTEGER': my_tokens.Token('INTEGER', 'INTEGER'),
    'REAL': my_tokens.Token('REAL', 'REAL'),
    'BEGIN': my_tokens.Token('BEGIN', 'BEGIN'),
    'END': my_tokens.Token('END', 'END'),
    'PROCEDURE': my_tokens.Token('PROCEDURE', 'PROCEDURE')
}


class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.curr_idx_position = 0
        self.current_char = self.text[self.curr_idx_position]

    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        """Advance the `curr_idx_position` pointer and set the `current_char` variable."""
        self.curr_idx_position += 1
        if self.curr_idx_position > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.curr_idx_position]

    def peek(self):
        peek_curr_idx_position = self.curr_idx_position + 1
        if peek_curr_idx_position > len(self.text) - 1:
            return None
        else:
            return self.text[peek_curr_idx_position]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        while self.current_char != '}':
            self.advance()
        self.advance()  # the closing curly brace

    def number(self):
        """Return a (multidigit) integer or float consumed from the input."""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        if self.current_char == '.':
            result += self.current_char
            self.advance()

            while (
                self.current_char is not None and
                self.current_char.isdigit()
            ):
                result += self.current_char
                self.advance()

            token = my_tokens.Token('REAL_CONST', float(result))
        else:
            token = my_tokens.Token('INTEGER_CONST', int(result))

        return token

    def _id(self):
        """Handle identifiers and reserved keywords"""
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()

        my_token = RESERVED_KEYWORDS.get(result.upper(), my_tokens.Token(my_tokens.ID, result))
        return my_token

    def tokenizer(self):
        """Lexical analyzer (also known as scanner or my_tokens.Tokennizer)

        This method is responsible for breaking a sentence
        apart into my_tokens.Tokens. One my_tokens.Token at a time.
        """
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char == '{':
                self.advance()
                self.skip_comment()
                continue

            if self.current_char.isalpha():
                return self._id()

            if self.current_char.isdigit():
                return self.number()

            if self.current_char == ':' and self.peek() == '=':
                self.advance()
                self.advance()
                return my_tokens.Token(my_tokens.ASSIGN, ':=')

            if self.current_char == ';':
                self.advance()
                return my_tokens.Token(my_tokens.SEMI, ';')

            if self.current_char == ':':
                self.advance()
                return my_tokens.Token(my_tokens.COLON, ':')

            if self.current_char == ',':
                self.advance()
                return my_tokens.Token(my_tokens.COMMA, ',')

            if self.current_char == '+':
                self.advance()
                return my_tokens.Token(my_tokens.PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return my_tokens.Token(my_tokens.MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return my_tokens.Token(my_tokens.MULTIPLY, '*')

            if self.current_char == '/':
                self.advance()
                return my_tokens.Token(my_tokens.FLOAT_DIV, '/')

            if self.current_char == '(':
                self.advance()
                return my_tokens.Token(my_tokens.LPARAN, '(')

            if self.current_char == ')':
                self.advance()
                return my_tokens.Token(my_tokens.RPARAN, ')')

            if self.current_char == '.':
                self.advance()
                return my_tokens.Token(my_tokens.DOT, '.')

            self.error()

        return my_tokens.Token(my_tokens.EOF, None)
