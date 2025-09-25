"""Streamlit entry point for the Tokamak Pit Parametric Designer."""

from __future__ import annotations

import json
from typing import Dict

import streamlit as st

if __package__ is None or __package__ == "":
    import sys
    from pathlib import Path

    sys.path.append(str(Path(__file__).resolve().parent.parent))
    from app.domain import TokamakPitParams, presets
    from app.domain.validate import validate
    from app.render.plan_preview import create_plan_figure
else:
    from .domain import TokamakPitParams, presets
    from .domain.validate import validate
    from .render.plan_preview import create_plan_figure


def load_preset_options() -> Dict[str, TokamakPitParams]:
    return presets()


def render_controls(params: TokamakPitParams) -> TokamakPitParams:
    st.sidebar.header("Geometry")
    inner_radius = st.sidebar.number_input("Inner Radius (m)", min_value=0.1, value=params.inner_radius)
    outer_radius = st.sidebar.number_input("Outer Radius (m)", min_value=inner_radius + 0.1, value=params.outer_radius)
    pit_depth = st.sidebar.number_input("Pit Depth (m)", min_value=0.1, value=params.pit_depth)
    floor_thickness = st.sidebar.number_input("Floor Thickness (m)", min_value=0.01, value=params.floor_thickness)
    wall_thickness = st.sidebar.number_input("Wall Thickness (m)", min_value=0.01, value=params.wall_thickness)
    sector_count = st.sidebar.slider("Sector Count", min_value=6, max_value=48, value=params.sector_count)
    sector_joints_width = st.sidebar.number_input("Sector Joint Width (m)", min_value=0.01, value=params.sector_joints_width)
    cryostat_plinth_radius = st.sidebar.number_input("Plinth Radius (m)", min_value=inner_radius, value=params.cryostat_plinth_radius)
    cryostat_plinth_height = st.sidebar.number_input("Plinth Height (m)", min_value=0.0, value=params.cryostat_plinth_height)

    # TODO: add controls for duct rings, ports, stairs

    return TokamakPitParams(
        inner_radius=inner_radius,
        outer_radius=outer_radius,
        pit_depth=pit_depth,
        floor_thickness=floor_thickness,
        wall_thickness=wall_thickness,
        sector_count=sector_count,
        sector_joints_width=sector_joints_width,
        cryostat_plinth_radius=cryostat_plinth_radius,
        cryostat_plinth_height=cryostat_plinth_height,
        duct_rings=params.duct_rings,
        ports=params.ports,
        stairs=params.stairs,
    )


def main() -> None:
    st.set_page_config(page_title="Tokamak Pit Designer", layout="wide")
    st.title("Tokamak Pit Parametric Designer")

    preset_options = load_preset_options()
    preset_names = list(preset_options.keys())
    selected_preset = st.sidebar.selectbox("Preset", preset_names, index=preset_names.index("default"))
    params = preset_options[selected_preset]

    params = render_controls(params)
    validation_messages = validate(params)

    if validation_messages:
        with st.expander("Validation issues", expanded=True):
            for message in validation_messages:
                st.error(message)

    plan_tab, json_tab = st.tabs(["Plan Preview", "Parameters JSON"])

    with plan_tab:
        figure = create_plan_figure(params)
        st.pyplot(figure, use_container_width=True)

    with json_tab:
        st.code(json.dumps(params.to_dict(), indent=2))


if __name__ == "__main__":
    main()

