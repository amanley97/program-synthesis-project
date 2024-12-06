from typing import List

from port import Port, InterfacePort
from sexpr import SExpr

class Signature:
    def __init__(self, name: str, event: str, interface: InterfacePort, in_ports: List[Port], out_ports: List[Port]):
        self.name = name
        self.event = event
        self.interface = interface
        self.in_ports = in_ports
        self.out_ports = out_ports

    @staticmethod
    def from_sexpr(expr: SExpr):
        name = expr["comp"]
        events = expr["events"]
        interface = None
        in_ports = []
        out_ports = []

        for port in expr["ports"]:
            if port[0].startswith("interface") and interface is None:
                interface = Port.from_sexpr(port)
            elif port[0].startswith("in-port"):
                in_ports.append(Port.from_sexpr(port))
            elif port[0].startswith("out-port"):
                out_ports.append(Port.from_sexpr(port))
            else:
                raise RuntimeError(f"Invalid port in signature definition: {port}")

        return Signature(name, events, interface, in_ports, out_ports)

    def __repr__(self):
        in_ports_str = ", ".join(repr(p) for p in self.in_ports)
        out_ports_str = ", ".join(repr(p) for p in self.out_ports)
        return (f"{self.name}<{self.event}>({self.interface}, {in_ports_str}) -> ({out_ports_str})")
