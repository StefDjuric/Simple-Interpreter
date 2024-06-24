import token


class Interpreter(object):

    def __init__(self, text):
        # text as in code that gets interpreted
        self.text = text.replace(' ', '')
        # index position of text
        self.curr_idx_position = 0
        self.curr_token: token.Token = None
        self.curr_char = self.text[self.curr_idx_position]

    def error(self) -> None:
        raise Exception('Error parsing input')

    def advance(self):
        """Advance the 'curr_idx_position' pointer and set the 'current_char' variable."""
        self.curr_idx_position += 1
        if self.curr_idx_position > len(self.text) - 1:
            self.curr_char = None  # Indicates end of input
        else:
            self.curr_char = self.text[self.curr_idx_position]

    def integer(self):
        """Return a (multidigit) integer consumed from the input."""
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

            self.error()

        return token.Token(token.EOF, None)

    def eat(self, token_type) -> None:

        if self.curr_token.type == token_type:
            self.curr_token = self.tokenizer()
        else:
            self.error()

    def expression(self) -> int:
        """INTEGER PLUS INTEGER"""
        self.curr_token = self.tokenizer()

        left = self.curr_token
        self.eat('INTEGER')

        operand = self.curr_token
        if operand.type == token.PLUS:
            self.eat('PLUS')
        elif operand.type == token.MINUS:
            self.eat('MINUS')

        right = self.curr_token
        self.eat('INTEGER')

        if operand.type == token.PLUS:
            return left.value + right.value
        elif operand.type == token.MINUS:
            return left.value - right.value
