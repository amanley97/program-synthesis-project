class SExpr:
    def __init__(self, l):
        self.as_list = l

    def __getitem__(self, key):
        return self.as_list[key]

    def __str__(self):
        return "(" + " ".join(map(str, self.as_list)) + ")"

    def __repr__(self):
        return str(self)

    def __len__(self):
        return len(self.as_list)
