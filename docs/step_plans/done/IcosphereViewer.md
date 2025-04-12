# Session 1: Setup and Base Viewer

**Goal:** Create a minimal working PySide6-based viewer that loads and displays a planet mesh using OpenGL.

This viewer will act as a standalone dev tool, with support for loading a `.planetbin` file, extracting mesh data, and rendering the geometry using mouse controls for camera interaction.

---

## 📁 Setup

- Create Git branch: `feature/planet-mesh-viewer`
- Directory: `ui/tools/mesh_viewer/`
- Add module entrypoint: `launch_viewer.py` with CLI support (avoid `__main__.py`)
- CLI usage:
  ```bash
  python -m ui.tools.mesh_viewer.launch_viewer --load path/to.planetbin
  ```

---

## 📂 File Structure

```
ui/
└── tools/
    └── mesh_viewer/
        ├── launch_viewer.py        # CLI entrypoint for the standalone viewer
        ├── viewer_app.py            # Contains PlanetViewerApp (QMainWindow)
        ├── gl_widget.py             # Contains PlanetGLWidget (QOpenGLWidget)
        ├── mesh_render_data.py      # MeshRenderData class (DTO for rendering)
        ├── planet_loader.py         # Load .planetbin → MeshRenderData
        ├── camera_controller.py     # (Skipped) Handles orbit camera movement
        └── utils.py                 # (Skipped) GL math helpers, constants, etc.
```

**Tests:**
```
tests/
└── ui/
    └── tools/
        └── mesh_viewer/
            ├── test_mesh_render_data.py
            ├── test_planet_loader.py
            └── test_camera_controller.py
```

---

## 🧱 Core Components

### 1. `PlanetViewerApp`
- Subclass of `QMainWindow`
- Hosts a `PlanetGLWidget` and optional sidebar/console in the future
- Manages `MeshRenderData` loading and passing into the OpenGL widget

### 2. `PlanetGLWidget`
- Subclass of `QOpenGLWidget`
- Renders the icosphere using vertex and face arrays
- Wireframe mode only for now
- Mouse interaction:
  - Left-drag: rotate
  - Scroll: zoom in/out

### 3. `MeshRenderData`
- Lightweight DTO to decouple viewer from full `Planet` object
- Fields:
  ```python
  class MeshRenderData:
      vertices: np.ndarray  # shape (n, 3)
      faces: np.ndarray     # shape (m, 3)
      face_ids: Optional[np.ndarray] = None
      elevation: Optional[np.ndarray] = None
  ```
- Can be constructed from a `Planet` or `.planetbin` file

### 4. `planet_loader.py`
- Loads `.planetbin` and extracts `MeshRenderData`
- May log details (vertex count, face count, etc.)

---

## 🔧 Logging
- Use project logger (`get_logger(__name__)`)
- Log key steps:
  - Startup/init
  - File load
  - Mesh stats
  - OpenGL render calls

---

## ✅ Milestone Checklist
- [X] Project folder and entrypoint in place
- [X] CLI flag `--load` implemented
- [X] `.planetbin` loader and `MeshRenderData` extractor
- [X] PySide6 app launches with viewer window
- [X] OpenGL widget renders basic wireframe
- [X] Rotation and zoom via mouse working
- [X] Log output visible in console

---

## 📌 Testing Strategy

### Write Now (Unit Tests):
- `MeshRenderData`: shape validation, serialization, etc.
- `planet_loader.py`: `.planetbin` loading, failure modes
- Any utility modules (camera math, transforms)

### Defer (Manual/Integration):
- `PlanetGLWidget`: render loop, OpenGL drawing
- `PlanetViewerApp`: full UI behavior and input interaction

Use `tests/ui/tools/mesh_viewer/` for local tests that don't rely on pipeline.

---

## 📌 Notes for Future Work
- Camera orbit math should remain modular for reuse in overlays or other views
- Add hotkey handler scaffold (even if empty)
- Prepare `MeshRenderData` to store overlay metadata in future sessions

