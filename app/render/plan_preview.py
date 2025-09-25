"""Matplotlib plan preview for the Tokamak pit."""

from __future__ import annotations

from typing import Tuple

import matplotlib.pyplot as plt
from matplotlib.axes import Axes

from ..domain import TokamakPitParams


def create_plan_figure(params: TokamakPitParams) -> plt.Figure:
    figure, axes = plt.subplots(subplot_kw={"aspect": "equal"})
    _draw_annulus(axes, params)
    axes.set_title("Tokamak Pit Plan")
    axes.set_xlabel("Meters")
    axes.set_ylabel("Meters")
    return figure


def _draw_annulus(axes: Axes, params: TokamakPitParams) -> None:
    outer = plt.Circle((0, 0), params.outer_radius, fill=False, color="black")
    inner = plt.Circle((0, 0), params.inner_radius, fill=False, color="black")
    axes.add_patch(outer)
    axes.add_patch(inner)

