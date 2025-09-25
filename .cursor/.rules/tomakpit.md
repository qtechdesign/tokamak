Tokamak Pit Parametric Designer — RULES.md
1) Product Brief

Goal: A parametric app that generates a tokamak pit layout (plan, section, and lightweight 3D), lets users tune parameters live, and exports plan (SVG) + parameter sets (JSON).

Audience: Concept/coordination engineers and students. Quick iteration; not a structural tool.

Platforms: Start with Streamlit for speed. Optional FastAPI backend later.

2) Scope (MVP → v1.0)

MVP

Plan view (annulus inner/outer walls, sector joints).

Configurable: inner/outer radii, depth, wall/floor thickness, sector count, sector joint width, cryostat plinth radius/height.

Components: duct rings, access ports, stair wedges.

Live validation (geometric overlaps, limits).

Export SVG (plan), JSON (params).

Lightweight 3D preview (mplot3d) just for spatial sense.

Deterministic seeds for reproducibility.

v1.0+

Section view generator (elevations with floor levels).

DXF export, GLB preview, snapping/dimensioning helpers.

Constraints solver (e.g., auto-spacing ducts/ports within bounds).

Presets library; import/export parameter sets.

Unit tests + baseline images for regression.

3) Non-Goals (now)

FEM/structural analysis, rebar, cost/QS, clash with foreign models.

Photoreal renders. CAD-grade solid modeling.

4) Core Domain Concepts

Pit annulus: inner_radius ↔ outer_radius
Sectoring: sector_count, sector_joints_width
Elements:

DuctRing: radius, width, elevation, count, duct_width

Port: angle_deg, width (tangential), start_radius, end_radius

Stair: angle_deg, run_width (tangential), start_radius, end_radius

Plinth: cryostat_plinth_radius, cryostat_plinth_height

Canonical Parameter Set (JSON Schema)
{
  "inner_radius": 8.0,
  "outer_radius": 16.0,
  "pit_depth": 18.0,
  "floor_thickness": 1.0,
  "wall_thickness": 1.5,
  "sector_count": 16,
  "sector_joints_width": 0.25,
  "cryostat_plinth_radius": 9.5,
  "cryostat_plinth_height": 2.0,
  "duct_rings": [
    {"radius": 11.0, "width": 1.0, "elevation": 2.0, "count": 16, "duct_width": 0.8},
    {"radius": 13.0, "width": 1.0, "elevation": 6.0, "count": 32, "duct_width": 0.6}
  ],
  "ports": [
    {"angle_deg": 0.0, "width": 2.0, "start_radius": 8.5, "end_radius": 16.0},
    {"angle_deg": 120.0, "width": 1.6, "start_radius": 9.0, "end_radius": 16.0}
  ],
  "stairs": [
    {"angle_deg": 220.0, "run_width": 2.4, "start_radius": 9.0, "end_radius": 15.5}
  ]
}

Derived/Geometry Notes

Arc angle from tangential width at radius R:
theta_deg = (width / R) * 180 / π

Port wedge: between radii [start_radius, end_radius], centered at angle_deg, span theta_deg.

Sector joint wedges: dtheta = 360 / sector_count, each joint uses arc for sector_joints_width at outer_radius.

Validity checks:

outer_radius > inner_radius + wall_thickness

pit_depth > 0, inner_radius > 0

Rings fit within annulus; non-overlapping expectations are advisory, not enforced.

5) UX & Interaction

Left: parameter controls (+ collapsible advanced).

Right: tabs → Plan (SVG preview), 3D, Section (stub for MVP), JSON.

Actions: Export SVG/JSON; Load JSON; Presets dropdown (Default, Compact, Wide, Deep, Demo-DensePorts).

Hints: Inline warnings for invalid/edge parameters; badge shows # of warnings.

6) Architecture

UI Layer: Streamlit components (sliders/number inputs/file upload/buttons/tabs).

Domain Layer: Pure functions for geometry + validation.

Renderers:

Plan → Matplotlib for preview + separate SVG exporter (write-to-bytes)

3D → Matplotlib mplot3d with coarse triangle mesh

I/O: JSON read/write; SVG bytes download.

Module layout

/app
  main.py                # Streamlit entry
  domain/
    params.py            # dataclasses, defaults, schema helpers
    validate.py          # validation & warnings
    geometry.py          # wedge/arc math, sectoring, mesh
  render/
    plan_preview.py      # matplotlib plan preview
    svg_export.py        # plan SVG writer
    mesh3d.py            # coarse 3D annulus mesh
  presets/
    default.json
    compact.json
    wide.json
  tests/
    test_validate.py
    test_geometry.py
    test_svg_export.py
  assets/
    icons/
  README.md

