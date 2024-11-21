from pyfilament.sexpr import SExpr

def parens_balanced(source: str) -> bool:
    count = 0

    for ch in source:
        if ch == '(':
            count += 1
        elif ch == ')':
            count -= 1
        if count < 0:
            return False

    return count == 0


def is_operator(c):
    return c in ('+', '-', '*', '/', '>', '<', '=')


def parse(source: str) -> SExpr:
    source = source.strip()
    assert(len(source) > 0 and source[0] == "(" and source[-1] == ")"), """
        S-Expression must be non-empty and must begin and end with parentheses.
    """

    if not parens_balanced(source):
        raise RuntimeError(f"Parentheses unbalanced in S-Expr: {source}")

    pos = 1
    expr = []
    current_term = ''

    while pos < len(source):
        if source[pos].isalnum() or is_operator(source[pos]):
            current_term += source[pos]
        else:
            if len(current_term) > 0:
                expr.append(current_term)
                current_term = ''

            if source[pos] == '(':
                depth = 0
                i = 1
                while source[pos + i] != ')' or depth > 0:
                    if source[pos + i] == '(':
                        depth += 1
                    elif source[pos + i] == ')':
                        depth -= 1
                    i += 1
                expr.append(parse(source[pos: pos + i + 1]))
                pos += i
            elif source[pos] == ')':
                return SExpr(expr)
            elif source[pos].isalnum():
                current_term += source[pos]

        pos += 1
    raise RuntimeError("Failed to parse S-Expression")

