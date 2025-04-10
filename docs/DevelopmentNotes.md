# Development Notes

`docs/DevelopmentNotes.md`

## Git Branch Prefixes
Use these prefixes to keep your branches organized and searchable:

- `feature/` – New gameplay, generation, or UI feature
- `bugfix/` or `fix/` – Corrects unintended behavior or errors
- `refactor/` – Restructures code without changing functionality
- `setup/` – Initial project setup or structural scaffolding
- `chore/` – Dev tooling, dependencies, or minor cleanup
- `doc/` – Documentation additions or updates
- `test/` – Test creation, updates, or fixes
- `infra/` – CI/CD, build tools, scripts, and automation
- `perf/` – Performance improvements
- `hotfix/` – Emergency patch to address production-critical issue


## Mesh Overlay Conventions
When creating a new mesh overlay (e.g. for tectonics, climate, or debug output), ensure it follows these guidelines:

- Inherit from the `Overlay` base class defined in `overlays/base.py`
- Implement the following methods:
  - `get_name()` – A short, unique label for toggling the overlay
  - `get_category()` – A logical grouping such as "Debug", "Terrain", "Political"
  - `get_description()` – A short explanation of what the overlay does (used in UI or tooltips)
- If the overlay requires data from the `Planet`, ensure the corresponding generation pipeline step populates the required field(s) in `MeshRenderData`.
- Register new overlays in a central location (e.g. `ALL_OVERLAYS`) to make them auto-discoverable by the UI and CLI.

This makes overlays modular, inspectable, and consistent with UI behavior.


## Viewer Rendering & Coordinate Spaces
OpenGL viewer overlays (e.g. face normals, labels, arrows) must account for the difference between **world space** and **camera (eye) space**:

- Mesh geometry (`vertices`, `normals`, `centroids`) exists in **world space**.
- OpenGL applies a **modelview transformation** to convert this data into camera (eye) space before rendering.
- The viewer rotates the camera via `glRotatef(...)`, but this doesn't affect the mesh data — it affects the **modelview matrix**, which changes every frame.

### Checking Visibility: Camera-Facing Only
To determine whether a face is **visible to the camera**:

1. Compute the **face normal in world space**.
2. Extract the **rotation portion** of the current modelview matrix:
   ```python
   modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
   rotation_matrix = np.array([
       [modelview[0][0], modelview[0][1], modelview[0][2]],
       [modelview[1][0], modelview[1][1], modelview[1][2]],
       [modelview[2][0], modelview[2][1], modelview[2][2]],
   ])
   ```
3. **Transform the normal** into camera space using the **transpose** of the rotation matrix:
   ```python
   normal_camera = rotation_matrix.T @ normal_world
   ```
4. In camera space, the viewer always looks along the **negative Z axis** (`[0, 0, -1]`).
5. If `np.dot(normal_camera, [0, 0, -1]) < 0`, the face is **front-facing** → draw it.

### Bonus: Use `gluProject` to Confirm Visibility
To ensure a face is not offscreen or behind the camera:

```python
win_x, win_y, win_z = gluProject(x, y, z, modelview, projection, viewport)
if 0.0 <= win_z <= 1.0:
    # on screen
```

Use this in tandem with the normal test to draw overlays **only on visible geometry**.
