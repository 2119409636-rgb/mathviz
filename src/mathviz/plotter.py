"""Plotting helpers: 2D and 3D plotting using matplotlib and plotly.
"""
from typing import Sequence, Optional, Callable
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def plot_2d(x: np.ndarray, y: np.ndarray, title: Optional[str] = None, savepath: Optional[str] = None):
    """Simple 2D plot using matplotlib."""
    plt.figure(figsize=(8, 4.5))
    plt.plot(x, y, lw=2)
    plt.xlabel('x')
    plt.ylabel('f(x)')
    if title:
        plt.title(title)
    plt.grid(True)
    if savepath:
        plt.savefig(savepath, dpi=150)
    else:
        plt.show()


def plot_multiple_2d(series: Sequence[tuple], title: Optional[str] = None, savepath: Optional[str] = None):
    """Plot multiple (x, y, label) series.

    series: sequence of (x, y, label)
    """
    plt.figure(figsize=(8, 4.5))
    for x, y, label in series:
        plt.plot(x, y, label=label)
    plt.xlabel('x')
    plt.ylabel('f(x)')
    if title:
        plt.title(title)
    plt.grid(True)
    plt.legend()
    if savepath:
        plt.savefig(savepath, dpi=150)
    else:
        plt.show()


def plot_3d(x: np.ndarray, y: np.ndarray, z: np.ndarray, title: Optional[str] = None, savepath: Optional[str] = None):
    """Interactive 3D scatter/mesh using Plotly."""
    fig = go.Figure(data=[go.Surface(x=x, y=y, z=z)])
    fig.update_layout(title=title or '3D plot', autosize=True)
    if savepath:
        fig.write_image(savepath)
    else:
        fig.show()


def complex_plot(f: Callable, xmin: float, xmax: float, ymin: float, ymax: float, 
                 resolution: int = 400, mode: str = 'magnitude', 
                 title: Optional[str] = None, savepath: Optional[str] = None):
    """Plot a complex-valued function f: ℂ → ℂ using colormapping.
    
    Args:
        f: Callable that takes complex input and returns complex output
        xmin, xmax, ymin, ymax: Real and imaginary axis bounds
        resolution: Number of points per axis
        mode: 'magnitude' (default) or 'phase' (argument)
        title: Plot title
        savepath: If provided, save image instead of showing
    """
    # Create grid in complex plane
    x = np.linspace(xmin, xmax, resolution)
    y = np.linspace(ymin, ymax, resolution)
    X, Y = np.meshgrid(x, y)
    Z_complex = X + 1j * Y
    
    # Evaluate function
    try:
        W = f(Z_complex)
    except Exception as e:
        print(f"Error evaluating complex function: {e}")
        return
    
    # Compute magnitude or phase
    if mode == 'magnitude':
        Z = np.abs(W)
        colorbar_title = '|f(z)|'
    elif mode == 'phase':
        Z = np.angle(W)
        colorbar_title = 'arg(f(z))'
    else:
        Z = np.abs(W)
        colorbar_title = '|f(z)|'
    
    plt.figure(figsize=(10, 8))
    im = plt.contourf(X, Y, Z, levels=40, cmap='hsv' if mode == 'phase' else 'viridis')
    plt.colorbar(im, label=colorbar_title)
    plt.xlabel('Re(z)')
    plt.ylabel('Im(z)')
    plt.title(title or f'Complex function ({mode})')
    if savepath:
        plt.savefig(savepath, dpi=150, bbox_inches='tight')
    else:
        plt.show()


def implicit_plot(f: Callable, xmin: float, xmax: float, ymin: float, ymax: float,
                  resolution: int = 400, title: Optional[str] = None, 
                  savepath: Optional[str] = None):
    """Plot implicitly defined function f(x, y) = 0 using contour lines.
    
    Args:
        f: Callable that takes (x, y) arrays and returns f(x,y)
        xmin, xmax, ymin, ymax: Domain bounds
        resolution: Grid resolution
        title: Plot title
        savepath: If provided, save image instead of showing
    """
    x = np.linspace(xmin, xmax, resolution)
    y = np.linspace(ymin, ymax, resolution)
    X, Y = np.meshgrid(x, y)
    
    try:
        Z = f(X, Y)
    except Exception as e:
        print(f"Error evaluating implicit function: {e}")
        return
    
    plt.figure(figsize=(10, 8))
    # Plot the zero level set
    contour = plt.contour(X, Y, Z, levels=[0], colors='blue', linewidths=2)
    plt.clabel(contour, inline=True, fontsize=8)
    # Background fill
    plt.contourf(X, Y, Z, levels=20, cmap='coolwarm', alpha=0.6)
    plt.colorbar(label='f(x, y)')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(title or 'Implicit curve: f(x, y) = 0')
    plt.grid(True, alpha=0.3)
    if savepath:
        plt.savefig(savepath, dpi=150, bbox_inches='tight')
    else:
        plt.show()


def parametric_plot(x_func: Callable, y_func: Callable, t_min: float, t_max: float,
                    z_func: Optional[Callable] = None, n_points: int = 1000,
                    title: Optional[str] = None, savepath: Optional[str] = None):
    """Plot a parametric curve (x(t), y(t)) or (x(t), y(t), z(t)).
    
    Args:
        x_func, y_func: Callables parameterized by t
        t_min, t_max: Parameter range
        z_func: Optional; if provided, creates 3D plot
        n_points: Number of points to sample
        title: Plot title
        savepath: If provided, save image instead of showing
    """
    t = np.linspace(t_min, t_max, n_points)
    
    try:
        xs = x_func(t)
        ys = y_func(t)
    except Exception as e:
        print(f"Error evaluating parametric functions: {e}")
        return
    
    if z_func is None:
        # 2D parametric plot
        plt.figure(figsize=(10, 7))
        plt.plot(xs, ys, lw=2)
        plt.xlabel('x(t)')
        plt.ylabel('y(t)')
        plt.title(title or 'Parametric curve')
        plt.grid(True, alpha=0.3)
        if savepath:
            plt.savefig(savepath, dpi=150, bbox_inches='tight')
        else:
            plt.show()
    else:
        # 3D parametric plot
        try:
            zs = z_func(t)
        except Exception as e:
            print(f"Error evaluating z function: {e}")
            return
        
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot(xs, ys, zs, lw=2)
        ax.set_xlabel('x(t)')
        ax.set_ylabel('y(t)')
        ax.set_zlabel('z(t)')
        ax.set_title(title or '3D Parametric curve')
        if savepath:
            plt.savefig(savepath, dpi=150, bbox_inches='tight')
        else:
            plt.show()
