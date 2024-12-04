from typing import List

from . import Signature, Command, Port

class Component:
    def __init__(self, signature: Signature, commands: list[Command]):
        self.signature = signature
        self.commands = commands


class Component:
    def __init__(self, name: str, guard: str, interface: str, in_ports: List[Port], out_ports: List[Port]):
        self.name = name
        self.guard = guard
        self.interface = interface
        self.in_ports = in_ports
        self.out_ports = out_ports

    def __repr__(self):
        return (f"Component(name={self.name}, guard={self.guard}, interface={self.interface}, "
                f"in_ports={self.in_ports}, out_ports={self.out_ports})")
