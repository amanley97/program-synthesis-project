from typing import List

from pyfilament.signature import Signature
from pyfilament.command import Command, Instance, Invoke, Connect
from pyfilament.sexpr import SExpr


class Component:
    def __init__(self, signature: "Signature", commands: List[Command]):
        self.signature = signature
        self.commands = commands

    def __repr__(self):
        commands_str = "\n  ".join(repr(cmd) for cmd in self.commands)
        return f"comp {repr(self.signature)} {{\n  {commands_str}\n}}"

    @staticmethod
    def from_sexpr(expr: SExpr):
        signature = Signature.from_sexpr(expr)
        commands = []
        for command in expr["instantiate"]:
            commands.append(Instance.from_sexpr(command))
        for command in expr["invoke"]:
            commands.append(Invoke.from_sexpr(command))
        for command in expr["connect"]:
            commands.append(Connect.from_sexpr(command))
        return Component(signature, commands)
