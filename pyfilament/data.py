from pyfilament.sexpr import SExpr
from typing import Optional

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
    """Represents a hardware port with various types and properties.
    
    Attributes:
        name (str): The name of the port.
        liveness (Range): The range of cycles during which the port is live.
        bitwidth (int): The bitwidth of the port.
        direction (Direction): The direction of the port (input/output).
        port_type (str): The type of the port ('bundle', 'this', 'inv', 'constant').
        invoke (Optional[str]): The component being invoked (used for 'inv' type).
        constant_value (Optional[int]): The constant value (used for 'constant' type).
    """
    def __init__(self, name: str, liveness: 'Range', bitwidth: int, direction: 'Direction', 
                 port_type: str = "this", invoke: Optional[str] = None, constant_value: Optional[int] = None):
        """
        Initialize a port.

        Args:
            name (str): The name of the port.
            liveness (Range): The range of cycles during which the port is live.
            bitwidth (int): The bitwidth of the port.
            direction (Direction): The direction of the port (input/output).
            port_type (str): The type of the port ('bundle', 'this', 'inv', 'constant').
            invoke (Optional[str]): The component being invoked (for 'inv' type).
            constant_value (Optional[int]): The constant value (for 'constant' type).
        """
        self.name = name
        self.liveness = liveness
        self.bitwidth = bitwidth
        self.direction = direction
        self.port_type = port_type
        self.invoke = invoke
        self.constant_value = constant_value


class Port:
    """@[G, G+1] name: bitwidth
    Args:
            name (str): The name of the port.
            liveness (Range): The range of cycles during which the port is live.
            bitwidth (int): The bitwidth of the port.
            direction (Direction): The direction of the port (input/output).
            port_type (str): The type of the port ('bundle', 'this', 'inv', 'constant').
            invoke (Optional[str]): The component being invoked (for 'inv' type).
            constant_value (Optional[int]): The constant value (for 'constant' type).
    """

    def __init__(self, name: str, liveness: 'Range', bitwidth: int, direction: 'Direction', 
                 port_type: str = "this", invoke: Optional[str] = None, constant_value: Optional[int] = None):
        self.name = name
        self.liveness = liveness
        self.bitwidth = bitwidth
        self.direction = direction
        self.port_type = port_type
        self.invoke = invoke
        self.constant_value = constant_value


class Direction:
    INPUT = "input"
    OUTPUT = "output"

    @staticmethod
    def reverse(direction: str) -> str:
        return Direction.OUTPUT if direction == Direction.INPUT else Direction.INPUT