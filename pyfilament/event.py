from typing import Optional

from pyfilament.sexpr import SExpr

class Range:
    def __init__(self, lo: str | SExpr, hi: Optional[str | SExpr]=None):
        self.lo = Event(lo)
        self.hi = Event(hi)

    def __repr__(self):
        if self.hi is not None:
            return f"{self.lo}, {self.hi}"
        else:
            return f"{self.lo}"


class Event:
    def __init__(self, expr: str | SExpr):
        self.expr = expr

    def __repr__(self):
        return f"{self.expr.arithmetic() if isinstance(self.expr, SExpr) else self.expr}"