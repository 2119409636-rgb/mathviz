import sympy as sp


def test_derivative_sin():
    x = sp.symbols('x')
    f = sp.sin(x)
    df = sp.diff(f, x)
    assert sp.simplify(df - sp.cos(x)) == 0
