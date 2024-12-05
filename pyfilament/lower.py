from command import Invoke, Instance, Connect
from component import Component, Signature
from port import Port, InterfacePort
from fsm import Fsm

def generate_lower(component: Component):
    """
        Entry point to transform a component into lower filament.

        Args:
            component (Component): Component to be transformed.
        """
    lower_fil = FSMgen.generate(component)
    print(lower_fil)

class FSMgen:
    def __init__(self, ctx:Component):
        """
        Initialize the FSM generator with FSM details and context.
        """
        self.ctx = ctx
        self.ports = ctx.signature.in_ports + ctx.signature.out_ports
        self.states = self.determine_states(self.ports)
        self.fsm = self.new()

    def new(self) -> Fsm:
        return Fsm(comp=self.ctx, states=self.states)
    
    def eval_event(self, event:str):

        G = 0  # Assign the base value for G (e.g., G = 0)
        try:
            return eval(event)  # Evaluate the symbolic expression
        except NameError:
            raise ValueError(f"Invalid symbolic expression: {event}")

    def determine_states(self, ports:list[Port]) -> int:
        unique_events = set()

        for port in ports:
            start, end = port.range_  # Unpack the range
            unique_events.add(start)
            unique_events.add(end)

        # Evaluate unique symbolic expressions like G and G+1
        # Convert them into concrete indices if needed.
        concrete_events = {self.eval_event(event) for event in unique_events}
        return len(concrete_events)

    def connect_register(self, reg_name, cmd):
        if reg_name == cmd.function:
            # Find the index of the Invoke command to insert after it
            index = self.ctx.commands.index(cmd)
            # Append the Connect commands immediately after the Invoke command
            self.ctx.commands[index + 1:index + 1] = [
                Connect(dest=f"{cmd.variable}.write_en", 
                        src=self.fsm.port(self.eval_event(cmd.range_[0]))),
                Connect(dest=f"{cmd.variable}.in", 
                        src=self.fsm.port(self.eval_event(cmd.range_[0])), 
                        guard=cmd.ports[0])
            ]

    def connect_comp(self, obj_name, cmd):
        if obj_name == cmd.function:
            # Find the index of the Invoke command to insert after it
            index = self.ctx.commands.index(cmd)
            # Append the Connect commands immediately after the Invoke command
            self.ctx.commands[index + 1:index + 1] = [
                Connect(dest=f"{cmd.variable}.left", 
                        src=self.fsm.port(self.eval_event(cmd.range_)),
                        guard=cmd.ports[0]),
                Connect(dest=f"{cmd.variable}.right", 
                        src=self.fsm.port(self.eval_event(cmd.range_)), 
                        guard=cmd.ports[1])
            ]

    def connect_fsm_ports(self):
        # Fetch invoke commands
        invokes = [cmd for cmd in self.ctx.commands if isinstance(cmd, Invoke)]
        registers = [cmd.variable for cmd in self.ctx.commands if isinstance(cmd, Instance) and cmd.type_name == "Register"]
        objects = [cmd.variable for cmd in self.ctx.commands if isinstance(cmd, Instance) and cmd.type_name != "Register"]

        for reg_name in registers:
            for cmd in invokes:
                self.connect_register(reg_name, cmd)

        for obj_name in objects:
            for cmd in invokes:
                self.connect_comp(obj_name, cmd)

    def fsm_command(self):
        return self.fsm

    def generate(ctx: Component):
        generator = FSMgen(ctx)
        generator.connect_fsm_ports()
        generator.ctx.commands.append(generator.fsm_command())

        return ctx

if __name__ == "__main__":

    test_component = Component(
        signature=Signature(
            name='main',
            event='G',
            interface=InterfacePort(
                name='go',
                event='G',
                width=1
            ),
            in_ports= [
                Port(name='left', direction='in', range_=('G', 'G+1'), width=32),
                Port(name='right', direction='in', range_=('G', 'G+1'), width=32),
                Port(name='opt', direction='in', range_=('G+1', 'G+2'), width=32),
            ],
            out_ports= [
                Port(name='out', direction='out', range_=('G+2', 'G+3'), width=32),
            ]
        ),
        commands = [
            Instance(variable="A", type_name="And", size=32),
            Instance(variable="X", type_name="Xor", size=32),
            Instance(variable="AND_STAGE", type_name="Register", size=32),
            Instance(variable="XOR_STAGE", type_name="Register", size=32),
            Instance(variable="R0", type_name="Register", size=32),

            Invoke(variable="a0", function="A", range_=("G"), ports=["left", "right"]),
            Invoke(variable="and_stage", function="AND_STAGE", range_=("G","G+2"), ports=["a0.out"]),
            Invoke(variable="x0", function="X", range_=("G+1"), ports=["and_stage.out", "opt"]),
            Invoke(variable="xor_stage", function="XOR_STAGE", range_=("G+1", "G+3"), ports=["x0.out"]),
            Invoke(variable="r0", function="R0", range_=("G+2","G+4"), ports=["xor_stage.out"]),

            Connect(src="r0.out", dest="out"),
        ]
    )

    generate_lower(test_component)