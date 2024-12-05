from typing import List

# from pyfilament.signature import Signature
from command import Command
from port import Port, InterfacePort

class Component:
    def __init__(self, signature: 'Signature', commands: List[Command]):
        self.signature = signature
        self.commands = commands

    def __repr__(self):
        commands_str = "\n  ".join(repr(cmd) for cmd in self.commands)
        return f"comp {repr(self.signature)} {{\n  {commands_str}\n}}"


class Signature:
    def __init__(self, name: str, event: str, interface: InterfacePort, in_ports: List[Port], out_ports: List[Port]):
        self.name = name
        self.event = event
        self.interface = interface
        self.in_ports = in_ports
        self.out_ports = out_ports

    def __repr__(self):
        in_ports_str = ", ".join(repr(p) for p in self.in_ports)
        out_ports_str = ", ".join(repr(p) for p in self.out_ports)
        return (f"{self.name}<{self.event}>({self.interface}, {in_ports_str}) -> ({out_ports_str})")
