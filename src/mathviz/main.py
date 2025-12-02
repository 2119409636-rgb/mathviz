"""Command-line entry for mathviz.

Example:
    uv run python -m mathviz.main --expr "sin(x)*exp(-x**2)" --xmin -5 --xmax 5

"""
from __future__ import annotations
import argparse
from typing import List
import numpy as np
import sympy as sp

from .analysis import parse_expression, derivative, integral, taylor_series, critical_points
from .plotter import plot_2d, plot_multiple_2d


def _prepare_numeric(expr: sp.Expr, var: sp.Symbol, xmin: float, xmax: float, points: int = 400):
    f = sp.lambdify(var, expr, modules=["numpy", "mpmath"])  # numeric callable
    x = np.linspace(xmin, xmax, points)
    y = f(x)
    return x, np.array(y)


def main(argv: List[str] | None = None):
    parser = argparse.ArgumentParser(description="mathviz — 数学函数可视化工具")
    parser.add_argument("--expr", required=True, help="数学表达式，多个用分号分隔，例如: 'sin(x);cos(x)'")
    parser.add_argument("--xmin", type=float, default=-5.0)
    parser.add_argument("--xmax", type=float, default=5.0)
    parser.add_argument("--points", type=int, default=600)
    parser.add_argument("--save", help="保存输出图像路径（可选）")
    args = parser.parse_args(argv)

    exprs = [s.strip() for s in args.expr.split(";") if s.strip()]
    series = []
    for e in exprs:
        sym = parse_expression(e, symbol_name="x")
        x_sym = list(sym.free_symbols)[0] if sym.free_symbols else sp.symbols('x')
        # analysis printouts
        print("Expression:", sym)
        print("Derivative:", derivative(sym, x_sym))
        print("Indefinite integral (symbolic):", integral(sym, x_sym))
        print("Taylor (order 6):", taylor_series(sym, 0, 6, x_sym))
        cp = critical_points(sym, x_sym)
        print("Critical points:", cp)

        # numeric evaluation
        x_num, y_num = _prepare_numeric(sym, x_sym, args.xmin, args.xmax, args.points)
        label = e
        series.append((x_num, y_num, label))

    if len(series) == 1:
        x, y, _ = series[0]
        plot_2d(x, y, title=str(series[0][2]), savepath=args.save)
    else:
        plot_multiple_2d(series, title="Comparison", savepath=args.save)


if __name__ == "__main__":
    main()
