from typing import Optional

from pyfilament.sexpr import SExpr, eval_expr

class Range:
    def __init__(self, lo: str | SExpr, hi: Optional[str | SExpr]=None):
        self.lo = Event(lo)
        if hi is not None:
            self.hi = Event(hi)
        else:
            self.hi = None

    def __len__(self):
        if self.hi is None:
            return 1
        else:
            return 2

    def __repr__(self):
        if self.hi is not None:
            return f"{self.lo}, {self.hi}"
        else:
            return f"{self.lo}"
        

class Event:
    def __init__(self, expr: str | SExpr):
        self.expr = expr

    def eval_constraint(self):
        return eval_expr(self.expr)

    def eval_event(self) -> int:
        G=0
        return eval(self.convert())
    
    def convert(self):
        return self.expr.arithmetic() if isinstance(self.expr, SExpr) else self.expr

    def __repr__(self):
        return f"{self.convert()}"