class Symbol(object):

    def __init__(self, name, type=None):
        self.name = name
        self.type = type


class BuiltInTypeSymbol(Symbol):

    def __init__(self, name):
        super().__init__(name)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<{self.__class__.__name__}(name='{self.name}')>"


class VariableSymbol(Symbol):
    def __init__(self, name, type):
        super().__init__(name, type)

    def __str__(self):
        return f'<{self.__class__.__name__} (name={self.name}), type={self.type}>'

    __repr__ = __str__


class SymbolTable(object):

    def __init__(self):
        self.symbols = {}
        self._init_builtins()

    def _init_builtins(self):
        self.insert(BuiltInTypeSymbol('INTEGER'))
        self.insert(BuiltInTypeSymbol('REAL'))

    def __str__(self):
        symtab_header = 'Symbol table contents'
        lines = ['\n', symtab_header, '_' * len(symtab_header)]
        lines.extend(
            ('%7s: %r' % (key, value))
            for key, value in self.symbols.items()
        )
        lines.append('\n')
        s = '\n'.join(lines)
        return s

    __repr__ = __str__

    def define(self, symbol):
        print(f'Define: {symbol}')
        self.symbols[symbol.name] = symbol

    def lookup(self, name) -> Symbol:
        print(f'Lookup: {name}')
        symbol = self.symbols.get(name)
        return symbol

    def insert(self, this_symbol: Symbol):
        print(f'Insert: {this_symbol.name}')
        self.symbols[this_symbol.name] = this_symbol
