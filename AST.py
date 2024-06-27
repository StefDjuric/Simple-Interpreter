import my_tokens


class AbstractSyntaxTree(object):
    pass


class UnaryOperatorNode(AbstractSyntaxTree):

    def __init__(self, operator, expression):
        self.token = self.operator = operator
        # expression represents an AST node
        self.expression = expression


# Operator representation
class BinaryOperatorNode(AbstractSyntaxTree):

    def __init__(self, left_node, operator, right_node):
        self.left_node = left_node
        self.right_node = right_node
        self.token = self.operator = operator


# Integer representation
class Number(AbstractSyntaxTree):

    def __init__(self, token: my_tokens.Token):
        self.token = token
        self.value = token.value


class Compound(AbstractSyntaxTree):
    """Represents a BEGIN ... END block"""

    def __init__(self):
        self.children = []


class Assign(AbstractSyntaxTree):

    def __init__(self, left_node, operator, right_node):
        self.left_node = left_node
        self.right_node = right_node
        self.token = self.operator = operator


class Variable(AbstractSyntaxTree):
    """The variable node is constructed using ID tokens"""

    def __init__(self, this_token: my_tokens.Token):
        self.token = this_token
        self.value = this_token.value


class NoStatements(object):
    pass
