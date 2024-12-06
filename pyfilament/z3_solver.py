from z3 import Int, Solver, Or, And, Implies

from pyfilament.command import Instance, Invoke, Connect
from pyfilament.component import Component
from pyfilament.signature import Signature
from pyfilament.port import Port, InterfacePort


def solve_component_constraints(component):
    """
    Argsuments- component: A Component instance containing its signature and commands.

    Returns-  A dictionary with resolved start times and FSM state transitions.
    """
    solver = Solver()

    # Define start times for all commands
    start_times = {cmd.variable: Int(f"{cmd.variable}_start") for cmd in component.commands if hasattr(cmd, 'variable')}

    # Define FSM states and add state constraints
    fsm_states = component.signature.event
    states = {f"{fsm_states}_{i}": Int(f"{fsm_states}_{i}_active") for i in range(4)}  # Assuming 4 cycles

    # Timing constraints for commands
    for cmd in component.commands:
        if isinstance(cmd, Instance):
            solver.add(start_times[cmd.variable] >= 0)  # Non-negative start time

        elif isinstance(cmd, Invoke):
            # Add timing constraints based on range
            range_start, range_end = map(range_to_cycle, cmd.range_)
            solver.add(start_times[cmd.variable] >= range_start)
            solver.add(start_times[cmd.variable] <= range_end)

        elif isinstance(cmd, Connect):
            # Ensure connection happens only after the source produces its output
            src_start_time = start_times.get(cmd.src.split('.')[0], None)
            dest_start_time = start_times.get(cmd.dest.split('.')[0], None)
            if src_start_time and dest_start_time:
                solver.add(dest_start_time >= src_start_time)

    # FSM constraints
    for cycle in range(4):  # Assume 4 cycles for the example
        solver.add(Or([states[f"{fsm_states}_{i}"] == 1 for i in range(4)]))  # Ensure one state active per cycle
        if cycle < 3:  # Add transitions between states
            solver.add(Implies(states[f"{fsm_states}_{cycle}"] == 1, states[f"{fsm_states}_{cycle + 1}"] == 1))

    # Solve constraints
    if solver.check() == "sat":
        model = solver.model()
        results = {
            "start_times": {cmd.variable: model[start_times[cmd.variable]].as_long() for cmd in start_times},
            "states": {state: model[states[state]].as_long() for state in states},
        }
        return results
    else:
        return None


def range_to_cycle(range_expr):
    """
    Convert a range expression (e.g., 'G', 'G+1') to a cycle number.
    """
    # Map ranges to cycle numbers for simplicity
    mapping = {'G': 0, 'G+1': 1, 'G+2': 2, 'G+3': 3}
    return mapping.get(range_expr, -1)


if __name__ == "__main__":
    # Define the test component
    test_component = Component(
        signature=Signature(
            name='main',
            event='G',
            interface=InterfacePort(
                name='go',
                event='G',
                width=1
            ),
            in_ports=[
                Port(name='left', direction='in', range_=('G', 'G+1'), width=32),
                Port(name='right', direction='in', range_=('G', 'G+1'), width=32),
                Port(name='opt', direction='in', range_=('G+1', 'G+2'), width=32),
            ],
            out_ports=[
                Port(name='out', direction='out', range_=('G+2', 'G+3'), width=32),
            ]
        ),
        commands=[
            Instance(variable='A', type_name='And', size=32),
            Instance(variable='X', type_name='Xor', size=32),
            Invoke(variable='a0', function='A', range_=('G', 'G+1'), ports=['left', 'right']),
            Invoke(variable='x0', function='X', range_=('G+1', 'G+2'), ports=['a0.out', 'opt']),
            Connect(src='x0.out', dest='out'),
        ]
    )

    # Solve constraints for the component
    results = solve_component_constraints(test_component)
    if results:
        print("Constraint Results:")
        print("Start Times:", results["start_times"])
        print("FSM States:", results["states"])
    else:
        print("No solution found.")
