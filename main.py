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
