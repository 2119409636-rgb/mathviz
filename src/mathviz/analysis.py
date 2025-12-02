"""Symbolic analysis helpers using SymPy.

Provides functions for derivative, integral, Taylor series and critical points.
"""
from typing import Tuple, List, Callable
import sympy as sp
import numpy as np


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

    Returns list of tuples: (point, classification_string).
    If solving fails for some expressions, returns empty list with a note.
    """
    if var is None:
        var = list(expr.free_symbols)[0]
    f1 = sp.diff(expr, var)
    try:
        sols = sp.solve(sp.Eq(f1, 0), var)
    except (NotImplementedError, ValueError) as e:
        # Some transcendental equations cannot be solved symbolically
        return [("(Unable to solve symbolically)", str(type(e).__name__))]
    
    results = []
    f2 = sp.diff(f1, var)
    for s in sols:
        try:
            val = f2.subs(var, s)
            if val.is_real:
                if val > 0:
                    typ = "local min"
                elif val < 0:
                    typ = "local max"
                else:
                    typ = "possible inflection"
            else:
                typ = "complex"
        except Exception:
            typ = "unknown"
        results.append((s, typ))
    return results


def inflection_points(expr: sp.Expr, var: sp.Symbol = None) -> List[Tuple]:
    """Compute inflection points (solutions of f''(x)=0) and check if f'''(x)≠0.

    Returns list of tuples: (point, classification_string).
    """
    if var is None:
        var = list(expr.free_symbols)[0]
    f1 = sp.diff(expr, var)
    f2 = sp.diff(f1, var)
    try:
        sols = sp.solve(sp.Eq(f2, 0), var)
    except (NotImplementedError, ValueError) as e:
        return [("(Unable to solve symbolically)", str(type(e).__name__))]
    
    results = []
    f3 = sp.diff(f2, var)
    for s in sols:
        try:
            val3 = f3.subs(var, s)
            if val3.is_real:
                if val3 != 0:
                    typ = "inflection"
                else:
                    typ = "possible higher-order"
            else:
                typ = "complex"
        except Exception:
            typ = "unknown"
        results.append((s, typ))
    return results


def parse_parametric(x_str: str, y_str: str, z_str: str = None) -> Tuple[Callable, Callable, Callable]:
    """Parse parametric equations and return numeric callables.
    
    Args:
        x_str: Expression for x(t)
        y_str: Expression for y(t)
        z_str: Optional expression for z(t)
    
    Returns:
        Tuple of (x_func, y_func, z_func) where each is a numpy-compatible callable
    """
    t = sp.symbols('t')
    x_expr = sp.sympify(x_str)
    y_expr = sp.sympify(y_str)
    z_expr = sp.sympify(z_str) if z_str else None
    
    x_func = sp.lambdify(t, x_expr, modules=["numpy", "mpmath"])
    y_func = sp.lambdify(t, y_expr, modules=["numpy", "mpmath"])
    z_func = sp.lambdify(t, z_expr, modules=["numpy", "mpmath"]) if z_expr else None
    
    return x_func, y_func, z_func


def parse_complex_function(expr_str: str) -> Callable:
    """Parse a complex function f(z) and return a numeric callable.
    
    Args:
        expr_str: Expression using 'z' as the complex variable
    
    Returns:
        Callable that takes complex input and returns complex output
    """
    z = sp.symbols('z')
    expr = sp.sympify(expr_str)
    f = sp.lambdify(z, expr, modules=["numpy", "mpmath"])
    return f


def parse_implicit_function(expr_str: str) -> Callable:
    """Parse an implicit function f(x, y) and return a numeric callable.
    
    Args:
        expr_str: Expression using 'x' and 'y' as variables
    
    Returns:
        Callable that takes numpy arrays (x, y) and returns f(x, y)
    """
    x, y = sp.symbols('x y')
    expr = sp.sympify(expr_str)
    f = sp.lambdify((x, y), expr, modules=["numpy", "mpmath"])
    return f
