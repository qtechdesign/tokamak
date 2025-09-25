"""Stub SVG exporter for the Tokamak pit plan."""

from __future__ import annotations

from typing import Any

from ..domain import TokamakPitParams


def export_plan_svg(params: TokamakPitParams) -> bytes:
    svg = f"""<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {params.outer_radius*2} {params.outer_radius*2}'>
    <circle cx='{params.outer_radius}' cy='{params.outer_radius}' r='{params.outer_radius}' fill='none' stroke='black'/>
    <circle cx='{params.outer_radius}' cy='{params.outer_radius}' r='{params.inner_radius}' fill='none' stroke='black'/>
</svg>"""
    return svg.encode("utf-8")

