# 🖱 Session 2: Overlays and Viewer Controls

**Goal:** Introduce a modular overlay system and a basic UI panel to toggle overlay visibility and viewer behaviors (e.g. rotation lock, wireframe vs. shaded, etc.).

---

## 📙 Core Features to Build

### ✅ 1. **Overlay Architecture**
- Create abstract base class `Overlay`
  - Methods:
    ```python
    class Overlay:
        def render(self, gl: QOpenGLWidget): ...
        def handle_mouse(self, event: QMouseEvent): ...
        def update_data(self, mesh_data: MeshRenderData): ...
        def get_name(self) -> str: ...
    ```
- Define a `BaseOverlayManager` to hold active overlays and call their `render()` in the main widget.
- Overlays should be **lightweight modules** (not subclasses of `PlanetGLWidget`) to allow composability and reuse.
- Store overlays in `ui/tools/mesh_viewer/overlays/` (e.g. `face_index_overlay.py`, `elevation_overlay.py`, etc.)

---

### ✅ 2. **Built-in Overlays**

#### 🔢 a. Face Index Overlay
- Draw face IDs (from `face_ids`) centered on each face using QPainter or OpenGL labels.
- Use a toggle for visibility.

#### 🌍 b. Elevation Overlay
- Use `elevation` field from `MeshRenderData`
- Color each face based on interpolated elevation (e.g. grayscale or Viridis)
- Fallback if no elevation data is present

#### 🗏️ c. Region ID Overlay *(placeholder for future)*
- If `face_region_ids` exists, color each face using a discrete colormap
- Use flat, face-wise coloring

#### 🌌 d. Normals Overlay *(new)*
- Display a line for each face pointing in the direction of its normal
- Color-code front- and back-facing normals (e.g. green for front, red for back)
- Optional: Add toggle to show/hide

---

### ✅ 3. **OverlayManager Integration**

- Add to `PlanetGLWidget`:
  ```python
  self.overlay_manager = OverlayManager()
  ```
- On render:
  ```python
  self.overlay_manager.render(self)
  ```

- On `MeshRenderData` update:
  ```python
  self.overlay_manager.update_data(mesh_data)
  ```

---

## 🤯 4. **Viewer Control UI (Sidebar or Toolbar)**

- Add a toggleable **sidebar panel** or **toolbar** in `PlanetViewerApp`
- Options:
  - [X] Wireframe / Filled mode (OpenGL state toggle)
  - [X] Lock/Unlock Rotation
  - [X] Enable Auto-Rotation
  - [X] Toggle Face IDs
  - [ ] Toggle Elevation Overlay
  - [ ] Toggle Region Overlay
  - [ ] Toggle Normals Overlay
  - [ ] Reset Camera
- Optional: Color map dropdown for elevation
- Optional: Lighting toggle for shaded/flat mode

Implementation tips:
- Use `QToolBar` or `QDockWidget` on the right
- Store user toggles in `PlanetViewerApp`, pass to `PlanetGLWidget`

---

## 📁 File Layout Changes

```
ui/tools/mesh_viewer/
├── overlays/
│   ├── __init__.py
│   ├── base.py              # Overlay ABC
│   ├── face_index_overlay.py
│   ├── elevation_overlay.py
│   ├── region_overlay.py    # (stub for now)
│   └── normals_overlay.py   # (new)
├── overlay_manager.py       # Coordinates active overlays
├── viewer_app.py            # Add sidebar panel and state toggles
├── gl_widget.py             # Calls overlay_manager.render()
```

---

## ✅ Milestone Checklist

- [X] `Overlay` base class
- [X] `OverlayManager` for registration + dispatch
- [X] Face index overlay (draws numeric face labels)
- [ ] Elevation overlay (color-by-scalar)
- [ ] Stub region overlay (discrete color fallback)
- [ ] Normals overlay (face normals, front/back coloring)
- [X] Sidebar or toolbar toggle UI
- [ ] Add logging on overlay switch
- [X] Viewer control state updates (wireframe toggle, lock rotation)
- [ ] Lighting toggle (flat vs shaded)
- [ ] Pass toggles from `PlanetViewerApp` → `PlanetGLWidget`

---

## 🥪 Tests & Dev Notes

- Use `tests/ui/tools/mesh_viewer/test_overlay_manager.py`
- Write unit tests for:
  - Overlay registration
  - Per-overlay toggle behavior
  - Fallback/no-data scenarios
- Manual test overlays using sample `.planetbin`

---

## 🕜️ Staging for Session 3

- Make overlay manager able to register overlays dynamically by name
- Prepare hooks for CLI to choose overlays or live toggle
- Consider overlay config format (e.g. JSON or `.toml`) for saving current settings
