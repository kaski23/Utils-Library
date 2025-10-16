import unittest
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # kein GUI-Backend für Tests

import matplotlib.pyplot as plt
plt.show = lambda *args, **kwargs: None  # plt.show neutralisieren

from viz_utils import auto_plot, pretty_print


class TestVizUtils(unittest.TestCase):

    # -------- auto_plot Tests --------
    def test_auto_plot_1d_list(self):
        auto_plot([1, 2, 3, "4.5"], title="1D List")

    def test_auto_plot_2d_scatter(self):
        arr = np.random.rand(10, 2)
        auto_plot(arr, multi=False, title="2D Scatter")

    def test_auto_plot_3d_scatter(self):
        arr = np.random.rand(10, 3)
        auto_plot(arr, multi=False, title="3D Scatter")

    def test_auto_plot_multi_line_dataframe(self):
        df = pd.DataFrame(np.random.rand(5, 4), columns=list("abcd"))
        auto_plot(df, title="Multi-Line")

    def test_auto_plot_force_2d(self):
        arr = np.random.rand(5, 3)
        auto_plot(arr, force_2d=True, title="Forced 2D")

    def test_auto_plot_surface(self):
        x = np.linspace(-5, 5, 20)
        y = np.linspace(-5, 5, 20)
        X, Y = np.meshgrid(x, y)
        Z = np.sin(np.sqrt(X**2 + Y**2))
        auto_plot(Z, title="Surface", xlabel="x", ylabel="y", zlabel="z")

    # -------- pretty_print Tests --------
    def test_pretty_print_simple(self):
        # Nur Text, ohne Header/Subtext
        pretty_print("Hello World", color="none")

    def test_pretty_print_with_header(self):
        pretty_print("Main Text", header="Info", color="cyan")

    def test_pretty_print_with_subtext_string(self):
        pretty_print("Main Text", header="Details", subtext="Subtext-Zeile", color="green")

    def test_pretty_print_with_subtext_list(self):
        pretty_print(
            "Main Text",
            header="List",
            subtext=["Ein Punkt", "Noch ein Punkt", "Lange Zeile die wrapped"],
            color="yellow"
        )


if __name__ == "__main__":
    unittest.main()
