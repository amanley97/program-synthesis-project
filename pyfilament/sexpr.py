from z3 import Int


class SExpr:
    def __init__(self, l):
        self.as_list = l

    def eval(self):
        if not can_eval(self):
            raise RuntimeError("Expression is not arithmetic")

    def __getitem__(self, key):
        return self.as_list[key]

    def __str__(self):
        return "(" + " ".join(map(str, self.as_list)) + ")"

    def __repr__(self):
        return str(self)

    def __len__(self):
        return len(self.as_list)


def can_eval(expr: SExpr | str) -> bool:
    """
    Checks if a given SExpr contains only numbers or arithmetic operations
    """
    match expr:
        case SExpr():
            match expr[0]:
                case str(head):
                    return (
                        head in ("+", "-", "*", "/")
                        and len(expr) == 3
                        and can_eval(expr[1])
                        and can_eval(expr[2])
                    )
                case _:
                    return False
        case str(expr):
            if expr.isdecimal():
                return True
            if len(expr) > 0 and expr[0].isalpha():
                return True
            return False
        case _:
            raise TypeError("Expected SExpr or string")


def eval_expr(expr: SExpr | str) -> bool:
    """
    Turns an arithmetic SExpr into a Z3 expression that can be used as part of a constraint
    """
    match expr:
        case str(expr):
            if expr.isdecimal():
                return Int(int(expr))
            if len(expr) > 0 and expr[0].isalpha():
                return Int(expr)
            raise RuntimeError(f"Unable to evaluate {expr} as arithmetic expression")
        case SExpr():
            if len(expr) != 3:
                raise RuntimeError(f"Invalid arithmetic expression: {expr}")
            match expr[0]:
                case str(head):
                    if head == "+":
                        return eval_expr(expr[1]) + eval_expr(expr[2])
                    elif head == "-":
                        return eval_expr(expr[1]) - eval_expr(expr[2])
                    elif head == "*":
                        return eval_expr(expr[1]) * eval_expr(expr[2])
                    elif head == "/":
                        return eval_expr(expr[1]) / eval_expr(expr[2])
                    raise RuntimeError(f"Invalid arithmetic expression: {expr}")
                case _:
                    raise RuntimeError(f"Invalid arithmetic expression: {expr}")
        case _:
            raise TypeError("Expected SExpr or string")