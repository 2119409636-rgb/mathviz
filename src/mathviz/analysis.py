"""Symbolic analysis helpers using SymPy.

Provides functions for derivative, integral, Taylor series and critical points.
"""
from typing import Tuple, List
import sympy as sp


def parse_expression(expr_str: str, symbol_name: str = "x") -> sp.Expr:
    """Parse a string expression into a SymPy expression.

    Args:
        expr_str: expression string, e.g. "sin(x)*exp(-x**2)"
        symbol_name: independent variable name

    Returns:
        sympy expression
    """
    x = sp.symbols(symbol_name)
    expr = sp.sympify(expr_str, locals={})
    return expr


def derivative(expr: sp.Expr, var: sp.Symbol = None) -> sp.Expr:
    """Return symbolic derivative of `expr` with respect to its first symbol."""
    if var is None:
        var = list(expr.free_symbols)[0]
    return sp.diff(expr, var)


def integral(expr: sp.Expr, var: sp.Symbol = None) -> sp.Expr:
    """Return indefinite integral (antiderivative)."""
    if var is None:
        var = list(expr.free_symbols)[0]
    return sp.integrate(expr, var)


def taylor_series(expr: sp.Expr, x0=0, n=6, var: sp.Symbol = None) -> sp.Expr:
    """Return Taylor series expansion around x0 up to order n-1 (SymPy series)."""
    if var is None:
        var = list(expr.free_symbols)[0]
    ser = sp.series(expr, var, x0, n).removeO()
    return ser


def critical_points(expr: sp.Expr, var: sp.Symbol = None) -> List[Tuple]:
    """Compute critical points (solutions of f'(x)=0) and classify via second derivative.

    Returns list of tuples: (point, classification_string)
    """
    if var is None:
        var = list(expr.free_symbols)[0]
    f1 = sp.diff(expr, var)
    sols = sp.solve(sp.Eq(f1, 0), var)
    results = []
    f2 = sp.diff(f1, var)
    for s in sols:
        try:
            val = f2.subs(var, s)
            if val.is_real:
                if val > 0:
                    typ = "min"
                elif val < 0:
                    typ = "max"
                else:
                    typ = "saddle/inflection"
            else:
                typ = "complex"
        except Exception:
            typ = "unknown"
        results.append((s, typ))
    return results
