

class AbstractSyntaxTree(object):
    pass


class BinaryOperatorNode(AbstractSyntaxTree):
    def __init__(self, left_node, operator, right_node):
        self.left_node = left_node
        self.token = self.operator = operator
        self.right_node = right_node


class Number(AbstractSyntaxTree):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class UnaryOperatorNode(AbstractSyntaxTree):
    def __init__(self, operator, expression):
        self.token = self.operator = operator
        self.expression = expression


class Compound(AbstractSyntaxTree):
    """Represents a 'BEGIN ... END' block"""
    def __init__(self):
        self.children = []


class Assign(AbstractSyntaxTree):
    def __init__(self, left_node, operator, right_node):
        self.left_node = left_node
        self.token = self.operator = operator
        self.right_node = right_node


class Variable(AbstractSyntaxTree):
    """The Var node is constructed out of ID token."""
    def __init__(self, token):
        self.token = token
        self.value = token.value


class NoStatements(AbstractSyntaxTree):
    pass


class Program(AbstractSyntaxTree):
    def __init__(self, name, block):
        self.name = name
        self.block = block


class Block(AbstractSyntaxTree):
    def __init__(self, declarations, compound_statement):
        self.declarations = declarations
        self.compound_statement = compound_statement


class VariableDeclaration(AbstractSyntaxTree):
    def __init__(self, var_node, type_node):
        self.var_node = var_node
        self.type_node = type_node


class Type(AbstractSyntaxTree):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class ProcedureDeclaration(AbstractSyntaxTree):
    def __init__(self, procedure_name, block_node):
        self.procedure_name = procedure_name
        self.block_node = block_node

