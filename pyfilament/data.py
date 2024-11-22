from pyfilament.sexpr import SExpr


class Event:
    """G: clocks"""

    def __init__(self, name, clocks: SExpr):
        self.name = name
        self.clocks = clocks


class Time:
    """G+1"""

    def __init__(self, event: Event, offset: SExpr):
        self.event = event
        self.offset = offset


class Range:
    """@[G, G+1]"""

    def __init__(self, begin: SExpr, end: SExpr):
        self.begin = begin
        self.end = end

    def well_formed(self):
        raise NotImplementedError()


class Port:
    """@[G, G+1] name: bitwidth"""

    def __init__(self, name: str, liveness: Range, bitwidth):
        self.name = name
        self.liveness = liveness
        self.bitwidth = bitwidth
