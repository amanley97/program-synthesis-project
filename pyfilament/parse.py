from typing import List, Tuple

from pyfilament.sexpr import SExpr


def parens_balanced(source: str) -> bool:
    count = 0

    for ch in source:
        if ch == "(":
            count += 1
        elif ch == ")":
            count -= 1
        if count < 0:
            return False

    return count == 0


def is_operator(c):
    return c in ("+", "-", "*", "/", ">", "<", "=")


def append_if_nonempty(s: str | SExpr, l: List[str | SExpr]):
    if len(s) > 0:
        l.append(s)


def parse_expr(source: str) -> Tuple[SExpr, int]:
    """
    Parse a string into an S-expression representation.
    """
    source = source.strip()
    assert (
        len(source) > 0 and source[0] == "(" and source[-1] == ")"
    ), """
        S-Expression must be non-empty and must begin and end with parentheses.
    """

    if not parens_balanced(source):
        raise RuntimeError(f"Parentheses unbalanced in S-Expr: {source}")

    pos = 1
    expr = []
    current_term = ""

    while pos < len(source):
        if (
            source[pos].isalnum()
            or is_operator(source[pos])
            or source[pos] in ("[", "]")
        ):
            current_term += source[pos]
        else:
            if source[pos] == ";":  # comment
                append_if_nonempty(current_term, expr)
                while source[pos] != "\n":
                    pos += 1
            if len(current_term) > 0:
                append_if_nonempty(current_term, expr)
                current_term = ""
            if source[pos] == "(":
                depth = 0
                i = 1
                while source[pos + i] != ")" or depth > 0:
                    if source[pos + i] == "(":
                        depth += 1
                    elif source[pos + i] == ")":
                        depth -= 1
                    i += 1
                inner_expr, _ = parse_expr(source[pos : pos + i + 1])
                append_if_nonempty(inner_expr, expr)
                pos += i
            elif source[pos] == ")":
                return SExpr(expr), pos
            elif source[pos].isalnum():
                current_term += source[pos]

        pos += 1

    raise RuntimeError("Failed to parse S-Expression")


def parse(source: str) -> List[SExpr]:
    """
    Parse a string containing multiple S expressions
    """
    exprs = []
    pos = 0
    while pos < len(source):
        while pos < len(source) and source[pos] != "(":
            pos += 1
        if pos >= len(source):
            break
        else:
            expr, offset = parse_expr(source[pos:])
            exprs.append(expr)
            pos += offset
    return exprs


def parse_file(filepath: str):
    """
    Parse a file containing S Expressions
    """
    with open(filepath, "r", encoding="utf-8") as fp:
        return parse(fp.read())
