# Planet Generation Pipeline – Detailed Design

`generation/docs/PlanetPipeline.md`

This document outlines the structure and purpose of each stage in the planet generation pipeline for The Vassal Game (TVG2).

Each stage is implemented as a standalone class with a `run(planet: Planet) -> Planet` method and follows the pipeline-as-code model defined in the high-level [`docs/PipelineDesign.md`](../../docs/PipelineDesign.md).

---

## 🌍 Overview

The generation pipeline creates a complete, immutable planet structure that the game logic and UI layers will consume. This data is intended to be serialized to a binary `.planetbin` format.

The pipeline is deterministic based on a seed value and designed for modular, stage-by-stage execution.

Each stage is structured to allow for **multiple interchangeable implementations**, from basic prototypes to advanced, parameterized models. This supports experimentation, development progression, and user-configurable complexity.

A shared pattern is followed:
- Each stage imports a strategy from a subfolder (e.g. `seed_cratons/`)
- Each subfolder contains one or more implementations, all subclassing a shared `BaseStrategy`
- The orchestrator dispatches to the appropriate implementation using a factory method or configuration directive

---

## 📊 Pipeline Stages

Each stage follows this naming and structure pattern:
```
/pipeline/<stage_name>/
  ├── base.py               # Abstract base class (e.g. SeedCratonsStrategy)
  ├── <strategy1>.py        # First implementation (e.g. random.py)
  ├── <strategy2>.py        # More refined alternative
  └── __init__.py           # get_strategy(name: str) -> strategy instance
```

Example stage entries:

### 1. `GenerateMesh`
- Subdivides a base icosahedron into a hex/triangle mesh
- Inputs: radius, subdivision level, seed
- Outputs: vertices, faces, adjacency map

### 2. `SeedCratons`
- Seeds ancient landmasses (cratons) on the mesh
- Outputs: list of craton objects

### 3. `SimulatePlateMotion`
- Expands tectonic plates from cratons
- Assigns motion vectors, boundaries, and interaction types
- Outputs: list of plates, tectonic map per face

### 4. `GenerateElevation`
- Uses tectonic context to deform terrain (mountains, rifts, trenches)
- Outputs: elevation per face or vertex

### 5. `SimulateErosion`
- Applies erosion simulation over elevation map
- Outputs: modified elevation, drainage map

### 6. `SimulateClimate`
- Calculates temperature and precipitation per face
- Outputs: climate data map

### 7. `GenerateBiomes`
- Maps biomes based on climate and elevation
- Outputs: biome ID per face

### 8. `PopulateRegions`
- Places geographic labels (continents, oceans, mountain ranges)
- Outputs: region metadata layer

### 9. `GeneratePoliticalMap`
- Seeds nations and draws territorial borders
- Outputs: political ownership per face, nation metadata

### 10. `ExportPlanet`
- Compresses and serializes the entire `Planet` object
- Outputs: `.planetbin` file

---

## 🔧 Orchestration Example

```python
pipeline = [
    GenerateMesh(),
    SeedCratons(strategy='random'),
    SimulatePlateMotion(strategy='vector_growth'),
    GenerateElevation(strategy='orogenic'),
    SimulateErosion(strategy='hydraulic'),
    SimulateClimate(strategy='global_model'),
    GenerateBiomes(strategy='whittaker'),
    PopulateRegions(strategy='namegen'),
    GeneratePoliticalMap(strategy='territorial'),
    ExportPlanet()
]

planet = Planet(radius=1.0, subdivision_level=6, seed=42)
for stage in pipeline:
    planet = stage.run(planet)
```

---

## ✅ Implementation Guidelines

- Each stage must be idempotent and pure (no global state)
- Prefer `run(planet: Planet) -> Planet` interface
- Stages should log timing and summary stats
- Strategy implementations should live in subfolders with `base.py` and `get_strategy()`
- Use shared base classes and ABCs for consistency across strategies
- Avoid tight coupling; each stage should only depend on the structure of `Planet`

---

## 📁 Location
- Module path: `generation/pipeline/`
- Each stage lives in its own folder:
  - Example: `generation/pipeline/simulate_erosion/`
  - Strategies: `simulate_erosion/random.py`, `simulate_erosion/river.py`, etc.
  - Interface: `simulate_erosion/base.py`, `__init__.py` exposes factory
- Orchestrator lives in `generation/main.py`

---

For schema and data structure details, see `generation/models/planet.py`.
