from z3 import Int, Solver

def solve_timing_constraints(operations, dependencies):
    """
    Solve timing constraints using Z3.

    Args:
        operations: List of operations, each represented as a dictionary with keys:
            - name: Unique operation name
            - type: Operation type (e.g., "Add", "Multiply")
            - cycles: Number of cycles required for the operation
        dependencies: List of dependencies, each represented as a dictionary with keys:
            - before: Name of the operation that must finish first
            - after: Name of the operation that depends on "before"

    Returns:
        A dictionary mapping operation names to their start times, or None if no solution exists.
    """
    # Create a solver instance
    solver = Solver()

    # Create Z3 variables for the start times of each operation
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

    # Solve the constraints
    if solver.check() == "sat":
        model = solver.model()
        return {op["name"]: model[start_times[op["name"]]].as_long() for op in operations}
    else:
        return None
