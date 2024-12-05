from typing import List

# from pyfilament.signature import Signature
from pyfilament.command import Command
from pyfilament.port import Port

class Component:
    def __init__(self, signature: 'Signature', commands: list[Command]):
        self.signature = signature
        self.commands = commands


class Signature:
    def __init__(self, name: str, event: str, interface: str, in_ports: List[Port], out_ports: List[Port]):
        self.name = name
        self.event = event
        self.interface = interface
        self.in_ports = in_ports
        self.out_ports = out_ports

    def __repr__(self):
        return (f"Component(name={self.name}, event={self.event}, interface={self.interface}, "
                f"in_ports={self.in_ports}, out_ports={self.out_ports})")
