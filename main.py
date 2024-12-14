from argparse import ArgumentParser

import pyfilament as pyf

argv = ArgumentParser()
argv.add_argument("filename")
argv.add_argument("--debug", action="store_true", default=False)

if __name__ == "__main__":
    args = argv.parse_args()
    expr = pyf.parse_file(args.filename)[0]
    if args.debug:
        print(f"S-Expression Form: \n-----\n{expr}\n")

    comp = pyf.Component.from_sexpr(expr)
    if args.debug:
        print(f"Component Object Form: \n-----\n{comp}\n")

    constraints = pyf.solve_component_constraints(comp)
    if args.debug:
        print(f"Z3-Solver Constraints: \n-----\n{constraints}\n")

    lower_fil = pyf.generate_lower(comp)
    print(f"Lower Filament Form: \n-----\n{lower_fil}\n")
