import token


class Interpreter(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.curr_token: token.Token = self.lexer.tokenizer()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type) -> None:

        if self.curr_token.type == token_type:
            self.curr_token = self.lexer.tokenizer()
        else:
            self.error()

    def factor(self) -> int:
        """Returns an INTEGER taken value """

        this_token = self.curr_token
        self.eat('INTEGER')
        return this_token.value

    def term(self) -> int:
        """Returns the value of a higher priority (DIV, MUL) expression"""
        # self.curr_token = self.tokenizer()

        result = self.factor()

        while self.curr_token.type in (token.MULTIPLY, token.DIVIDE):
            this_token = self.curr_token

            if this_token.type == token.MULTIPLY:
                self.eat('MULTIPLY')
                result *= self.factor()
            elif this_token.type == token.DIVIDE:
                self.eat('DIVIDE')
                result /= self.factor()
        return result

    def expression(self):
        result = self.term()

        while self.curr_token.type in (token.PLUS, token.MINUS):
            this_token = self.curr_token
            if this_token.type == token.PLUS:
                self.eat('PLUS')
                result += self.term()
            elif this_token.type == token.MINUS:
                self.eat('MINUS')
                result -= self.term()
        return result







