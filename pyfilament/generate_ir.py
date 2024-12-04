from pyfilament.data import Port, Direction, Event
from pyfilament.fsm import Fsm
from pyfilament.signature import Signature
from pyfilament.sexpr import SExpr
from typing import List, Dict, Tuple, Any


class CalyxIRGenerator:
    def __init__(self, library, binding):
        """
        Initialize the generator with the Calyx library and component binding.
        Args:
            library: Library of Calyx primitives and external definitions.
            binding: Maps Filament components to their Calyx signatures.
        """
        self.library = library
        self.binding = binding

    def generate_ports(self, signature):
        """
        Convert Filament ports into Calyx IR port definitions.
        """
        ports = []
        for port in signature.inputs + signature.outputs:
            direction = Direction.INPUT if port.is_input else Direction.OUTPUT
            ports.append({
                "name": port.name,
                "width": port.bitwidth,
                "direction": direction
            })
        return ports

    def create_calyx_component(self, filament_component):
        """
        Create the structure of a Calyx IR component from a Filament component.
        """
        ports = self.generate_ports(filament_component.signature)
        calyx_component = {
            "name": filament_component.signature.name,
            "ports": ports,
            "body": [],
            "attributes": {"nointerface": True}
        }
        return calyx_component

    def process_fsm(self, fsm, context):
        """
        Process FSM commands and generate the corresponding Calyx IR FSM component.
        """
        fsm_instance = Fsm(fsm, context)
        context.fsms[fsm.name] = fsm_instance

    def process_instance(self, instance, context):
        """
        Process instance commands and add them to the Calyx IR.
        """
        if instance.component in context.binding:
            # Use existing component signature
            signature = context.binding[instance.component]
            cell = {
                "name": instance.name,
                "component": signature.name,
                "ports": signature.ports
            }
        else:
            # Create a new primitive
            cell = {
                "name": instance.name,
                "component": instance.component,
                "bindings": instance.bindings
            }
        context.instances[instance.name] = cell

    def process_connection(self, connection, context):
        """
        Process connections between ports and add them to the IR.
        """
        src, guard_src = context.compile_port(connection.src)
        dst, guard_dst = context.compile_port(connection.dst)
        guard = guard_src if guard_src else guard_dst
        assignment = {
            "dst": dst,
            "src": src,
            "guard": guard
        }
        context.calyx_component["body"].append(assignment)

    def generate_ir(self, filament_component):
        """
        Generate Calyx IR for a given Filament component.
        """
        context = Context(self.library, self.binding)
        calyx_component = self.create_calyx_component(filament_component)
        context.calyx_component = calyx_component

        for command in filament_component.body:
            if isinstance(command, core.Instance):
                self.process_instance(command, context)
            elif isinstance(command, core.Fsm):
                self.process_fsm(command, context)
            elif isinstance(command, core.Connect):
                self.process_connection(command, context)
            else:
                raise ValueError(f"Unsupported command type: {type(command)}")

        return calyx_component


class Context:
    """
    helper class to manage bindings and instances during IR generation.
    """
    def __init__(self, library, binding):
        self.library = library
        self.binding = binding
        self.instances = {}
        self.fsms = {}
        self.calyx_component = None

    def compile_port(self, port):
        """
        Translate Filament ports into Calyx IR ports.
        """
        if port.type == "constant":
            return {"name": f"const_{port.constant_value}", "width": port.bitwidth}, None
        elif port.type == "this":
            return {"name": port.name}, None
        elif port.type == "invocation":
            fsm = self.fsms.get(port.invoke)
            if fsm:
                return {"name": f"{fsm.cell}_{port.name}"}, None
            raise ValueError(f"Unknown invocation target: {port.invoke}")
        else:
            raise ValueError(f"Unknown port type: {port.type}")



# I assumed`filament_component` is a parsed Filament component object.
# `library` - I need the loaded Calyx library.
# `binding` is the component binding.

generator = CalyxIRGenerator(library, binding)
calyx_ir = generator.generate_ir(filament_component)
print(calyx_ir)
