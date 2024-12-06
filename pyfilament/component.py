from typing import List

from pyfilament.signature import Signature
from pyfilament.command import Command, Instance, Invoke
from pyfilament.port import Port, InterfacePort
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
        # for command in expr["instantiate"]:
        #     commands.append(Instance.from_sexpr(signature, command))
        # for command in expr["invoke"]:
        #     commands.append(Invoke.from_sexpr(signature, command))
        return Component(signature, commands)
