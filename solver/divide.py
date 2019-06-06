def eval_expr(expr: str) -> float:
    """
    Evaluates the string expression `expr`.

    `expr` should be a string representing a list of numbers with
    optional nested lists of numbers to be divided in the appropriate
    order e.g. `'[[16,[8,2],4],2,80]'`
    """
    # Assume we can trust our inputs
    expr = expr.replace('[', '(').replace(']', ')').replace(',', '/')
    return eval(expr)
