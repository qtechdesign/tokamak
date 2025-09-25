"""Dataclasses representing the Tokamak pit parameter set.

The Canonical Parameter Set described in `Tokamak Pit Parametric Designer — RULES` is
implemented here as immutable dataclasses with helpers for (de)serialisation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, Tuple


@dataclass(frozen=True)
class DuctRing:
    """Circular duct ring set running around the pit annulus."""

    radius: float
    width: float
    elevation: float
    count: int
    duct_width: float


@dataclass(frozen=True)
class Port:
    """Tangential port wedge connecting inner and outer radii of the pit."""

    angle_deg: float
    width: float
    start_radius: float
    end_radius: float


@dataclass(frozen=True)
class Stair:
    """Stair wedge defined by its tangential run and radial start/end."""

    angle_deg: float
    run_width: float
    start_radius: float
    end_radius: float


@dataclass(frozen=True)
class TokamakPitParams:
    """Complete parametric definition of the Tokamak pit layout."""

    inner_radius: float
    outer_radius: float
    pit_depth: float
    floor_thickness: float
    wall_thickness: float
    sector_count: int
    sector_joints_width: float
    cryostat_plinth_radius: float
    cryostat_plinth_height: float
    duct_rings: Tuple[DuctRing, ...] = field(default_factory=tuple)
    ports: Tuple[Port, ...] = field(default_factory=tuple)
    stairs: Tuple[Stair, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        object.__setattr__(self, "duct_rings", tuple(self.duct_rings))
        object.__setattr__(self, "ports", tuple(self.ports))
        object.__setattr__(self, "stairs", tuple(self.stairs))

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass graph into JSON-serialisable primitives."""

        return {
            "inner_radius": self.inner_radius,
            "outer_radius": self.outer_radius,
            "pit_depth": self.pit_depth,
            "floor_thickness": self.floor_thickness,
            "wall_thickness": self.wall_thickness,
            "sector_count": self.sector_count,
            "sector_joints_width": self.sector_joints_width,
            "cryostat_plinth_radius": self.cryostat_plinth_radius,
            "cryostat_plinth_height": self.cryostat_plinth_height,
            "duct_rings": [asdict_duct_ring(ring) for ring in self.duct_rings],
            "ports": [asdict_port(port) for port in self.ports],
            "stairs": [asdict_stair(stair) for stair in self.stairs],
        }


def asdict_duct_ring(ring: DuctRing) -> Dict[str, Any]:
    """Dictionary representation of a `DuctRing`."""

    return {
        "radius": ring.radius,
        "width": ring.width,
        "elevation": ring.elevation,
        "count": ring.count,
        "duct_width": ring.duct_width,
    }


def asdict_port(port: Port) -> Dict[str, Any]:
    """Dictionary representation of a `Port`."""

    return {
        "angle_deg": port.angle_deg,
        "width": port.width,
        "start_radius": port.start_radius,
        "end_radius": port.end_radius,
    }


def asdict_stair(stair: Stair) -> Dict[str, Any]:
    """Dictionary representation of a `Stair`."""

    return {
        "angle_deg": stair.angle_deg,
        "run_width": stair.run_width,
        "start_radius": stair.start_radius,
        "end_radius": stair.end_radius,
    }


def from_dict(payload: Dict[str, Any]) -> TokamakPitParams:
    """Create `TokamakPitParams` from a parsed JSON-like dictionary."""

    duct_rings = [DuctRing(**item) for item in payload.get("duct_rings", [])]
    ports = [Port(**item) for item in payload.get("ports", [])]
    stairs = [Stair(**item) for item in payload.get("stairs", [])]
    return TokamakPitParams(
        inner_radius=float(payload["inner_radius"]),
        outer_radius=float(payload["outer_radius"]),
        pit_depth=float(payload["pit_depth"]),
        floor_thickness=float(payload["floor_thickness"]),
        wall_thickness=float(payload["wall_thickness"]),
        sector_count=int(payload["sector_count"]),
        sector_joints_width=float(payload["sector_joints_width"]),
        cryostat_plinth_radius=float(payload["cryostat_plinth_radius"]),
        cryostat_plinth_height=float(payload["cryostat_plinth_height"]),
        duct_rings=duct_rings,
        ports=ports,
        stairs=stairs,
    )


def default_params() -> TokamakPitParams:
    """Return the canonical default parameters outlined in the rules document."""

    return TokamakPitParams(
        inner_radius=8.0,
        outer_radius=16.0,
        pit_depth=18.0,
        floor_thickness=1.0,
        wall_thickness=1.5,
        sector_count=16,
        sector_joints_width=0.25,
        cryostat_plinth_radius=9.5,
        cryostat_plinth_height=2.0,
        duct_rings=[
            DuctRing(radius=11.0, width=1.0, elevation=2.0, count=16, duct_width=0.8),
            DuctRing(radius=13.0, width=1.0, elevation=6.0, count=32, duct_width=0.6),
        ],
        ports=[
            Port(angle_deg=0.0, width=2.0, start_radius=8.5, end_radius=16.0),
            Port(angle_deg=120.0, width=1.6, start_radius=9.0, end_radius=16.0),
        ],
        stairs=[
            Stair(angle_deg=220.0, run_width=2.4, start_radius=9.0, end_radius=15.5),
        ],
    )


def presets() -> Dict[str, TokamakPitParams]:
    """Return built-in preset configurations referenced in the rules."""

    # TODO: fill in with additional presets as JSON files are added.
    default = default_params()
    compact = TokamakPitParams(
        inner_radius=7.0,
        outer_radius=14.0,
        pit_depth=18.0,
        floor_thickness=1.0,
        wall_thickness=1.5,
        sector_count=12,
        sector_joints_width=0.25,
        cryostat_plinth_radius=9.5,
        cryostat_plinth_height=2.0,
        duct_rings=list(default.duct_rings),
        ports=list(default.ports),
        stairs=list(default.stairs),
    )
    wide = TokamakPitParams(
        inner_radius=10.0,
        outer_radius=22.0,
        pit_depth=18.0,
        floor_thickness=1.0,
        wall_thickness=1.5,
        sector_count=18,
        sector_joints_width=0.25,
        cryostat_plinth_radius=9.5,
        cryostat_plinth_height=2.0,
        duct_rings=list(default.duct_rings),
        ports=list(default.ports),
        stairs=list(default.stairs),
    )
    deep = TokamakPitParams(
        inner_radius=8.0,
        outer_radius=16.0,
        pit_depth=28.0,
        floor_thickness=1.0,
        wall_thickness=1.5,
        sector_count=16,
        sector_joints_width=0.25,
        cryostat_plinth_radius=9.5,
        cryostat_plinth_height=2.0,
        duct_rings=[
            DuctRing(radius=11.0, width=1.0, elevation=3.0, count=16, duct_width=0.8),
            DuctRing(radius=13.0, width=1.0, elevation=10.0, count=32, duct_width=0.6),
        ],
        ports=list(default.ports),
        stairs=list(default.stairs),
    )
    return {
        "default": default,
        "compact": compact,
        "wide": wide,
        "deep": deep,
    }

