import token
import AST


class Parser(object):
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

    def factor(self):
        """Returns a operator or number node taken value """

        this_token = self.curr_token

        if this_token.type == token.INTEGER:
            self.eat('INTEGER')
            return AST.Number(this_token)

        elif this_token.type == token.PLUS:
            self.eat('PLUS')
            node = AST.UnaryOperatorNode(this_token, self.factor())
            return node

        elif this_token.type == token.MINUS:
            self.eat('MINUS')
            node = AST.UnaryOperatorNode(this_token, self.factor())
            return node

        elif this_token.type == token.LPARAN:
            self.eat(token.LPARAN)
            node = self.expression()
            self.eat(token.RPARAN)
            return node

    def term(self) -> AST.BinaryOperatorNode:
        """Returns the value of a higher priority (DIV, MUL) expression"""
        # self.curr_token = self.tokenizer()

        node = self.factor()

        while self.curr_token.type in (token.MULTIPLY, token.DIVIDE):
            this_token = self.curr_token

            if this_token.type == token.MULTIPLY:
                self.eat('MULTIPLY')
                # result *= self.factor()
            elif this_token.type == token.DIVIDE:
                self.eat('DIVIDE')
                # result /= self.factor()

            node = AST.BinaryOperatorNode(left_node=node, operator=this_token, right_node=self.factor())
        return node

    def expression(self) -> AST.BinaryOperatorNode:
        # Priority expression
        node = self.term()

        while self.curr_token.type in (token.PLUS, token.MINUS):
            this_token = self.curr_token
            if this_token.type == token.PLUS:
                self.eat('PLUS')
                # result += self.term()
            elif this_token.type == token.MINUS:
                self.eat('MINUS')
                # result -= self.term()
            node = AST.BinaryOperatorNode(left_node=node, operator=this_token, right_node=self.term())
        return node

    def parse(self):
        return self.expression()


class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node.__name__)))


class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser

    def visit_BinaryOperatorNode(self, node: AST.BinaryOperatorNode):
        if node.operator.type == token.PLUS:
            return self.visit(node.left_node) + self.visit(node.right_node)
        elif node.operator.type == token.MINUS:
            return self.visit(node.left_node) - self.visit(node.right_node)
        elif node.operator.type == token.MULTIPLY:
            return self.visit(node.left_node) * self.visit(node.right_node)
        elif node.operator.type == token.DIVIDE:
            return self.visit(node.left_node) / self.visit(node.right_node)

    def visit_UnaryOperatorNode(self, node: AST.UnaryOperatorNode):
        operator = node.operator.type

        if operator == token.PLUS:
            return +self.visit(node.expression)
        elif operator == token.MINUS:
            return -self.visit(node.expression)

    def visit_Number(self, node: AST.Number):
        return node.value

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)
