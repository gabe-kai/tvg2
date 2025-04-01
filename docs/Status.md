# Project Status

`docs/Status.md`

## Daily Commit Summaries

- 2025.03.31:  Created folder structure and starting documentation. Developed PipelineDesign.md + 3 layer-specific pipeline docs. Scaffolded core data models for the planet generation pipeline.

---

## In-Progress and Next-Up

Building the logging system.

Fixing a bug in the structure_dump script: if I create a file / folder that sorts alphabetically later it marks the files already there as Removed, and also re-adds them in new alphabetical ordering. 
Extending the structure_dump script to allow custom ordering.

---

## Critical Conventions
### Python File Notes
- Start every python file with a line-1 comment displaying the relative path and filename.
- Ensure that every class, method, and function has a docstring.
- Use inline comments extensively to explain what things do.
- Put imports at the top of the file, not above the function / method that uses it. Sort the imports into groups by function.

### Logging System
TBD (but it is critical!)

---

## 🧭 Working Set Overview

- **Status**: This file – Daily log, bugs, and short-term goals
- **Project Layout**: [`docs/ProjectLayout.md`](../docs/ProjectLayout.md) – File & folder structure with comments
- **Pipeline Design (Global)**: [`docs/PipelineDesign.md`](../docs/PipelineDesign.md) – High-level overview of all 3 layers
- **Planet Generation Design**: [`generation/docs/PlanetPipeline.md`](../generation/docs/PlanetPipeline.md)
- **Game Logic Design**: [`game_logic/docs/GamePipeline.md`](../game_logic/docs/GamePipeline.md)
- **UI Design**: [`ui/docs/UIPipeline.md`](../ui/docs/UIPipeline.md)
- **Planet Models**: [`generation/models/planet.py`](../generation/models/planet.py) and [related model files](../generation/models/)
