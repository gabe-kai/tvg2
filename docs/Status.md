# Project Status

`docs/Status.md`

## Daily Commit Summaries

- 2025.03.31:  Created folder structure and starting documentation. Developed PipelineDesign.md + 3 layer-specific pipeline docs. Scaffolded core data models for the planet generation pipeline.
- 2025.04.01:  Implement custom logging. Implement Feature: generate-mesh-pipeline. Implement Feature: planetbin-export.
- 2025.04.02:  Create custom feature project_layout_manager.
- 2025.04.03:  Update the ProjectLayout and a lot of descriptions. Built the standalone mesh viewer, phase 1 (simple).
- 2025.04.07:  Built Overlay system. Built Toolbar: wireframe, rotation lock, & auto-rotate.
- 2025.04.08:  Added Face ID overlay. Added Icosphere Mesh relaxer.
- 2025.04.09:  Updated Flat-Shading mode, added Sunlit-Shaded mode. Added a Normals overlay.
- 2025.04.10:  Build seed_cratons step to the generate_planet pipeline.
- 2025.04.11:  Built the cratons_overlay for the mesh-viewer. Changed all overlays to start unchecked.
- 2025.04.12:  Fixed the Craton Overlay flat-shading. Improved craton seeding performance.
- 2025.04.17:  Refactored generate_planet to split CLI arguments into another module. Refactored IcosphereMeshStrategy to calculate & store face centroids.

---

## In-Progress and Next-Up

[X] Refactor generate_planet to split the CLI commands into a new module.
[X] Refactor the generate_mesh step to calculate and store face centroids. Note that they will need to be updated after mesh deformations.
[ ] Implement the simulate_plate_motion pipeline steps.
[ ] Enable live debug viewing during planet generation or standalone use.

---

## Critical Conventions
### Python File Notes
- Start every python file with a line-1 comment displaying the relative path and filename.
- Ensure that every class, method, and function has a docstring.
- Use inline comments extensively to explain what things do.
- Put imports at the top of the file, not above the function / method that uses it. Sort the imports into groups by function.
- Don't name anything `__main__.py` or `config.py`, those are reserved. Use names specific to the feature or utility.

### Logging System
Use the project logger, not Python’s default logging.getLogger(), when building or updating files.

Import via:
```python
from shared.logging.logger import get_logger
log = get_logger(__name__)
```

Use log.debug(), log.info(), log.warning(), etc. as needed.
For detailed tracing during debugging, use log.trace() (lower than debug).

Logging is configured automatically; no setup is needed in each file.
When building logging for unit tests, put the logs in tests/logs/, not in logs/ or in test-specific folders.

---

## 🧭 Working Set Overview

- **Status**: This file – Daily log, bugs, and short-term goals
- **Project Layout**: [`docs/ProjectLayout.md`](../docs/ProjectLayout.md) – File & folder structure with comments
- **Pipeline Design (Global)**: [`docs/PipelineDesign.md`](../docs/PipelineDesign.md) – High-level overview of all 3 layers
- **Planet Generation Design**: [`generation/docs/PlanetPipeline.md`](../generation/docs/PlanetPipeline.md)
- **Game Logic Design**: [`game_logic/docs/GamePipeline.md`](../game_logic/docs/GamePipeline.md)
- **UI Design**: [`ui/docs/UIPipeline.md`](../ui/docs/UIPipeline.md)
- **Planet Models**: [`generation/models/planet.py`](../generation/models/planet.py) and [related model files](../generation/models/)