import token


class Lexer(object):
    def __init__(self, text):
        # text as in code that gets interpreted
        self.text = text.replace(' ', '')
        # index position of text
        self.curr_idx_position = 0
        self.curr_char = self.text[self.curr_idx_position]

    def error(self) -> None:
        raise Exception('Invalid character')

    def advance(self):
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

    def tokenizer(self) -> token.Token:
        """This method breaks text down into tokens"""

        while self.curr_char is not None:

            if self.curr_char.isdigit():
                return token.Token(token.INTEGER, self.integer())

            elif self.curr_char == '+':
                self.advance()
                return token.Token(token.PLUS, self.curr_char)

            elif self.curr_char == '-':
                self.advance()
                return token.Token(token.MINUS, self.curr_char)

            elif self.curr_char == '*':
                self.advance()
                return token.Token(token.MULTIPLY, self.curr_char)

            elif self.curr_char == '/':
                self.advance()
                return token.Token(token.DIVIDE, self.curr_char)

            self.error()

        return token.Token(token.EOF, None)
