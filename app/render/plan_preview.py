"""Plan view renderer using Matplotlib patches.

The figure aims to provide a quick preview of the Tokamak pit geometry with
layers for walls, sector joints, duct rings, ports, stairs, and the plinth.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib import patches
from matplotlib.axes import Axes

from ..domain import TokamakPitParams
from ..domain.geometry import make_wedge, sector_angles, tangential_width_to_arc_deg


WALL_COLOR = "#264653"
SECTOR_COLOR = "#f4a261"
DUCT_COLOR = "#2a9d8f"
PORT_COLOR = "#e76f51"
STAIR_COLOR = "#8ab17d"
PLINTH_EDGE = "#1d3557"
PLINTH_FILL = "#a8dadc"


def create_plan_figure(params: TokamakPitParams) -> plt.Figure:
    """Return a Matplotlib figure showing a plan of the Tokamak pit."""

    figure, axes = plt.subplots(figsize=(6, 6))
    axes.set_aspect("equal", adjustable="box")

    _draw_walls(axes, params)
    _draw_sector_joints(axes, params)
    _draw_duct_rings(axes, params)
    _draw_ports(axes, params)
    _draw_stairs(axes, params)
    _draw_plinth(axes, params)

    limit = params.outer_radius + params.wall_thickness * 1.2
    axes.set_xlim(-limit, limit)
    axes.set_ylim(-limit, limit)
    axes.set_xlabel("Meters")
    axes.set_ylabel("Meters")
    axes.set_title("Tokamak Pit Plan")
    axes.grid(alpha=0.15)

    return figure


def _draw_walls(axes: Axes, params: TokamakPitParams) -> None:
    outer_circle = patches.Circle((0, 0), params.outer_radius, fill=False, lw=2, color=WALL_COLOR)
    inner_circle = patches.Circle((0, 0), params.inner_radius, fill=False, lw=2, color=WALL_COLOR)
    axes.add_patch(outer_circle)
    axes.add_patch(inner_circle)


def _draw_sector_joints(axes: Axes, params: TokamakPitParams) -> None:
    if params.sector_joints_width <= 0 or params.sector_count <= 0:
        return
    joint_span = tangential_width_to_arc_deg(params.sector_joints_width, params.outer_radius)
    radial_width = params.outer_radius - params.inner_radius
    for angle in sector_angles(params.sector_count):
        theta1 = angle - joint_span / 2
        theta2 = angle + joint_span / 2
        sector_patch = patches.Wedge(
            (0, 0),
            r=params.outer_radius,
            theta1=theta1,
            theta2=theta2,
            width=radial_width,
            facecolor=SECTOR_COLOR,
            edgecolor="none",
            alpha=0.35,
        )
        axes.add_patch(sector_patch)


def _draw_duct_rings(axes: Axes, params: TokamakPitParams) -> None:
    for ring in params.duct_rings:
        inner = ring.radius - ring.width / 2
        outer = ring.radius + ring.width / 2
        if inner <= 0:
            continue
        filled = patches.Circle((0, 0), outer, color=DUCT_COLOR, alpha=0.08)
        axes.add_patch(filled)
        axes.add_patch(patches.Circle((0, 0), outer, fill=False, ls="--", color=DUCT_COLOR, lw=1))
        axes.add_patch(patches.Circle((0, 0), inner, fill=False, ls="--", color=DUCT_COLOR, lw=1))


def _draw_ports(axes: Axes, params: TokamakPitParams) -> None:
    for port in params.ports:
        radius_ref = max(port.start_radius, params.inner_radius + 1e-6)
        wedge = make_wedge(
            center_deg=port.angle_deg,
            width=port.width,
            radius=radius_ref,
            start_radius=port.start_radius,
            end_radius=port.end_radius,
        )
        axes.add_patch(
            patches.Wedge(
                (0, 0),
                r=wedge.end_radius,
                theta1=wedge.start_angle_deg,
                theta2=wedge.end_angle_deg,
                width=wedge.end_radius - wedge.start_radius,
                facecolor=PORT_COLOR,
                edgecolor="none",
                alpha=0.45,
            )
        )


def _draw_stairs(axes: Axes, params: TokamakPitParams) -> None:
    for stair in params.stairs:
        radius_ref = max(stair.start_radius, params.inner_radius + 1e-6)
        wedge = make_wedge(
            center_deg=stair.angle_deg,
            width=stair.run_width,
            radius=radius_ref,
            start_radius=stair.start_radius,
            end_radius=stair.end_radius,
        )
        axes.add_patch(
            patches.Wedge(
                (0, 0),
                r=wedge.end_radius,
                theta1=wedge.start_angle_deg,
                theta2=wedge.end_angle_deg,
                width=wedge.end_radius - wedge.start_radius,
                facecolor=STAIR_COLOR,
                edgecolor="none",
                alpha=0.45,
            )
        )


def _draw_plinth(axes: Axes, params: TokamakPitParams) -> None:
    if params.cryostat_plinth_radius <= 0:
        return
    plinth = patches.Circle(
        (0, 0),
        params.cryostat_plinth_radius,
        facecolor=PLINTH_FILL,
        edgecolor=PLINTH_EDGE,
        alpha=0.4,
        lw=1.5,
    )
    axes.add_patch(plinth)

