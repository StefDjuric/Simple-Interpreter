import token


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

    def __init__(self, token: token.Token):
        self.token = token
        self.value = token.value
