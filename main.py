# from z3 import *
import pyfilament as pyf
from argparse import ArgumentParser

argv = ArgumentParser()
argv.add_argument("filename")

if __name__ == '__main__':
    args = argv.parse_args()
    expr = pyf.parse_file(args.filename)[0]
    print(f"S-Expression Form: \n-----\n{expr}\n")

    comp = pyf.Component.from_sexpr(expr)
    print(f"Component Object Form: \n-----\n{comp}\n")

    constraints = pyf.solve_component_constraints(comp)
    # print(constraints)

    lower_fil = pyf.generate_lower(comp)
    print(f"Lower Filament Form: \n-----\n{lower_fil}\n")

"""
comp main<G: 1>(
    @interface[G] go: 1,
    @[G, G+1] left: 32,
    @[G, G+1] right: 32,
    @[G+1, G+2] opt: 32,
) -> (@[G+3, G+4] out: 32) {
 
    // AND block
    A := new And[32];
    a0 := A<G>(left, right);
    and_stage := new Register[32]<G, G+2>(a0.out); // Register AND result
 
    // XOR block
    X := new Xor[32];
    x0 := X<G+1>(and_stage.out, opt);
    xor_stage := new Register[32]<G+1, G+3>(x0.out); // Register XOR result
 
    // Output register to satisfy timing
    r0 := new Register[32]<G+2, G+4>(xor_stage.out);
    out = r0.out;
}
"""

"""
(comp main
  (events
   (event G))
  (ports
   (interface[1] (G) go)  # G is not phantom in this component because it has an interface
   (in-port[32]  (G       (+ G 1)) left)
   (in-port[32]  (G       (+ G 1)) right)
   (in-port[32]  ((+ G 1) (+ G 2)) opt)
   (out-port[32] ((+ G 3) (+ G 4)) out))
  (instantiations
   (A (new And[32]))
   (X (new Xor[32])))
  (invocations
   (a0 (A (G) left right))
   (x0 (X (+ G 1) a0 opt)))
  (connect (out x0))
# (constraints (> L G)) # optional constraints over events, if there are multiple events
)
"""