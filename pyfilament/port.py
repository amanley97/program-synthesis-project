from enum import Enum

from pyfilament.sexpr import SExpr
from pyfilament.event import Range


class Direction(Enum):
    IN = 0
    OUT = 1
    INTERFACE = 2


class Port:
    def __init__(self, name: str, direction: Direction, range_: Range, width: int):
        self.name = name
        self.direction = direction
        self.range_ = range_
        self.width = width

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
        elif len(sexpr[1]) == 2:
            range_ = Range(sexpr[1][0], sexpr[1][1])
        else:
            raise RuntimeError(f"Incorrect number of arguments to range: {sexpr[1]}")

        name = sexpr[2]
        if direction == Direction.INTERFACE:
            return InterfacePort(name, range_, width)
        return Port(name, direction, range_, width)

    def __repr__(self):
        return f"@[{self.range_}] {self.name}: {self.width}"


class InterfacePort(Port):
    def __init__(self, name: str, event: Range, width: int):
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
        return f"@interface[{self.event}] {self.name}: {self.width}"
