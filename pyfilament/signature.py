from pyfilament.sexpr import SExpr, can_eval, eval_expr
from pyfilament.data import *
from z3 import *

# from . import Port


def parse_event(event: SExpr) -> Event:
    if event[0] != "event":
        raise RuntimeError(f"Expected event type. Got {event[0]}")
    return Event(event[1], event[2])


def parse_port(port: SExpr, ctx) -> Port:
    if port[0] == "interface":
        pass
    elif port[0] == "in-port":
        name = port[1]

        if len(port[2]) == 3 and can_eval(port[2][0]) and can_eval(port[2][1]):
            # TODO parse these into `Time`s
            range = Range(port[2][0], port[2][1])
        else:
            raise RuntimeError(f"Error in range specification for port {port[0]}")

        if can_eval(port[3]):
            bitwidth = port[3]
        else:
            raise RuntimeError(f"Error in bitwidth specification for port {port[0]}")

        return Port(name, range, bitwidth)

    elif port[0] == "out-port":
        pass
    else:
        raise RuntimeError(
            f"Expected port type ('interface', 'in-port', 'out-port'). Got {port[0]}"
        )


# Updated parse_constraint to integrate with Z3
def parse_constraint(constraint: SExpr):
    """
    Convert SExpr constraints into Z3 expressions.
    """
    if constraint[0] == "=":
        return Int(constraint[1]) == Int(constraint[2])
    elif constraint[0] == ">":
        return Int(constraint[1]) > Int(constraint[2])
    elif constraint[0] == "<":
        return Int(constraint[1]) < Int(constraint[2])
    else:
        raise RuntimeError(f"Unsupported constraint operator: {constraint[0]}")


# Updated Signature class
class Signature:
    def __init__(self, sexpr: SExpr):
        self.port_mapping = dict() # str -> port
        self.port_mapping += {'left': Port(...)}



    def solve_constraints(self):
        """
        Solve the constraints using Z3.
        """
        solver = Solver()
        for constraint in self.constraints:
            solver.add(constraint)

        if solver.check() == sat:
            model = solver.model()
            print("Solution:")
            for var in model:
                print(f"{var} = {model[var]}")
        else:
            print("No solution found.")
