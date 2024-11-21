from pyfilament.sexpr import SExpr
from pyfilament.data import *

def parse_event(event: SExpr) -> Event:
    if event[0] != 'event':
        raise RuntimeError(f"Expected event type. Got {event[0]}")
    return Event(event[1], event[2])

def parse_port(port: SExpr) -> Port:
    if port[0] == 'interface':
        pass
    elif port[0] == 'in-port':
        pass
    elif port[0] == 'out-port':
        pass
    else:
        raise RuntimeError(f"Expected port type ('interface', 'in-port', 'out-port'). Got {port[0]}")

def parse_constraint(constraint: SExpr) -> SExpr:
    return constraint

class Signature:
    def __init__(self, sexpr: SExpr):
        assert(sexpr[0] == "comp"), "Not a component definition"
        assert(len(sexpr) == 5), "Malformed component definition"
        self.name = sexpr[1]
        self.events = list(map(parse_event, [event for event in sexpr[2]]))
        # self.ports = list(map(parse_port, [port for port in sexpr[3]]))
        self.ports = [] # TODO parse ports, need context from self.events to fill in event data
        self.constraints = list(map(parse_constraint, [constraint for constraint in sexpr[4][1:]]))
