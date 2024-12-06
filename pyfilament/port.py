from enum import Enum
from typing import Optional, List

from pyfilament.sexpr import SExpr

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

    def parse_range_expression(expr: str) -> tuple:
        def tokenize(expression):
            return expression.replace('(', ' ( ').replace(')', ' ) ').split()
        
        def process_tokens(tokens):
            results = []
            i = 0
            while i < len(tokens):
                if tokens[i] == '(':
                    # Check for addition pattern
                    if i + 4 < len(tokens) and tokens[i+1] == '+':
                        # Pattern like (+ G 2)
                        variable = tokens[i+2]
                        number = tokens[i+3]
                        results.append(f"{variable}+{number}")
                        i += 5
                    elif i + 1 < len(tokens):
                        # Simple G or nested case
                        if tokens[i+1] == 'G':
                            results.append('G')
                            i += 2
                        elif tokens[i+1] == '(':
                            # Nested case with addition
                            if i + 5 < len(tokens) and tokens[i+2] == '+':
                                variable = tokens[i+3]
                                number = tokens[i+4]
                                results.append(f"{variable}+{number}")
                                i += 6
                        else:
                            i += 1
                    else:
                        i += 1
                else:
                    i += 1
            
            return results

        # Tokenize and process the expression
        tokens = tokenize(expr)
        parsed = process_tokens(tokens)
        
        # Return as a tuple, ensuring single element is still a tuple
        return tuple(parsed)

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
        
        start, stop = sexpr[0].find('['), sexpr[0].find(']')
        if start == -1 or stop == -1:
            raise RuntimeError(f"No width specified for port: {sexpr}")
        width = int(sexpr[0][start+1:stop])
        range_ = Port.parse_range_expression(str(sexpr[1]))
        name = sexpr[2]
        if direction == Direction.INTERFACE:
            return InterfacePort(name, range_, width)
        return Port(name, direction, range_, width)

    def __repr__(self):
        range_str = f"{self.range_[0]}, {self.range_[1]}"
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