# Project Status

`docs/Status.md`

## Daily Commit Summaries

- 2025.03.31:  Created folder structure and starting documentation. Developed PipelineDesign.md + 3 layer-specific pipeline docs. Scaffolded core data models for the planet generation pipeline.
- 2025.04.01:  Implement custom logging. Implement Feature: generate-mesh-pipeline. Implement Feature: planetbin-export.
- 2025.04.02:  Create custom feature project_layout_manager.

---

## In-Progress and Next-Up

Build the planet-mesh-viewer standalone app for quick viewing and debugging of our planet generation pipeline.

---

## Critical Conventions
### Python File Notes
- Start every python file with a line-1 comment displaying the relative path and filename.
- Ensure that every class, method, and function has a docstring.
- Use inline comments extensively to explain what things do.
- Put imports at the top of the file, not above the function / method that uses it. Sort the imports into groups by function.

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

---

## 🧭 Working Set Overview

- **Status**: This file – Daily log, bugs, and short-term goals
- **Project Layout**: [`docs/ProjectLayout.md`](../docs/ProjectLayout.md) – File & folder structure with comments
- **Pipeline Design (Global)**: [`docs/PipelineDesign.md`](../docs/PipelineDesign.md) – High-level overview of all 3 layers
- **Planet Generation Design**: [`generation/docs/PlanetPipeline.md`](../generation/docs/PlanetPipeline.md)
- **Game Logic Design**: [`game_logic/docs/GamePipeline.md`](../game_logic/docs/GamePipeline.md)
- **UI Design**: [`ui/docs/UIPipeline.md`](../ui/docs/UIPipeline.md)
- **Planet Models**: [`generation/models/planet.py`](../generation/models/planet.py) and [related model files](../generation/models/)
