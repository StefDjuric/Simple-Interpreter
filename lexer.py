import my_tokens

RESERVED_KEYWORDS = {
    'BEGIN': my_tokens.Token('BEGIN', 'BEGIN'),
    'END': my_tokens.Token('END', 'END'),
}


class Lexer(object):
    def __init__(self, text):
        # text as in code that gets interpreted
        self.text = text
        # index position of text
        self.curr_idx_position = 0
        self.curr_char = self.text[self.curr_idx_position]

    def error(self) -> None:
        raise Exception('Invalid character')

    def skip_whitespace(self):
        while self.curr_char is not None and self.curr_char.isspace():
            self.advance()

    def advance(self) -> None:
        """Advance the 'curr_idx_position' pointer and set the 'current_char' variable."""
        self.curr_idx_position += 1
        if self.curr_idx_position > len(self.text) - 1:
            self.curr_char = None  # Indicates end of input
        else:
            self.curr_char = self.text[self.curr_idx_position]

    def integer(self):
        """Returns a (multi digit) integer consumed from the input."""
        integer_buffer = ''
        while self.curr_char is not None and self.curr_char.isdigit():
            integer_buffer += self.curr_char
            self.advance()
        return int(integer_buffer)

    def peek(self):
        """Peeks into the next position of the text without moving the index position"""
        peek_pos = self.curr_idx_position + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def _id(self):
        """Handles identifiers and reserved keywords"""
        result = ''
        while self.curr_char is not None and self.curr_char.isalnum():
            result += self.curr_char
            self.advance()
        this_token = RESERVED_KEYWORDS.get(result.upper(), my_tokens.Token(my_tokens.ID, result))
        return this_token

    def tokenizer(self) -> my_tokens.Token:
        """This method breaks text down into tokens"""

        while self.curr_char is not None:

            if self.curr_char.isdigit():
                return my_tokens.Token(my_tokens.INTEGER, self.integer())

            elif self.curr_char.isspace():
                self.skip_whitespace()
                continue

            elif self.curr_char.isalpha():
                return self._id()

            elif self.curr_char == ':' and self.peek() == '=':
                self.advance()
                self.advance()
                return my_tokens.Token(my_tokens.ASSIGN, ':=')

            elif self.curr_char == ';':
                self.advance()
                return my_tokens.Token(my_tokens.SEMI, ';')

            elif self.curr_char == '.':
                self.advance()
                return my_tokens.Token(my_tokens.DOT, '.')

            elif self.curr_char == '+':
                self.advance()
                return my_tokens.Token(my_tokens.PLUS, '+')

            elif self.curr_char == '-':
                self.advance()
                return my_tokens.Token(my_tokens.MINUS, '-')

            elif self.curr_char == '*':
                self.advance()
                return my_tokens.Token(my_tokens.MULTIPLY, '*')

            elif self.curr_char == '/':
                self.advance()
                return my_tokens.Token(my_tokens.DIVIDE, '/')

            elif self.curr_char == '(':
                self.advance()
                return my_tokens.Token(my_tokens.LPARAN, '(')

            elif self.curr_char == ')':
                self.advance()
                return my_tokens.Token(my_tokens.RPARAN, ')')

            self.error()

        return my_tokens.Token(my_tokens.EOF, None)
