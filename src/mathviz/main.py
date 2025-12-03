"""Command-line entry for mathviz.

Example:
    uv run python -m mathviz.main --expr "sin(x)*exp(-x**2)" --xmin -5 --xmax 5

"""
from __future__ import annotations
import argparse
from typing import List
import numpy as np
import sympy as sp

from .analysis import (parse_expression, derivative, integral, taylor_series, 
                       critical_points, inflection_points, parse_parametric,
                       parse_complex_function, parse_implicit_function)
from .plotter import plot_2d, plot_multiple_2d, plot_3d, complex_plot, implicit_plot, parametric_plot


def _parse_float_or_expr(s: str) -> float:
    """Parse a string as either a float or a sympy expression (e.g., '4*pi', '2**2')."""
    try:
        return float(s)
    except ValueError:
        try:
            return float(sp.sympify(s))
        except Exception:
            raise ValueError(f"Cannot parse '{s}' as float or symbolic expression")


def _prepare_numeric(expr: sp.Expr, var: sp.Symbol, xmin: float, xmax: float, points: int = 400):
    f = sp.lambdify(var, expr, modules=["numpy", "mpmath"])  # numeric callable
    x = np.linspace(xmin, xmax, points)
    y = f(x)
    return x, np.array(y)


def main(argv: List[str] | None = None):
    parser = argparse.ArgumentParser(description="mathviz — 数学函数可视化工具")
    parser.add_argument("--expr", help="数学表达式，多个用分号分隔，例如: 'sin(x);cos(x)'")
    parser.add_argument("--xmin", type=float, default=-5.0)
    parser.add_argument("--xmax", type=float, default=5.0)
    parser.add_argument("--points", type=int, default=600)
    parser.add_argument("--save", help="保存输出图像路径（可选）")
    parser.add_argument("--3d", action="store_true", help="使用 3D 表面绘图（仅限单个表达式）")
    
    # Complex function options
    parser.add_argument("--complex", metavar="EXPR", help="复变函数表达式，使用 'z' 作为复变量，例如: 'z**2'")
    parser.add_argument("--complex-mode", choices=["magnitude", "phase"], default="magnitude", 
                       help="复函数可视化模式")
    
    # Implicit function options
    parser.add_argument("--implicit", metavar="EXPR", help="隐函数表达式 f(x,y)=0，例如: 'x**2 + y**2 - 1'")
    parser.add_argument("--ymin", type=float, default=-5.0)
    parser.add_argument("--ymax", type=float, default=5.0)
    
    # Parametric options
    parser.add_argument("--parametric-x", help="参数方程 x(t)")
    parser.add_argument("--parametric-y", help="参数方程 y(t)")
    parser.add_argument("--parametric-z", help="参数方程 z(t)（可选，用于 3D）")
    parser.add_argument("--tmin", type=str, default="0", help="参数 t 的最小值（支持表达式如 '0'）")
    parser.add_argument("--tmax", type=str, default="2*pi", help="参数 t 的最大值（支持表达式如 '2*pi'）")
    
    args = parser.parse_args(argv)
    
    # Handle complex function visualization
    if args.complex:
        print("\n" + "="*70)
        print(f"[复变函数] {args.complex}")
        print("="*70)
        try:
            f_complex = parse_complex_function(args.complex)
            complex_plot(f_complex, args.xmin, args.xmax, args.ymin, args.ymax,
                        resolution=300, mode=args.complex_mode, 
                        title=f"Complex: {args.complex} ({args.complex_mode})",
                        savepath=args.save)
        except Exception as e:
            print(f"⚠ 复变函数可视化失败: {e}")
        return
    
    # Handle implicit function visualization
    if args.implicit:
        print("\n" + "="*70)
        print(f"[隐函数] {args.implicit} = 0")
        print("="*70)
        try:
            f_implicit = parse_implicit_function(args.implicit)
            implicit_plot(f_implicit, args.xmin, args.xmax, args.ymin, args.ymax,
                         resolution=400, title=f"Implicit: {args.implicit} = 0",
                         savepath=args.save)
        except Exception as e:
            print(f"⚠ 隐函数绘图失败: {e}")
        return
    
    # Handle parametric equations
    if args.parametric_x and args.parametric_y:
        print("\n" + "="*70)
        print(f"[参数方程] x(t) = {args.parametric_x}")
        print(f"         y(t) = {args.parametric_y}")
        if args.parametric_z:
            print(f"         z(t) = {args.parametric_z}")
        print("="*70)
        try:
            tmin = _parse_float_or_expr(args.tmin)
            tmax = _parse_float_or_expr(args.tmax)
            x_func, y_func, z_func = parse_parametric(args.parametric_x, args.parametric_y, args.parametric_z)
            parametric_plot(x_func, y_func, tmin, tmax, z_func,
                           n_points=1000,
                           title=f"Parametric curve (t ∈ [{args.tmin}, {args.tmax}])",
                           savepath=args.save)
        except Exception as e:
            print(f"⚠ 参数方程绘图失败: {e}")
        return
    
    # Default: Handle regular expression(s)
    if not args.expr:
        parser.print_help()
        return
    
    exprs = [s.strip() for s in args.expr.split(";") if s.strip()]
    
    if getattr(args, '3d') and len(exprs) > 1:
        print("⚠ 警告: 3D 绘图仅支持单个表达式，将忽略 --3d 选项")
        setattr(args, '3d', False)
    
    series = []
    for idx, e in enumerate(exprs):
        sym = parse_expression(e, symbol_name="x")
        x_sym = list(sym.free_symbols)[0] if sym.free_symbols else sp.symbols('x')
        
        # Pretty-print analysis results
        print("\n" + "="*70)
        print(f"[表达式 {idx+1}] {sym}")
        print("="*70)
        
        print("\n📊 符号分析:")
        print(f"  导数:        {derivative(sym, x_sym)}")
        print(f"  积分:        {integral(sym, x_sym)}")
        print(f"  泰勒展开(6阶): {taylor_series(sym, 0, 6, x_sym)}")
        
        print("\n🔍 极值点:")
        cp = critical_points(sym, x_sym)
        # If symbolic solver couldn't solve, try numeric fallback within [xmin,xmax]
        if cp and isinstance(cp[0][0], str) and "Unable to solve" in cp[0][0]:
            print("    (符号求解失败，尝试数值搜索...)")
            try:
                from .analysis import numeric_critical_points
                ncp = numeric_critical_points(sym, x_sym, args.xmin, args.xmax, samples=2000)
                if ncp:
                    for pt, typ in ncp:
                        print(f"    {pt:.6g} ({typ})")
                else:
                    print("    (数值未找到根)")
            except Exception as e:
                print(f"    (数值回退失败: {e})")
        else:
            if cp:
                for pt, typ in cp:
                    print(f"    {pt} ({typ})")
            else:
                print("    (无)")
        
        print("\n📐 拐点:")
        ip = inflection_points(sym, x_sym)
        if ip and isinstance(ip[0][0], str) and "Unable to solve" in ip[0][0]:
            print("    (符号求解失败，尝试数值搜索...)")
            try:
                # use numeric_inflection_points to find f''(x)=0 roots and classify them correctly
                from .analysis import numeric_inflection_points
                nips = numeric_inflection_points(sym, x_sym, args.xmin, args.xmax, samples=2000)
                if nips:
                    for pt, typ in nips:
                        print(f"    {pt:.6g} ({typ})")
                else:
                    print("    (数值未找到拐点)")
            except Exception as e:
                print(f"    (数值回退失败: {e})")
        else:
            if ip:
                for pt, typ in ip:
                    print(f"    {pt} ({typ})")
            else:
                print("    (无)")

        # numeric evaluation
        x_num, y_num = _prepare_numeric(sym, x_sym, args.xmin, args.xmax, args.points)
        label = e
        # collect markers for extrema/inflection to annotate the plot
        local_markers = []
        # extrema (symbolic or numeric)
        if cp and isinstance(cp[0][0], str) and "Unable to solve" in cp[0][0]:
            try:
                from .analysis import numeric_critical_points
                ncp = numeric_critical_points(sym, x_sym, args.xmin, args.xmax, samples=2000)
                for pt, typ in ncp:
                    # estimate y value
                    try:
                        yval = float(sp.lambdify(x_sym, sym, modules=['numpy'])(pt))
                    except Exception:
                        yval = 0.0
                    local_markers.append((pt, yval, 'red', 'o', typ))
            except Exception:
                pass
        else:
            if cp:
                for pt, typ in cp:
                    try:
                        yval = float(sp.lambdify(x_sym, sym, modules=['numpy'])(float(pt)))
                    except Exception:
                        yval = 0.0
                    local_markers.append((float(pt), yval, 'red', 'o', typ))

        # inflection (symbolic or numeric)
        if ip and isinstance(ip[0][0], str) and "Unable to solve" in ip[0][0]:
            try:
                from .analysis import numeric_inflection_points
                nips = numeric_inflection_points(sym, x_sym, args.xmin, args.xmax, samples=2000)
                for pt, typ in nips:
                    try:
                        yval = float(sp.lambdify(x_sym, sym, modules=['numpy'])(pt))
                    except Exception:
                        yval = 0.0
                    local_markers.append((pt, yval, 'green', 's', 'inflection'))
            except Exception:
                pass
        else:
            if ip:
                for pt, typ in ip:
                    try:
                        yval = float(sp.lambdify(x_sym, sym, modules=['numpy'])(float(pt)))
                    except Exception:
                        yval = 0.0
                    # if symbolic inflection detected, label it
                    label_text = 'inflection' if 'inflection' in str(typ) else typ
                    local_markers.append((float(pt), yval, 'green', 's', label_text))

        series.append((x_num, y_num, label, local_markers))

    print("\n" + "="*70)
    if getattr(args, '3d'):
        # 3D plotting for single expression
        x, y, label, markers = series[0]  # 修复：改为解包四个值
        # Create 2D grid for surface
        x_grid = np.linspace(args.xmin, args.xmax, 50)
        y_grid = np.linspace(args.xmin, args.xmax, 50)
        X, Y = np.meshgrid(x_grid, y_grid)
        try:
            sym = parse_expression(exprs[0], symbol_name="x")
            x_sym = sp.symbols('x')
            f_func = sp.lambdify(x_sym, sym, modules=["numpy", "mpmath"])
            Z = f_func(X)
            plot_3d(X, Y, Z, title=f"3D: {label}", savepath=args.save)
        except Exception as e:
            print(f"⚠ 3D 绘图失败: {e}")
            # fall back to annotated 2D
            x, y, lbl, markers = series[0]
            from .plotter import plot_2d_with_markers
            plot_2d_with_markers(x, y, markers=markers, title=lbl, savepath=args.save)
    elif len(series) == 1:
        x, y, lbl, markers = series[0]
        from .plotter import plot_2d_with_markers
        plot_2d_with_markers(x, y, markers=markers, title=str(lbl), savepath=args.save)
    else:
        # multiple series: call original plot_multiple_2d (no markers support per-series yet)
        # flatten series to (x,y,label)
        flat = [(s[0], s[1], s[2]) for s in series]
        plot_multiple_2d(flat, title="Comparison", savepath=args.save)


if __name__ == "__main__":
    main()