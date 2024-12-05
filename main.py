# from z3 import *
import pyfilament as pyf


if __name__ == '__main__':
    expr = pyf.parse("""
    (comp AddMult
      ((event G 2))
      ((interface go G 1) (in-port a (range G (+ G L)) 32) (in-port b (range G (+ G 1)) 32) (out-port out (range (+ G 2) (+ G 3))))
      ())
    """)

    sig = pyf.Signature(expr)

    print(expr)
    print(sig)


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