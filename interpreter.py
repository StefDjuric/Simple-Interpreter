import my_tokens
import AST


class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.curr_token: my_tokens.Token = self.lexer.tokenizer()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type) -> None:
        # TODO: fix errors (my_tokens.BEGIN) error
        if self.curr_token.type == token_type:
            self.curr_token = self.lexer.tokenizer()
        else:
            self.error()

    def empty(self):
        return AST.NoStatements()

    def variable(self):
        node = AST.Variable(self.curr_token)
        self.eat(my_tokens.ID)
        return node

    def assignment_statement(self):
        left = self.variable()
        this_token = self.curr_token
        self.eat(my_tokens.ASSIGN)
        right = self.expression()
        node = AST.Assign(left, this_token, right)
        return node

    def statement_list(self):
        node = self.statement()

        results = [node]
        while self.curr_token.type == my_tokens.SEMI:
            self.eat(my_tokens.SEMI)
            results.append(self.statement())

        if self.curr_token.type == my_tokens.ID:
            self.error()
        return results

    def compound_statement(self):
        self.eat(my_tokens.BEGIN)
        nodes = self.statement_list()
        self.eat(my_tokens.END)

        root = AST.Compound()
        for node in nodes:
            root.children.append(node)
        return root

    def statement(self):
        if self.curr_token.type == my_tokens.BEGIN:
            node = self.compound_statement()
        elif self.curr_token.type == my_tokens.ID:
            node = self.assignment_statement()
        else:
            node = self.empty()
        return node

    def program(self):
        node = self.compound_statement()
        self.eat(my_tokens.DOT)
        return node

    def factor(self):
        """Returns a operator or number node taken value """

        this_token = self.curr_token

        if this_token.type == my_tokens.INTEGER:
            self.eat('INTEGER')
            return AST.Number(this_token)

        elif this_token.type == my_tokens.PLUS:
            self.eat('PLUS')
            node = AST.UnaryOperatorNode(this_token, self.factor())
            return node

        elif this_token.type == my_tokens.MINUS:
            self.eat('MINUS')
            node = AST.UnaryOperatorNode(this_token, self.factor())
            return node

        elif this_token.type == my_tokens.LPARAN:
            self.eat(my_tokens.LPARAN)
            node = self.expression()
            self.eat(my_tokens.RPARAN)
            return node

        else:
            node = self.variable()
            return node

    def term(self) -> AST.BinaryOperatorNode:
        """Returns the value of a higher priority (DIV, MUL) expression"""
        # self.curr_token = self.tokenizer()

        node = self.factor()

        while self.curr_token.type in (my_tokens.MULTIPLY, my_tokens.DIVIDE):
            this_token = self.curr_token

            if this_token.type == my_tokens.MULTIPLY:
                self.eat('MULTIPLY')
                # result *= self.factor()
            elif this_token.type == my_tokens.DIVIDE:
                self.eat('DIVIDE')
                # result /= self.factor()

            node = AST.BinaryOperatorNode(left_node=node, operator=this_token, right_node=self.factor())
        return node

    def expression(self) -> AST.BinaryOperatorNode:
        # Priority expression
        node = self.term()

        while self.curr_token.type in (my_tokens.PLUS, my_tokens.MINUS):
            this_token = self.curr_token
            if this_token.type == my_tokens.PLUS:
                self.eat('PLUS')
                # result += self.term()
            elif this_token.type == my_tokens.MINUS:
                self.eat('MINUS')
                # result -= self.term()
            node = AST.BinaryOperatorNode(left_node=node, operator=this_token, right_node=self.term())
        return node

    def parse(self):
        node = self.program()
        if self.curr_token.type != my_tokens.EOF:
            self.error()
        return node


class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node.__name__)))


class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.GLOBAL_SCOPE: dict = {}
        self.parser = parser

    def visit_BinaryOperatorNode(self, node: AST.BinaryOperatorNode):
        if node.operator.type == my_tokens.PLUS:
            return self.visit(node.left_node) + self.visit(node.right_node)
        elif node.operator.type == my_tokens.MINUS:
            return self.visit(node.left_node) - self.visit(node.right_node)
        elif node.operator.type == my_tokens.MULTIPLY:
            return self.visit(node.left_node) * self.visit(node.right_node)
        elif node.operator.type == my_tokens.DIVIDE:
            return self.visit(node.left_node) / self.visit(node.right_node)

    def visit_UnaryOperatorNode(self, node: AST.UnaryOperatorNode):
        operator = node.operator.type

        if operator == my_tokens.PLUS:
            return +self.visit(node.expression)
        elif operator == my_tokens.MINUS:
            return -self.visit(node.expression)

    def visit_Number(self, node: AST.Number):
        return node.value

    def visit_Compound(self, node: AST.Compound):
        for child in node.children:
            self.visit(child)

    def visit_NoStatements(self, node):
        pass

    def visit_Assign(self, node: AST.Assign):
        var_name = node.left_node.value
        self.GLOBAL_SCOPE[var_name] = self.visit(node.right_node)

    def visit_Variable(self, node: AST.Variable):
        var_name = node.value
        value = self.GLOBAL_SCOPE.get(var_name)
        if value is None:
            raise NameError(repr(var_name))
        else:
            return value

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)
