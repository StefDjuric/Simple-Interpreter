import my_tokens
import AST


class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        # set current token to the first token taken from the input
        self.current_token = self.lexer.tokenizer()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):

        if self.current_token.type == token_type:
            self.current_token = self.lexer.tokenizer()
        else:
            self.error()

    def program(self):

        self.eat(my_tokens.PROGRAM)
        var_node = self.variable()
        prog_name = var_node.value
        self.eat(my_tokens.SEMI)
        block_node = self.block()
        program_node = AST.Program(prog_name, block_node)
        self.eat(my_tokens.DOT)
        return program_node

    def block(self):

        declaration_nodes = self.declarations()
        compound_statement_node = self.compound_statement()
        node = AST.Block(declaration_nodes, compound_statement_node)
        return node

    def declarations(self):

        declarations = []
        if self.current_token.type == my_tokens.VAR:
            self.eat(my_tokens.VAR)
            while self.current_token.type == my_tokens.ID:
                var_declaration = self.variable_declaration()
                declarations.extend(var_declaration)
                self.eat(my_tokens.SEMI)

        return declarations

    def variable_declaration(self):
        """variable_declaration : ID (COMMA ID)* COLON type_spec"""
        var_nodes = [AST.Variable(self.current_token)]  # first ID
        self.eat(my_tokens.ID)

        while self.current_token.type == my_tokens.COMMA:
            self.eat(my_tokens.COMMA)
            var_nodes.append(AST.Variable(self.current_token))
            self.eat(my_tokens.ID)

        self.eat(my_tokens.COLON)

        type_node = self.type_spec()
        var_declarations = [
            AST.VariableDeclaration(var_node, type_node)
            for var_node in var_nodes
        ]
        return var_declarations

    def type_spec(self):

        token = self.current_token
        if self.current_token.type == my_tokens.INTEGER:
            self.eat(my_tokens.INTEGER)
        else:
            self.eat(my_tokens.REAL)
        node = AST.Type(token)
        return node

    def compound_statement(self):

        self.eat(my_tokens.BEGIN)
        nodes = self.statement_list()
        self.eat(my_tokens.END)

        root = AST.Compound()
        for node in nodes:
            root.children.append(node)

        return root

    def statement_list(self):

        node = self.statement()

        results = [node]

        while self.current_token.type == my_tokens.SEMI:
            self.eat(my_tokens.SEMI)
            results.append(self.statement())

        return results

    def statement(self):

        if self.current_token.type == my_tokens.BEGIN:
            node = self.compound_statement()
        elif self.current_token.type == my_tokens.ID:
            node = self.assignment_statement()
        else:
            node = self.empty()
        return node

    def assignment_statement(self):
        """
        assignment_statement : variable ASSIGN expr
        """
        left = self.variable()
        token = self.current_token
        self.eat(my_tokens.ASSIGN)
        right = self.expression()
        node = AST.Assign(left, token, right)
        return node

    def variable(self):
        """
        variable : ID
        """
        node = AST.Variable(self.current_token)
        self.eat(my_tokens.ID)
        return node

    def empty(self):
        """An empty production"""
        return AST.NoStatements()

    def expression(self):
        """
        expr : term ((PLUS | MINUS) term)*
        """
        node = self.term()

        while self.current_token.type in (my_tokens.PLUS, my_tokens.MINUS):
            token = self.current_token
            if token.type == my_tokens.PLUS:
                self.eat(my_tokens.PLUS)
            elif token.type == my_tokens.MINUS:
                self.eat(my_tokens.MINUS)

            node = AST.BinaryOperatorNode(left_node=node, operator=token, right_node=self.term())

        return node

    def term(self):
        """term : factor ((MUL | INTEGER_DIV | FLOAT_DIV) factor)*"""
        node = self.factor()

        while self.current_token.type in (my_tokens.MULTIPLY, my_tokens.INTEGER_DIV, my_tokens.FLOAT_DIV):
            token = self.current_token
            if token.type == my_tokens.MULTIPLY:
                self.eat(my_tokens.MULTIPLY)
            elif token.type == my_tokens.INTEGER_DIV:
                self.eat(my_tokens.INTEGER_DIV)
            elif token.type == my_tokens.FLOAT_DIV:
                self.eat(my_tokens.FLOAT_DIV)

            node = AST.BinaryOperatorNode(left_node=node, operator=token, right_node=self.factor())

        return node

    def factor(self):

        token = self.current_token
        if token.type == my_tokens.PLUS:
            self.eat(my_tokens.PLUS)
            node = AST.UnaryOperatorNode(token, self.factor())
            return node
        elif token.type == my_tokens.MINUS:
            self.eat(my_tokens.MINUS)
            node = AST.UnaryOperatorNode(token, self.factor())
            return node
        elif token.type == my_tokens.INTEGER_CONST:
            self.eat(my_tokens.INTEGER_CONST)
            return AST.Number(token)
        elif token.type == my_tokens.REAL_CONST:
            self.eat(my_tokens.REAL_CONST)
            return AST.Number(token)
        elif token.type == my_tokens.LPARAN:
            self.eat(my_tokens.LPARAN)
            node = self.expression()
            self.eat(my_tokens.RPARAN)
            return node
        else:
            node = self.variable()
            return node

    def parse(self):
        node = self.program()
        if self.current_token.type != my_tokens.EOF:
            self.error()

        return node


class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))


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
        elif node.operator.type == my_tokens.INTEGER_DIV:
            return self.visit(node.left_node) // self.visit(node.right_node)
        elif node.operator.type == my_tokens.FLOAT_DIV:
            return float(self.visit(node.left_node)) / float(self.visit(node.right_node))

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

    def visit_Program(self, node):
        self.visit(node.block)

    def visit_Block(self, node):
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.compound_statement)

    def visit_VariableDeclaration(self, node):
        pass

    def visit_Type(self, node):
        pass

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)
