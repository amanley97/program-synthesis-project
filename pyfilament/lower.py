# Takes in a namespace and generates lower filament for it
import re
from typing import Optional, List, Union, Dict

class Port:
    def __init__(self, name: str, direction: str, range_: Optional[str], width: int):
        self.name = name
        self.direction = direction
        self.range_ = range_
        self.width = width

    def __repr__(self):
        return (f"Port(name={self.name}, direction={self.direction}, "
                f"range_={self.range_}, width={self.width})")

    @staticmethod
    def parse(port_str: str, direction: str) -> "Port":
        # Match the range, name, and width
        match = re.match(r"@\[([^\]]*)\]\s*(\w+):\s*(\d+)", port_str)
        if match:
            range_ = match.group(1).strip() if match.group(1) else None
            name = match.group(2)
            width = int(match.group(3))
            return Port(name, direction, range_, width)
        else:
            raise ValueError(f"Invalid port format: {port_str}")

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

    @staticmethod
    def parse(component: str) -> "Component":
        # Match the name and guard
        name_match = re.search(r"comp\s+(\w+)<([^>]*)>", component)
        name = name_match.group(1) if name_match else None
        guard = f"<{name_match.group(2)}>" if name_match else None

        # Match the interface
        interface_match = re.search(r"\(@interface\[.*?\]\s*([^)]*)\)", component)
        interface = interface_match.group(1).strip() if interface_match else None

        # Match input ports
        in_ports_match = re.findall(r"(@\[.*?\]\s*\w+:\s*\d+)", component)
        in_ports = [Port.parse(port_str, direction="in") for port_str in in_ports_match]

        # Match output ports
        out_ports_match = re.findall(r"(@\[.*?\]\s*\w+:\s*\d+)", component)
        out_ports = [Port.parse(port_str, direction="out") for port_str in out_ports_match]

        return Component(name, guard, interface, in_ports, out_ports)


class Command:
    def __init__(self, text: str):
        self.text = text

    def __repr__(self):
        return f"{self.__class__.__name__}({self.text})"

class Instance(Command):
    def __init__(self, text: str, variable: str, type_name: str, size: Optional[int]):
        super().__init__(text)
        self.variable = variable
        self.type_name = type_name
        self.size = size

    def __repr__(self):
        return (f"{self.__class__.__name__}(variable={self.variable}, type_name={self.type_name}, "
                f"size={self.size})")

    @staticmethod
    def parse(cmd: str):
        match = re.match(r"(\w+)\s*:=\s*new\s+(\w+)\[(\d+)\]", cmd)
        if match:
            variable, type_name, size = match.groups()
            return Instance(cmd, variable, type_name, int(size))    
        else:
            raise ValueError(f"Invalid Instance command format: {cmd}")
        
class Invoke(Command):
    def __init__(self, text: str, variable: str, function: str, range_: str, ports: List[str]):
        super().__init__(text)
        self.variable = variable
        self.function = function
        self.range_ = range_
        self.ports = ports

    def __repr__(self):
        return (f"{self.__class__.__name__}(variable={self.variable}, function={self.function}, "
                f"range_={self.range_}, ports={self.ports})")

    @staticmethod
    def parse(cmd: str):
        match = re.match(r"(\w+)\s*:=\s*(\w+)<([^>]*)>\(([^)]*)\)", cmd.strip())
        if match:
            variable, function, range_, ports = match.groups()
            ports_list = [port.strip() for port in ports.split(",")]
            return Invoke(cmd, variable, function, range_, ports_list)
        else:
            raise ValueError(f"Invalid Invoke command format: {cmd}")

# Subclass for Connect commands
class Connect(Command):
    def __init__(self, text: str, target: str, source: str):
        super().__init__(text)
        self.target = target
        self.source = source

    def __repr__(self):
        return f"{self.__class__.__name__}(target={self.target}, source={self.source})"
    
    @staticmethod
    def parse(cmd:str):
        match = re.match(r"(\w+)\s*=\s*(\w+)", cmd)
        if match:
            target, source = match.groups()
            return Connect(cmd, target, source)
        else:
            raise ValueError(f"Invalid Connect command format: {cmd}")

class PyFilamentLower:
    def __init__(self):
        pass
    
    def split_namespace(self, namespace:str) -> list[str]:
        components = re.findall(r"comp\s+\w+<[^>]*>\([^)]*\)\s*->\s*\([^)]*\)\s*\{[^}]*\}", namespace, re.DOTALL)
        return components

    def extract_comp_data(self, components: List[str]) -> dict[str, Component]:
        data = {}

        for component_str in components:
            # Parse the component using the Component class
            component = Component.parse(component_str)

            # Add the parsed component to the dictionary using its name as the key
            if component.name:
                data[component.name] = component

        return data


    def _parse_command(self, command_str: str) -> Union[Instance, Invoke, Connect]:
        command_str = command_str.strip()

        if ":=" in command_str and "new" in command_str:
            return Instance.parse(command_str)

        if ":=" in command_str and "new" not in command_str:
            return Invoke.parse(command_str)

        if "=" in command_str:
            return Connect.parse(command_str)

        raise ValueError(f"Unknown command type: {command_str}")

    def convert_commands_to_objects(self, components: dict[str, List[str]]) -> dict[str, List[Command]]:
        result = {}
        for component_name, commands in components.items():
            result[component_name] = [self._parse_command(command) for command in commands]
        return result


if __name__ == "__main__":
    test_lower = PyFilamentLower()

    ns = """
            comp main<G: 1>(@interface[G] go: 1, @[G, G+1] left: 32, @[G, G+1] right: 32, @[G+1, G+2] opt: 32) -> (@[G+3, G+4] out: 32) {
                A := new And[32];
                a0 := A<G>(left,right);
                AND_STAGE := new Register[32];
                and_stage := AND_STAGE<G,G+2>(a0.out);
                X := new Xor[32];
                x0 := X<G+1>(and_stage.out,opt);
                XOR_STAGE := new Register[32];
                xor_stage := XOR_STAGE<G+1,G+3>(x0.out);
                R0 := new Register[32];
                r0 := R0<G+2,G+4>(xor_stage.out);
                out = r0.out;
            }
            """

    comps = test_lower.split_namespace(ns)
    comp_d = test_lower.extract_comp_data(comps)

    cmd_objs = test_lower.convert_commands_to_objects(comp_d)

    for obj in cmd_objs.values():
        for cmd in obj:
            print(cmd)