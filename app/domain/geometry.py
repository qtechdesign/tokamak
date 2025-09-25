"""Geometry helpers for the Tokamak pit domain."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List


def tangential_width_to_arc_deg(width: float, radius: float) -> float:
    """Convert a tangential width at a given radius to an angle in degrees.

    Formula: theta = width / radius * 180 / pi
    """

    if radius <= 0:
        raise ValueError("radius must be positive")
    return math.degrees(width / radius)


def angle_range(center_deg: float, span_deg: float) -> tuple[float, float]:
    half_span = span_deg / 2
    return center_deg - half_span, center_deg + half_span


def sector_angles(sector_count: int) -> List[float]:
    step = 360.0 / sector_count
    return [step * i for i in range(sector_count)]


@dataclass(frozen=True)
class Wedge:
    start_radius: float
    end_radius: float
    start_angle_deg: float
    end_angle_deg: float


def make_wedge(center_deg: float, width: float, radius: float, start_radius: float, end_radius: float) -> Wedge:
    span = tangential_width_to_arc_deg(width, radius)
    start_angle, end_angle = angle_range(center_deg, span)
    return Wedge(start_radius=start_radius, end_radius=end_radius, start_angle_deg=start_angle, end_angle_deg=end_angle)