7) Acceptance Criteria (MVP)

Adjusting any parameter updates the preview within ~500ms.

SVG export opens correctly in Illustrator/Inkscape; circles/paths are absolute (no transforms).

JSON export/import round-trips identically (ignoring ordering).

Validation fires on mis-sized rings/ports/stairs with clear messages.

3D preview renders without errors for sector_count in [6..48] and radii up to 100 m.

8) Engineering Rules (Cursor)

Keep domain pure, deterministic, side-effect free.

No magic numbers: centralize in constants.py or top of modules.

Prefer dataclasses for params; never rely on dicts in domain functions.

Type hints everywhere; mypy --strict clean for domain.

Unit tests for validation + geometry math; avoid testing Streamlit.

Functions < 60 lines. If longer, refactor.

Docstrings with formulas for any geometric conversion.

9) Mind Map (Mermaid)
mindmap
  root((Tokamak Pit Designer))
    Goals
      MVP visuals
      Parametric edits
      SVG/JSON export
    Domain
      Pit
        inner_radius
        outer_radius
        depth
        wall_thickness
        floor_thickness
      Sectoring
        sector_count
        joint_width
      Elements
        DuctRings
        Ports
        Stairs
        Plinth
    Geometry
      ArcFromWidth
      SectorWedges
      CollisionChecks
      Coarse3DMesh
    UI
      Sliders/Inputs
      Tabs: Plan/3D/Section/JSON
      Presets
      Warnings
    Renderers
      PlanPreview(Matplotlib)
      SVGExport(Paths)
      3DPreview(mplot3d)
    I/O
      Import/Export JSON
      Download SVG
    Roadmap
      SectionViews
      DXF/GLB
      ConstraintsSolver
      PresetLibrary

10) Validation Rules (detailed)

Geometry bounds

inner_radius > 0

outer_radius > inner_radius + wall_thickness

pit_depth > 0

DuctRing

(radius - width/2) >= inner_radius

(radius + width/2) <= (outer_radius - wall_thickness)

count >= 1, duct_width > 0

Port/Stair

start_radius >= inner_radius

end_radius <= outer_radius

width/run_width > 0

Advisories

cryostat_plinth_radius ideally in (inner_radius, outer_radius - wall_thickness]

11) Presets (initial)

Default: values from schema above.

Compact: inner=7, outer=14, sectors=12.

Wide: inner=10, outer=22, sectors=18.

Deep: depth=28, two ring levels at elevations 3 & 10.

Demo-DensePorts: 6 ports at 60° intervals, width 1.6–2.4 m.

12) Tasks (MVP Sprint)

Datamodel: dataclasses + defaults + (de)serialize helpers.

Validation: rule set + unit tests.

Geometry helpers: width↔arc conversion, sector positions.

Plan preview: matplotlib layers (walls, joints, ports, stairs, plinth).

SVG exporter: absolute paths, mm/px scaling, metadata.

3D preview: annulus mesh + basic lighting.

Streamlit UI: controls, tabs, file I/O, preset dropdown.

QA: test large radii, many sectors, edge cases, exports open in Inkscape/AI.

13) Stretch Items

Section view generator with level tags and elevation callouts.

DXF via ezdxf and GLB via trimesh.

Solver helpers (e.g., auto place n ports without overlap).

Screenshot/export PNG of plan preview.

14) Example User Stories

As a designer, I can set inner/outer radii and see the plan update instantly.

As an engineer, I can export an SVG and dimension it in Illustrator.

As a reviewer, I can load a shared JSON to reproduce the same layout.

As a coordinator, I get warnings if duct rings encroach walls.

15) Testing Plan

Unit: validation math; arc-angle conversion; sector angle distribution.

Golden files: SVG byte hashes for canonical presets (allow minor tolerance for float formatting).

Property tests: random valid params must not throw; invalid params must produce ≥1 warning.

Performance: 100 UI parameter changes in under 1 min on mid-range laptop.

16) Dependencies & Versions

Python 3.9+

streamlit, numpy, matplotlib

Optional: pydantic (schema/validation), trimesh (future 3D), ezdxf (future DXF)

17) CLI (optional later)
tokapit export --params params.json --out plan.svg
tokapit validate --params params.json
tokapit preset --list

18) Coding Prompts (Cursor)

Domain function template:

“Create a pure function tangential_width_to_arc_deg(width, radius) with docstring and tests.”

Renderer prompt:

“Render plan with layers: walls → joints → ports → stairs → plinth; return matplotlib Figure; no I/O.”

Exporter prompt:

“Write export_plan_svg(params) -> bytes producing absolute path commands; unit test file size > 2 KB for default preset.”