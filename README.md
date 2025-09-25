# Tokamak Pit Parametric Designer

This project is an interactive Streamlit application that lets designer teams explore
Tokamak pit layouts using a parametric model. The layout is described in the
product rules and rendered instantly with a plan preview. JSON parameter sets
and SVG exports will be available as the project evolves.

## Features (MVP)

- Plan view with adjustable inner/outer radii, sectoring, rings, ports, and stairs.
- Real-time validation for geometric constraints (wall clearance, wedge bounds).
- Streamlit UI for parameter sliders, preset selection, and JSON viewing.
- Matplotlib-based plan preview with visual layering for key elements.

## Getting Started

### First-time Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt  # optional once dependencies exported
pip install streamlit numpy matplotlib
```

### Run the App

```powershell
.\.venv\Scripts\Activate.ps1
streamlit run app/main.py
```

The development server will provide a local URL, typically
`http://localhost:8501`. Adjust parameters via the sidebar and watch the plan
preview update immediately.

## Project Layout

```text
app/
  main.py               # Streamlit entry point
  domain/               # Pure data models, validation, geometry helpers
  render/               # Matplotlib plan preview, SVG export
  presets/              # Parameter presets (JSON)
  tests/                # Unit tests (coming)
```

## Next Steps

- Expand plan preview with richer detail and interactive layers.
- Implement SVG and JSON export workflows.
- Add unit tests and golden image comparisons.
- Extend UI for editing duct rings, ports, and stairs dynamically.

## License

TBD.

