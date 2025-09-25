"""Shared constants for the Tokamak Pit domain models."""

from __future__ import annotations

MIN_SECTOR_COUNT = 6
MAX_SECTOR_COUNT = 48
# Upper bound for outer radius based on MVP acceptance criteria
MAX_RADIUS = 100.0


__all__ = [
    "MIN_SECTOR_COUNT",
    "MAX_SECTOR_COUNT",
    "MAX_RADIUS",
]

