from pyfilament.data import Port, Direction
from pyfilament.signature import Signature
from typing import List, Dict, Optional, Tuple, Any

class Fsm:
    """
    A Calyx-like FSM representation in Python that increments every cycle.
    """
    def __init__(self, fsm: Dict[str, Any], ctx: 'Context'):
        self.cell = self._construct_fsm(fsm, ctx)

    def _construct_fsm(self, fsm: Dict[str, Any], ctx: 'Context') -> 'Cell':
        event = fsm['name']
        comp = ctx.binding.fsm_comps[fsm['states']]
        
        # Add the component to the builder's context
        cell = ctx.builder.add_component(
            f"{event}",
            comp.name,
            self._cell_to_port_def(comp.signature)
        )
        
        # Connect the trigger port to the instance
        port, guard = ctx.compile_port(fsm['trigger'])
        assert guard is None, "Trigger port implies no guard"
        
        go_assign = ctx.builder.build_assignment(
            cell.get_port("go"),
            port,
            "True"  # A default guard equivalent to ir::Guard::True
        )
        ctx.builder.component.continuous_assignments.append(go_assign)
        return cell

    def event(self, port: str) -> str:
        return self.cell.get_port(port)

class Context:
    """
    Context for building a component.
    """
    def __init__(self, builder: 'Builder', binding: 'Binding', library: 'LibrarySignatures'):
        self.builder = builder
        self.binding = binding
        self.library = library
        self.instances: Dict[str, 'Cell'] = {}
        self.invokes: Dict[str, 'Cell'] = {}
        self.fsms: Dict[str, 'Fsm'] = {}

    def compile_port(self, port: 'Port') -> Tuple['Port', Optional['Guard']]:
        """
        Compile a port into a hardware representation.

        Args:
            port (Port): The port to compile.

        Returns:
            Tuple[Port, Optional[Guard]]: A tuple of the compiled port and an optional guard.
        """
        if port.port_type == "bundle":
            raise ValueError("Bundles should be compiled away")
        elif port.port_type == "this":
            # Retrieve the port from the current component's signature
            return self.builder.component.signature.get_port(port.name), None
        elif port.port_type == "inv":
            # Handle invocation ports
            if port.invoke in self.fsms:
                fsm = self.fsms[port.invoke]
                return self.builder.add_constant(1, 1).get_port("out"), fsm.event(port.name)
            elif port.invoke in self.invokes:
                cell = self.invokes[port.invoke]
                return cell.get_port(port.name), None
            else:
                raise ValueError(f"Invocation target {port.invoke} not found")
        elif port.port_type == "constant":
            # Handle constant ports
            return self.builder.add_constant(port.constant_value, port.bitwidth).get_port("out"), None
        else:
            raise ValueError(f"Unknown port type: {port.port_type}")


class Binding:
    def __init__(self):
        # Component signatures
        self.comps: Dict[str, 'Cell'] = {}
        # Mapping to the component representing FSM with a particular number of states
        self.fsm_comps: Dict[int, 'Component'] = {}

    @staticmethod
    def cell_to_port_def(cell: 'Cell') -> List['Port']:
        return [
            Port(
                name=port.name,
                width=port.width,
                direction=port.direction.reverse()
            )
            for port in cell.ports
        ]

    def get(self, name: str) -> Optional[List['Port']]:
        cell = self.comps.get(name)
        return self.cell_to_port_def(cell) if cell else None

    def insert_comp(self, name: str, sig: 'Cell'):
        self.comps[name] = sig
        
class Builder:
    def __init__(self, component: 'Component', library: 'LibrarySignatures'):
        self.component = component
        self.library = library

    def add_constant(self, value: int, width: int) -> 'Cell':
        # Create and return a new cell representing a constant
        return Cell(f"const_{value}_{width}", [Port("out", width, Direction.OUTPUT)])
    

class Component:
    def __init__(self, name: str, ports: List[Port]):
        self.name = name
        self.ports = ports
        self.attributes = {}

class Cell:
    def __init__(self, name: str, ports: List[Port]):
        self.name = name
        self.ports = ports

    def get_port(self, port_name: str) -> Port:
        for port in self.ports:
            if port.name == port_name:
                return port
        raise ValueError(f"Port {port_name} not found in {self.name}")
