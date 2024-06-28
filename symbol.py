import symbol


class Symbol(object):

    def __init__(self, name, type=None):
        self.name = name
        self.type = type


class BuiltInTypeSymbol(Symbol):

    def __init__(self, name):
        super().__init__(name)

    def __str__(self):
        return self.name

    __repr__ = __str__


class VariableSymbol(Symbol):
    def __init__(self, name, type):
        super().__init__(name, type)

    def __str__(self):
        return f'<{self.name}:{self.type}>'

    __repr__ = __str__


class SymbolTable(object):

    def __init__(self):
        self.symbols = {}
        self._init_builtins()

    def _init_builtins(self):
        self.define(BuiltInTypeSymbol('INTEGER'))
        self.define(BuiltInTypeSymbol('REAL'))

    def __str__(self):
        return f'Symbols: {[value for value in self.symbols.values()]}'

    __repr__ = __str__

    def define(self, symbol):
        print(f'Define: {symbol}')
        self.symbols[symbol.name] = symbol

    def lookup(self, name) -> symbol.Symbol:
        print(f'Lookup: {name}')
        symbol = self.symbols.get(name)
        return symbol
