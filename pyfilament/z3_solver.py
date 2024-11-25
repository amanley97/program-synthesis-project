from z3 import Int, Solver, Or

def solve_fsm_constraints(operations, dependencies, fsm_states):
    """
    Solve timing and FSM constraints using Z3.

    Args:
        operations: List of operations, each represented as a dictionary with keys:
            - name: Unique operation name
            - type: Operation type (e.g., "Add", "Multiply")
            - cycles: Number of cycles required for the operation
        dependencies: List of dependencies between operations.
        fsm_states: FSM state definitions as a list of dictionaries with keys:
            - name: State name.
            - transitions: List of transitions (tuples) with conditions.

    Returns:
        A dictionary with operation start times and FSM state transitions.
    """
    solver = Solver()

    # Create Z3 variables for operation start times
    start_times = {op["name"]: Int(f"{op['name']}_start") for op in operations}

    # Add constraints: All operations must start at or after cycle 0
    for op in operations:
        solver.add(start_times[op["name"]] >= 0)

    # Add dependency constraints
    for dep in dependencies:
        before = dep["before"]
        after = dep["after"]
        before_cycles = next(op["cycles"] for op in operations if op["name"] == before)
        solver.add(start_times[after] >= start_times[before] + before_cycles)

    # Create Z3 variables for FSM states
    states = {state["name"]: Int(f"{state['name']}_active") for state in fsm_states}

    # Add FSM state transition constraints
    for state in fsm_states:
        current_state = states[state["name"]]
        transitions = state.get("transitions", [])

        # Ensure exactly one state is active at any given time
        solver.add(Or([current_state == 1 for state in fsm_states]))

        # Add transition conditions
        for target, condition in transitions:
            target_state = states[target]
            solver.add(Implies(condition, target_state == 1))

    # Solve the constraints
    if solver.check() == "sat":
        model = solver.model()
        result = {
            "start_times": {op["name"]: model[start_times[op["name"]]].as_long() for op in operations},
            "states": {state["name"]: model[states[state["name"]]] for state in fsm_states}
        }
        return result
    else:
        return None
