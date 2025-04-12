# Icosphere Viewer Development Plan

This document outlines the plan for building a standalone PySide6-based mesh viewer to visualize the icosphere and later stages of the planet generation pipeline.

The goal is to support visual debugging, overlay development, and eventual reuse within in-game tools like the map editor or generation screens.

---

## 📂 Key Integration Points

These files are useful references or integration points when developing the mesh viewer:

- `generation/models/planet.py` — The `Planet` data structure (viewer expects a `Planet` instance)
- `generation/models/mesh.py` — The `MeshData` class (contains vertices, faces, adjacency)
- `generation/generate_planet.py` — Pipeline CLI entry point
- `generation/pipeline/export_planet/hdf5_export.py` — Read/write `.planetbin` format
- `shared/config/planet_gen_config.py` — Load generation config if needed
- `tests/generation/models/test_planet_io.py` — Example of loading a `.planetbin` file

New abilities:
- Viewer can **load a `.planetbin` directly** (without regenerating)
- Viewer can be launched **as a dev tool**, **from CLI**, or **in future UIs**
- Viewer can operate on a simplified `MeshRenderData` DTO extracted from a `Planet`

---

## 🎯 Objectives

- Render the generated mesh (vertices, faces) using PySide6
- Support rotation, zoom, and selection
- Display overlays (face index, region ID, tectonic plate, etc.)
- Design architecture for future embedding (e.g. as `PlanetViewer(QWidget)`)
- Allow live viewing from the pipeline or CLI with `--view`
- Allow viewing a saved `.planetbin` via `--load path`
- Decouple rendering from data model using a `MeshRenderData` object

---

## 🧱 Session 1: Setup and Base Viewer

**Goal:** Minimal working viewer that can display a mesh

### Tasks:
- Create branch: `feature/planet-mesh-viewer`
- Create folder: `ui/tools/mesh_viewer/`
- Build PySide6 app with `QMainWindow` + `QOpenGLWidget`
- Accept a `Planet` object or path to `.planetbin` and extract `MeshRenderData`
- Render mesh (wireframe) from `MeshRenderData`
- Add mouse control: rotate, zoom
- Show basic logging/debug output
- Add dev CLI entrypoint: `python -m ui.tools.mesh_viewer --load path/to.planetbin`

---

## 🎨 Session 2: Overlays and UI Controls

**Goal:** Add modular overlay system to visualize mesh metadata

### Tasks:
- Define `Overlay` base class with `render()` and `handle_mouse()` methods
- Load overlays dynamically for toggling
- Draw face indices as labels
- Add color overlays for:
  - Elevation (continuous colormap)
  - Region/group ID (discrete color by index)
- Add overlay mode switcher (toolbar or sidebar)

---

## 🔄 Session 3: CLI and Pipeline Integration

**Goal:** Enable live debug viewing during planet generation or standalone use

### Tasks:
- Add `PlanetViewer.show(planet)` function
- Add CLI flag to `generate_planet.py`:
  - `--view` to launch viewer with the generated planet
- Add CLI flag to mesh viewer tool:
  - `--load path/to.planetbin`
- Optional: auto-reload view when `.planetbin` changes (dev mode)
- Optional: hotkey reload (e.g. press `R` to reload)
- Optional: save screenshot of current view
- Optional: display overlay debug info in logs

---

## 🛠️ Design Considerations

- Use `QOpenGLWidget` for future performance and flexibility
- Stick to PySide6-compatible rendering (no `moderngl`, `pyglet`, etc.)
- Watch for row/column-major issues when passing NumPy arrays to OpenGL
- Keep `PlanetViewer` self-contained and embeddable in larger UIs
- Support hover inspection via face picking
- Consider hot-reloadable config for overlay color/label schemes

---

## ✅ Future Goals

- Highlight hovered face and show data popup
- Click-to-select and inspect face, plate, or region
- Add comparison mode to toggle between overlay types
- Integrate time-based animations (plate motion, erosion stages)
- Prepare export-to-image or export-overlay-data options

