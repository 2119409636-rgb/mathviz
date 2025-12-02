"""Plotting helpers: 2D and 3D plotting using matplotlib and plotly.
"""
from typing import Sequence, Optional
import numpy as np
import matplotlib.pyplot as plt
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
