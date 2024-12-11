from z3 import sat, Int, Solver, Or, And, Implies

from pyfilament.command import Instance, Invoke, Connect
from pyfilament.component import Component
from pyfilament.signature import Signature
from pyfilament.port import Port, InterfacePort
from pyfilament.sexpr import can_eval, eval_expr


def solve_component_constraints(component: Component):
    """
    Argsuments- component: A Component instance containing its signature and commands.

    Returns-  A dictionary with resolved start times and FSM state transitions.
    """
    solver = Solver()

    # Define start times for all commands
    start_times = {
        cmd.variable: Int(f"{cmd.variable}_start")
        for cmd in component.commands
        if hasattr(cmd, "variable")
    }

    # use ports from signature
    for port in component.signature.in_ports:
        start_times[port.name] = eval_expr(port.range_[0])
    for port in component.signature.out_ports:
        start_times[port.name] = eval_expr(port.range_[0])

    # Define FSM states and add state constraints
    # here event is a list of event definitions as SExprs
    fsm_states = component.signature.event[0][1]
    states = {
        f"{fsm_states}_{i}": Int(f"{fsm_states}_{i}_active") for i in range(4)
    }  # Assuming 4 cycles

    solver.add(Int("G") == 0)
    # Timing constraints for commands
    for cmd in component.commands:
        if isinstance(cmd, Instance):
            # pass
            solver.add(start_times[cmd.variable] >= 0)  # Non-negative start time

        elif isinstance(cmd, Invoke):
            # Add timing constraints based on range
            if len(cmd.range_) == 1:
                solver.add(start_times[cmd.variable] == range_to_cycle(cmd.range_[0]))
            elif len(cmd.range_) == 2:
                solver.add(start_times[cmd.variable] >= range_to_cycle(cmd.range_[0]))
                solver.add(start_times[cmd.variable] <= range_to_cycle(cmd.range_[1]))
            elif len(cmd.range_) == 3:
                solver.add(start_times[cmd.variable] == 3)
            else:
                raise RuntimeError(
                    f"Too many timing constraints in invocation - {cmd}: {cmd.range_}"
                )
            # range_start, range_end = map(range_to_cycle, cmd.range_)
            # solver.add(start_times[cmd.variable] >= range_start)
            # solver.add(start_times[cmd.variable] <= range_end)

        elif isinstance(cmd, Connect):
            # Ensure connection happens only after the source produces its output
            src_start_time = start_times.get(cmd.src.split(".")[0], None)
            dest_start_time = start_times.get(cmd.dest.split(".")[0], None)
            if src_start_time is not None and dest_start_time is not None:
                solver.add(dest_start_time >= src_start_time)
            else:
                if src_start_time is None:
                    raise RuntimeError(f"Missing start time for variable {cmd.src}")
                elif dest_start_time is None:
                    raise RuntimeError(f"Missing start time for variable {cmd.dest}")

    # FSM constraints
    for cycle in range(4):  # Assume 4 cycles for the example
        solver.add(
            Or([states[f"{fsm_states}_{i}"] == 1 for i in range(4)])
        )  # Ensure one state active per cycle
        if cycle < 3:  # Add transitions between states
            solver.add(
                Implies(
                    states[f"{fsm_states}_{cycle}"] == 1,
                    states[f"{fsm_states}_{cycle + 1}"] == 1,
                )
            )

    # Solve constraints
    if solver.check() == sat:
        model = solver.model()
        print(model)
        results = {
            "start_times": start_times,
            "states": {state: model[states[state]].as_long() for state in states},
        }
        return results
    else:
        # print(solver.assertions())
        return None


def range_to_cycle(range_expr):
    """
    Convert a range expression (e.g., 'G', 'G+1') to a cycle number.
    """
    # Map ranges to cycle numbers for simplicity
    if len(range_expr) == 1:
        return 0
    return range_expr[2]
    mapping = {"G": 0, "G+1": 1, "G+2": 2, "G+3": 3}
    return mapping.get(range_expr, -1)
