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
