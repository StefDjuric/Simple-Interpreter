import token


class AbstractSyntaxTree(object):
    pass


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
