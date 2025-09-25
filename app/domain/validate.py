"""Validation routines for Tokamak pit parameters.

The functions here return human-readable messages describing issues or
warnings without raising; the caller decides how to surface them.
"""

from __future__ import annotations

from typing import List

from .constants import MAX_RADIUS, MAX_SECTOR_COUNT, MIN_SECTOR_COUNT
from .params import DuctRing, Port, Stair, TokamakPitParams


def validate(params: TokamakPitParams) -> List[str]:
    """Return a list of validation error messages for the given parameters."""

    errors: List[str] = []

    errors.extend(_validate_geometry_bounds(params))
    errors.extend(_validate_sectoring(params))
    errors.extend(_validate_duct_rings(params))
    errors.extend(_validate_ports(params))
    errors.extend(_validate_stairs(params))

    return errors


def _validate_geometry_bounds(params: TokamakPitParams) -> List[str]:
    errors: List[str] = []
    if params.inner_radius <= 0:
        errors.append("inner_radius must be greater than zero")
    if params.outer_radius <= params.inner_radius + params.wall_thickness:
        errors.append("outer_radius must exceed inner_radius + wall_thickness")
    if params.pit_depth <= 0:
        errors.append("pit_depth must be greater than zero")
    if params.outer_radius > MAX_RADIUS:
        errors.append(f"outer_radius must be <= {MAX_RADIUS} m for MVP")
    return errors


def _validate_sectoring(params: TokamakPitParams) -> List[str]:
    errors: List[str] = []
    if params.sector_count < MIN_SECTOR_COUNT or params.sector_count > MAX_SECTOR_COUNT:
        errors.append(
            f"sector_count must be in the range [{MIN_SECTOR_COUNT}, {MAX_SECTOR_COUNT}]"
        )
    if params.sector_joints_width <= 0:
        errors.append("sector_joints_width must be positive")
    return errors


def _validate_duct_rings(params: TokamakPitParams) -> List[str]:
    errors: List[str] = []
    for index, ring in enumerate(params.duct_rings):
        errors.extend(_validate_duct_ring(ring, params, index))
    return errors


def _validate_duct_ring(ring: DuctRing, params: TokamakPitParams, index: int) -> List[str]:
    errors: List[str] = []
    inner_limit = params.inner_radius
    outer_limit = params.outer_radius - params.wall_thickness
    if (ring.radius - ring.width / 2) < inner_limit:
        errors.append(f"duct_rings[{index}] inner edge encroaches inner radius")
    if (ring.radius + ring.width / 2) > outer_limit:
        errors.append(f"duct_rings[{index}] outer edge encroaches wall thickness")
    if ring.count < 1:
        errors.append(f"duct_rings[{index}] count must be at least 1")
    if ring.duct_width <= 0:
        errors.append(f"duct_rings[{index}] duct_width must be positive")
    return errors


def _validate_ports(params: TokamakPitParams) -> List[str]:
    errors: List[str] = []
    for index, port in enumerate(params.ports):
        errors.extend(_validate_wedge(port, params, f"ports[{index}]"))
    return errors


def _validate_stairs(params: TokamakPitParams) -> List[str]:
    errors: List[str] = []
    for index, stair in enumerate(params.stairs):
        errors.extend(_validate_wedge(stair, params, f"stairs[{index}]"))
    return errors


def _validate_wedge(
    wedge: Port | Stair,
    params: TokamakPitParams,
    label: str,
) -> List[str]:
    errors: List[str] = []
    run_width = wedge.width if isinstance(wedge, Port) else wedge.run_width
    if wedge.start_radius < params.inner_radius:
        errors.append(f"{label} start_radius must be >= inner_radius")
    if wedge.end_radius > params.outer_radius:
        errors.append(f"{label} end_radius must be <= outer_radius")
    if run_width <= 0:
        width_name = "width" if isinstance(wedge, Port) else "run_width"
        errors.append(f"{label} {width_name} must be positive")
    return errors

