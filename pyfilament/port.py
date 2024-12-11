from enum import Enum
from typing import Optional, List

from pyfilament.sexpr import SExpr, print_expr
from pyfilament.event import Range, Event


class Direction(Enum):
    IN = 0
    OUT = 1
    INTERFACE = 2


class Port:
    def __init__(self, name: str, direction: Direction, range_: tuple, width: int):
        self.name = name
        self.direction = direction
        # self.range_ = range_
        self.width = width

        if len(range_) == 1:
            self.range_ = (range_[0], range_[0])
        elif len(range_) == 2:
            self.range_ = (range_[0], range_[1])
        else:
            raise RuntimeError("Range expected only one or two expressions")

    @staticmethod
    def from_sexpr(sexpr: SExpr):
        if sexpr[0].startswith("in-port"):
            direction = Direction.IN
        elif sexpr[0].startswith("out-port"):
            direction = Direction.OUT
        elif sexpr[0].startswith("interface"):
            direction = Direction.INTERFACE
        else:
            raise RuntimeError(f"Invalid direction for port: {sexpr}")

        start, stop = sexpr[0].find("["), sexpr[0].find("]")
        if start == -1 or stop == -1:
            raise RuntimeError(f"No width specified for port: {sexpr}")
        width = int(sexpr[0][start + 1 : stop])

        if len(sexpr[1]) == 1:
            range_ = Range(sexpr[1][0])
        elif len(sexpr[1] == 2):
            range_ = Range(sexpr[1][0], sexpr[1][1])
        else:
            raise RuntimeError(f"Incorrect number of arguments to range: {sexpr[1]}")

        name = sexpr[2]
        if direction == Direction.INTERFACE:
            return InterfacePort(name, range_, width)
        return Port(name, direction, range_, width)


    def __repr__(self):
        if len(self.range_) == 2:
            range_str = f"{print_expr(self.range_[0])}, {print_expr(self.range_[1])}"
        else:
            range_str = f"{print_expr(self.range_)}"
        return f"@[{range_str}] {self.name}: {self.width}"


class InterfacePort(Port):
    def __init__(self, name: str, event: tuple, width: int):
        """
        Represent an interface port with an event.

        Args:
            name (str): Name of the port.
            event (str): Event associated with the port.
            width (int): Width of the port in bits.
        """
        super().__init__(name, Direction.INTERFACE, event, width)
        self.event = event

    def __repr__(self):
        return f"@interface[{self.event[0]}] {self.name}: {self.width}"
