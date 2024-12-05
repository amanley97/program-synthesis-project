from enum import Enum

from typing import Optional

class Direction(Enum):
    IN = 0
    OUT = 1
    INTERFACE = 2

class Port:
    def __init__(self, name: str, direction: Direction, range_: tuple, width: int):
        self.name = name
        self.direction = direction
        self.range_ = range_
        self.width = width

    def __repr__(self):
        range_str = f"({self.range_[0]}, {self.range_[1]})"
        return f"@[{range_str}] {self.name}: {self.width}"

class InterfacePort(Port):
    def __init__(self, name: str, event: str, width: int):
        """
        Represent an interface port with an event.

        Args:
            name (str): Name of the port.
            event (str): Event associated with the port.
            width (int): Width of the port in bits.
        """
        super().__init__(name, Direction.INTERFACE, (event, event), width)
        self.event = event

    def __repr__(self):
        return f"@interface[{self.event}] {self.name}: {self.width}"