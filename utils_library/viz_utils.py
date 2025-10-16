# viz_utils.py
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from typing import Any, Optional
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401


def _to_numpy(data: Any) -> np.ndarray:
    if isinstance(data, pd.DataFrame):
        return data.to_numpy()
    elif isinstance(data, pd.Series):
        return data.to_numpy()
    elif isinstance(data, (list, tuple)):
        return np.array([_safe_float(x) for x in data])
    elif isinstance(data, np.ndarray):
        return data
    else:
        raise TypeError(f"Unsupported data type: {type(data)}")


def _safe_float(x: Any) -> float:
    try:
        return float(x)
    except (ValueError, TypeError):
        return x


def _maybe_show():
    """Nur anzeigen, wenn ein interaktives Backend aktiv ist."""
    backend = matplotlib.get_backend().lower()
    if backend not in ["agg", "pdf", "svg", "ps"]:  # typische non-GUI Backends
        plt.show()


def auto_plot(
    data: Any,
    x: Optional[Any] = None,
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
    zlabel: str = "",
    multi: bool = True,
    force_2d: bool = False
):
    """
    Automatische Visualisierung von Daten (1D, 2D, 3D) mit Matplotlib.

    Plot-Regeln (wenn force_2d=False):
    - 1D Daten -> Line-Plot
    - 2D mit 2 Spalten -> Scatter (x vs y)
    - 2D mit 3 Spalten -> 3D-Scatter (x, y, z)
    - 2D mit >3 Spalten:
        - multi=True  -> jede Spalte als separate Linie
        - multi=False -> Autologik (nicht empfohlen für >3D)
    - 2D Array als Z-Matrix (Surface-Plot), falls x/y Grids angegeben sind

    Falls force_2d=True:
    - Egal welche Dimensionen -> alle Spalten als überlagerte Linienplots
      (n-dimensionale Daten werden "plattgedrückt" in 2D).
    """
    arr = _to_numpy(data)

    # Force alle Dimensionen auf 2D-Linienplots
    if force_2d:
        arr = np.atleast_2d(arr)
        plt.figure()
        for i in range(arr.shape[1] if arr.ndim > 1 else 1):
            if arr.ndim == 1:
                plt.plot(arr, label="col0")
            else:
                plt.plot(arr[:, i], label=f"col{i}")
        plt.legend()
        plt.title(title or "[Auto] Forced 2D Multi-Line")
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.tight_layout()
        _maybe_show()
        return

    # 1D -> Line Plot
    if arr.ndim == 1:
        plt.figure()
        if x is None:
            plt.plot(arr)
        else:
            plt.plot(_to_numpy(x), arr)
        plt.title(title or "[Auto] Line Plot")
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.tight_layout()
        _maybe_show()

    # 2D
    elif arr.ndim == 2:
        ncols = arr.shape[1]

        if ncols == 2 and not multi:
            plt.figure()
            plt.scatter(arr[:, 0], arr[:, 1], alpha=0.7)
            plt.title(title or "[Auto] Scatter Plot")
            plt.xlabel(xlabel or "x")
            plt.ylabel(ylabel or "y")
            plt.tight_layout()
            _maybe_show()

        elif ncols == 3 and not multi:
            fig = plt.figure()
            ax = fig.add_subplot(111, projection="3d")
            ax.scatter(arr[:, 0], arr[:, 1], arr[:, 2], alpha=0.7)
            ax.set_title(title or "[Auto] 3D Scatter")
            ax.set_xlabel(xlabel or "x")
            ax.set_ylabel(ylabel or "y")
            ax.set_zlabel(zlabel or "z")
            plt.tight_layout()
            _maybe_show()

        else:
            plt.figure()
            for i in range(ncols):
                plt.plot(arr[:, i], label=f"col{i}")
            plt.legend()
            plt.title(title or "[Auto] Multi-Line Plot")
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.tight_layout()
            _maybe_show()

    # 3D Surface (Matrixdaten)
    elif arr.ndim == 2 and x is not None:
        Z = arr
        X, Y = np.meshgrid(np.arange(Z.shape[0]), np.arange(Z.shape[1]))
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        ax.plot_surface(X, Y, Z, cmap="viridis", edgecolor="none")
        ax.set_title(title or "[Auto] 3D Surface")
        ax.set_xlabel(xlabel or "x")
        ax.set_ylabel(ylabel or "y")
        ax.set_zlabel(zlabel or "z")
        plt.tight_layout()
        _maybe_show()

    else:
        raise ValueError(f"Data shape {arr.shape} not supported")


import textwrap
from typing import Union, List

def pretty_print(
    text: str,
    header: str = None,
    subtext: Union[str, List[str], None] = None,
    width: int = 80,
    indent: int = 4,
    color: str = "none"
):
    """
    Formatiertes Printen mit optionalem Header und Subtext.

    Parameters
    ----------
    text : str
        Haupttext, wird immer ausgegeben.
    header : str, optional
        Überschrift, wird großgeschrieben und nicht eingerückt.
    subtext : str | list[str], optional
        Zusatzinformation(en). Falls Liste -> jede Zeile mit "-" beginnen.
    width : int
        Maximale Zeilenbreite (für automatisches Wrapping).
    indent : int
        Anzahl Spaces für Einrückung, wenn Header existiert.
    color : str
        Farbmodus: "none" (keine Farbe), oder eine von
        {"white", "cyan", "red", "green", "yellow", "blue"}.
        Betrifft die gesamte Ausgabe.
    """
    COLORS = {
        "none": "",
        "white": "\033[97m",
        "cyan": "\033[96m",
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
    }
    BOLD = "\033[1m"
    RESET = "\033[0m"

    color_code = COLORS.get(color.lower(), "")

    def cprint(msg, bold=False):
        if color == "none":
            print(msg)
        else:
            style = color_code + (BOLD if bold else "")
            print(f"{style}{msg}{RESET}")

    # Header
    if header:
        header_str = header.upper()
        cprint(header_str, bold=True)
        cprint("=" * len(header_str))

    # Main Text
    wrapped_text = textwrap.fill(
        text,
        width=width,
        subsequent_indent=" " * (indent if header else 0),
        initial_indent=" " * (indent if header else 0)
    )
    cprint(wrapped_text)

    # Subtext(e)
    if subtext:
        if isinstance(subtext, str):
            subtext = [subtext]
        for line in subtext:
            wrapped = textwrap.fill(
                f"- {line}",
                width=width,
                initial_indent=" " * (indent + 2),
                subsequent_indent=" " * (indent + 2)
            )
            cprint(wrapped)
