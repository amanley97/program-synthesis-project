from pyfilament.command import Invoke, Instance, Connect
from pyfilament.component import Component
from pyfilament.port import Port, Direction
from pyfilament.fsm import Fsm
from pyfilament.event import Event


def generate_lower(component: Component):
    """
    Entry point to transform a component into lower filament.

    Args:
        component (Component): Component to be transformed.
    """
    lower_fil = FSMgen.generate(component)
    return lower_fil


class FSMgen:
    def __init__(self, ctx: Component):
        """
        Initialize the FSM generator with FSM details and context.
        """
        self.ctx = ctx
        self.ports = ctx.signature.in_ports + ctx.signature.out_ports
        self.states = self.determine_states(self.ports)
        self.fsm = self.new()

    def new(self) -> Fsm:
        return Fsm(comp=self.ctx, states=self.states)

    def eval_event(self, event: Event):
        try:
            G = 0
            return eval(repr(event))
        except NameError:
            raise ValueError(f"Invalid expression: {event}")

    def determine_states(self, ports: list[Port]) -> int:
        unique_events = set()

        for port in ports:
            if port.direction == Direction.IN:
                unique_events.add(port.range_.lo)
                unique_events.add(port.range_.hi)
            else:
                unique_events.add(port.range_.lo)

        # Evaluate unique symbolic expressions like G and G+1
        # Convert them into concrete indices if needed.
        concrete_events = {repr(event) for event in unique_events}
        return len(concrete_events)

    def connect_register(self, reg_name, cmd: Invoke):
        if reg_name == cmd.function:
            # Find the index of the Invoke command to insert after it
            index = self.ctx.commands.index(cmd)
            # Append the Connect commands immediately after the Invoke command

            self.ctx.commands[index + 1 : index + 1] = [
                Connect(
                    dest=f"{cmd.variable}.write_en",
                    src=self.fsm.port(cmd.range_.lo.eval_event()),
                ),
                Connect(
                    dest=f"{cmd.variable}.in",
                    src=self.fsm.port(cmd.range_.lo.eval_event()),
                    guard=cmd.ports[0],
                ),
            ]
            cmd.flag_lower()

    def process_command(self, cmd):
        if cmd.type_name == "Mux":
            raise NotImplementedError("Mux type is not implemented.")
        return cmd.type_name != "Register"

    def connect_comp(self, obj_name, cmd: Invoke):
        if obj_name == cmd.function:
            # Find the index of the Invoke command to insert after it
            index = self.ctx.commands.index(cmd)
            # Append the Connect commands immediately after the Invoke command

            self.ctx.commands[index + 1 : index + 1] = [
                Connect(
                    dest=f"{cmd.variable}.left",
                    src=self.fsm.port(cmd.range_.lo.eval_event()),
                    guard=cmd.ports[0],
                ),
                Connect(
                    dest=f"{cmd.variable}.right",
                    src=self.fsm.port(cmd.range_.lo.eval_event()),
                    guard=cmd.ports[1],
                ),
            ]
            cmd.flag_lower()

    def connect_fsm_ports(self):
        # Fetch invoke commands
        invokes = [cmd for cmd in self.ctx.commands if isinstance(cmd, Invoke)]
        registers = [
            cmd.variable
            for cmd in self.ctx.commands
            if isinstance(cmd, Instance) and cmd.type_name == "Register"
        ]
        objects = [
            cmd.variable
            for cmd in self.ctx.commands
            if isinstance(cmd, Instance) and self.process_command(cmd)
        ]

        for reg_name in registers:
            for cmd in invokes:
                self.connect_register(reg_name, cmd)

        for obj_name in objects:
            if obj_name.type_name == "Mux":
                raise NotImplementedError(f"Only two input components and registers are supported, not {obj_name} object!")
            for cmd in invokes:
                self.connect_comp(obj_name, cmd)

    def fsm_command(self):
        return self.fsm

    def generate(ctx: Component):
        generator = FSMgen(ctx)
        generator.connect_fsm_ports()
        generator.ctx.commands.append(generator.fsm_command())

        return ctx
