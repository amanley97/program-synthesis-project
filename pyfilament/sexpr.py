class SExpr:
    def __init__(self, l):
        self.as_list = l

    def __str__(self):
        return '(' + ' '.join(map(str, self.as_list)) + ')'

    def __repr__(self):
        return str(self)

