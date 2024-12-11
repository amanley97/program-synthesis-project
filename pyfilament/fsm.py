from pyfilament.component import Component


class Fsm:
    def __init__(self, comp: Component, states: int):
        """
        Initialize the FSM with a name, states, and a trigger.
        """
        self.component = comp
        self.states = states
        self.trigger = comp.signature.interface
        self.name = f"{self.trigger.event}_fsm"

    def __repr__(self):
        return f"fsm {self.name}[{self.states}]({self.trigger.name})"

    def port(self, state):
        """
        Return the port associated with the given state.
        """
        return f"{self.name}._{state}"
