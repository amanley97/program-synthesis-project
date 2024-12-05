from typing import List, Optional

from pyfilament.sexpr import SExpr
# from component import Signature

class Command:
    def __init__(self):
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}()"


class Instance(Command):
    def __init__(self, variable: str, type_name: str, size: Optional[int]):
        """
        Represent an (instantiate) command.

        Args:
            variable (str): The name of the instance variable.
            type_name (str): The type of the instance (e.g., Register).
            size (Optional[int]): The size of the instance (if applicable).
        """
        super().__init__()
        self.variable = variable
        self.type_name = type_name
        self.size = size

    def __repr__(self):
        size_str = f"[{self.size}]" if self.size else ""
        return f"{self.variable} := new {self.type_name}{size_str};"

    @staticmethod
    def from_sexpr(sexpr: SExpr):
        name = sexpr[0]
        definition = sexpr[1][1]
        start, stop = definition.find('['), definition.find(']')
        if start == -1 or stop == -1:
            raise RuntimeError("No width for instantiation")
        type_name = definition[:start]
        width = definition[start+1:stop]
        return Instance(name, type_name, width)

class Invoke(Command):
    def __init__(self, variable: str, function: str, event: str, ports: List[str]):
        """
        Represent an (invoke) command.

        Args:
            variable (str): The name of the invoke variable.
            function (str): The function or instance being invoked.
            event (str): The event associated with the invoke.
            ports (List[str]): The list of port names connected to the invoke.
        """
        super().__init__()
        self.variable = variable
        self.function = function
        self.event = event
        self.ports = ports

    @staticmethod
    def from_sexpr(sexpr: SExpr):
        name = sexpr[0]
        definition = sexpr[1][1]
        start, stop = definition.find('['), definition.find(']')
        if start == -1 or stop == -1:
            raise RuntimeError("No width for instantiation")
        type_name = definition[:start]
        width = definition[start+1:stop]
        return Instance(name, type_name, width)

    def __repr__(self):
        ports_str = ", ".join(self.ports)
        return f"{self.variable} := invoke {self.function}<{self.range_}>({ports_str});"


class Connect(Command):
    def __init__(self, dest: str, src: str, guard: Optional[str] = None):
        """
        Represent a (connect) command.

        Args:
            target (str): The target of the connection.
            source (str): The source of the connection.
            guard (Optional[str]): The guard condition for the connection.
        """
        super().__init__()
        self.dest = dest
        self.src = src
        self.guard = guard

    def __repr__(self):
        guard_str = f"{self.guard} ? " if self.guard else ""
        return f"{self.target} = {guard_str}{self.source};"
