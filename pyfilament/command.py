from typing import List, Optional

from pyfilament.sexpr import SExpr
from pyfilament.event import Range


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
        start, stop = definition.find("["), definition.find("]")
        if start == -1 or stop == -1:
            raise RuntimeError("No width for instantiation")
        type_name = definition[:start]
        width = definition[start + 1 : stop]
        return Instance(name, type_name, width)


class Invoke(Command):
    def __init__(self, variable: str, function: str, range_: Range, ports: List[str]):
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
        self.range_ = range_
        self.ports = ports
        self.lower = False

    @staticmethod
    def from_sexpr(sexpr: SExpr):
        name = sexpr[0]
        function = sexpr[1][0]
        if len(sexpr[1][1]) == 1:
            range_ = Range((sexpr[1][1][0]))
        elif len(sexpr[1][1]) == 3:
            range_ = Range(SExpr(sexpr[1][1]))
        elif len(sexpr[1][1]) == 2:
            range_ = Range(sexpr[1][1][0], sexpr[1][1][1])
        else:
            raise RuntimeError(f"Incorrect number of arguments to range: {sexpr[1][1]}")
        ports = sexpr[1][2:]
        return Invoke(name, function, range_, ports)

    def flag_lower(self):
        self.lower = True

    def __repr__(self):
        ports_str = ", ".join(self.ports)
        if not self.lower:
            return f"{self.variable} := invoke {self.function}<{self.range_}>({ports_str});"
        else:
            return f"{self.variable} := invoke {self.function}<{self.range_}>;"


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

    @staticmethod
    def from_sexpr(sexpr: SExpr):
        dest = sexpr[0]
        src = sexpr[1]
        return Connect(dest, src, None)

    def __repr__(self):
        guard_str = f" ? {self.guard}" if self.guard else ""
        return f"{self.dest} = {self.src}{guard_str};"
