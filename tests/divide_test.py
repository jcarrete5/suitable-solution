from collections import namedtuple

import pytest

from solver.divide import eval_expr

Pair = namedtuple('Pair', 'expr result')
ErrorPair = namedtuple('ErrorPair', 'expr error')


@pytest.fixture
def expr_list() -> list:
    return [
        Pair('[[16,[8,2],4],2,80]', 0.00625),
        Pair('[1]', 1),
        Pair('[[4]]', 4),
        Pair('[4,-2,[6,3],[100,-10]]', 0.1)
    ]


@pytest.fixture
def error_expr_list() -> list:
    return [
        ErrorPair('[1,0]', ZeroDivisionError),
        ErrorPair('[10,3,[5,0]]', ZeroDivisionError),
        ErrorPair('[[1,3]', SyntaxError)
    ]


def test_eval_expr(expr_list: list, error_expr_list: list):
    for test in expr_list:
        assert eval_expr(test.expr) == test.result
    for test in error_expr_list:
        with pytest.raises(test.error):
            eval_expr(test.expr)
