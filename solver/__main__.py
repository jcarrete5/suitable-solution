"""
"""

from argparse import ArgumentParser

from .divide import eval_expr

parser = ArgumentParser(
    description="Takes serial division expressions as arguments and "
                "prints the solution to each expression on a new line."
)
parser.add_argument(
    'expr_list',
    nargs='+',
    type=str,
    metavar='expr',
    help="Expression to be evaluated"
)
args = parser.parse_args()  # Exits on invalid arguments

for expr in args.expr_list:
    print(eval_expr(expr))
