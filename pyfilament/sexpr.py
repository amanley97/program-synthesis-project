from z3 import Int, ArithRef


class SExpr:
    def __init__(self, l):
        self.as_list = l

    def eval(self):
        if not can_eval(self):
            raise RuntimeError("Expression is not arithmetic")

    def arithmetic(self) -> str:
        if not can_eval(self):
            raise RuntimeError("Expression is not arithmetic")
        if len(self) == 1:
            return f"{self[0]}"
        else:
            return f"{'(' + self[1].arithmetic() + ')' if isinstance(self[1], SExpr) else self[1]} {self[0]} {'(' + self[2].arithmetic() + ')' if isinstance(self[2], SExpr) else self[2]}"

    def __getitem__(self, key):
        if isinstance(key, int) or isinstance(key, slice):
            return self.as_list[key]
        elif isinstance(key, str):
            for i, item in enumerate(self.as_list):
                if isinstance(item, str):
                    if item == key and i + 1 < len(self):
                        return self[i + 1]
                elif isinstance(item, SExpr):
                    if len(item) > 0 and isinstance(item[0], str):
                        if item[0] == key:
                            return item.as_list[1:]

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


def print_expr(expr: SExpr):
    """
    expects (G) or (+ G 3)
    """
    if len(expr) == 1:
        return expr[0]
    elif len(expr) == 3:
        return f"{expr[1]}{expr[0]}{expr[2]}"


def eval_expr(expr: SExpr | str):
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
            if len(expr) == 1:
                return eval_expr(expr[0])
            elif len(expr) != 3:
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
