# Pipeline Design - High-Level Overview for The Vassal Game

`docs/PipelineDesign.md`

This document outlines the **high-level architecture and pipeline philosophy** for The Vassal Game (TVG2). Each major layer (planet generation, game logic, UI) follows a modular, pipeline-driven approach to promote scalability, testability, and clarity.

## Git
Repository: https://github.com/gabe-kai/tvg2

Local Path: C:\Users\gabek\PycharmProjects\tvg2

## 🧩 Pipeline-as-Code Philosophy

We follow a `pipeline-as-code` pattern:
- Each step is a **pluggable module** with a common interface (e.g. `run(data) -> data`)
- Each layer has its own **orchestrator** that wires together its pipeline
- Layers communicate via **well-defined APIs or file formats**, not function calls
- Each pipeline can be run in isolation, headless, or integrated into the game loop


## 🗂️ Layer Breakdown

### 1. 🌍 Planet Generation Layer
Module path: `generation/`
Detailed spec: [`generation/docs/PlanetPipeline.md`]

- Generates a complete planet from scratch
- Stateless and deterministic from seed
- Produces the immutable world data used by all downstream logic

#### Pipeline Stages:
1. `GenerateMesh` – Create icosphere mesh from radius and subdivision level
2. `SeedCratons` – Place primordial tectonic blocks
3. `SimulatePlateMotion` – Assign plate boundaries and simulate motion
4. `GenerateElevation` – Use tectonics to raise/lower terrain
5. `SimulateErosion` – Water and wind erosion modeling
6. `SimulateClimate` – Atmospheric patterns, ocean currents
7. `GenerateBiomes` – Map biome zones based on temperature + rainfall
8. `PopulateRegions` – Pre-populate with nations, capitals, cities
9. `GeneratePoliticalMap` – Assign territory control, influence maps
10. `ExportPlanet` – Save to binary `.planetbin` format

Each stage transforms a shared `Planet` object passed down the pipeline.


### 2. 🧠 Game Logic Layer
Module path: `game_logic/`
Detailed spec: [`game_logic/docs/GamePipeline.md`]

- Runs the simulation over the static planet
- Applies world state transitions, AI decisions, diplomacy, economy, etc.
- Treats the planet as read-only input

#### Potential Pipeline Flow:
1. `InitializeGameState` – Load planet + seed initial world state
2. `TickCivilizations` – Simulate cultural, technological, and economic growth
3. `ProcessDiplomacy` – Resolve treaties, wars, influence spread
4. `ExecuteActions` – Carry out AI plans and player inputs
5. `ApplyEvents` – Climate events, disasters, migrations
6. `UpdateWorldState` – Commit deltas to the game database
7. `ExportGameState` – Save snapshots for rendering or serialization


### 3. 🖥️ UI Layer
Module path: `ui/`
Detailed spec: [`ui/docs/UIPipeline.md`]

- Presents the world and its state to the player
- Driven by a UI-specific pipeline that transforms simulation state into visuals
- Prototyped in PySide6, later migrated to C/C++

#### Potential UI Pipeline Flow:
1. `LoadPlanetAsset` – Read binary planet file or stream
2. `LoadGameState` – Attach to game state snapshot or feed
3. `GenerateMapLayers` – Convert terrain, biomes, and politics into renderable overlays
4. `RenderViewport` – Handle user camera, zoom, pan
5. `RenderUIWidgets` – Update HUD, tooltips, overlays
6. `HandleInput` – Capture and translate player actions into game events


## 📎 Document Structure

This file is a master index of pipeline concepts. Each layer has its own design document:
- `generation/docs/PlanetPipeline.md`
- `game_logic/docs/GamePipeline.md`
- `ui/docs/UIPipeline.md`

Keep this document updated with major structural changes or new pipelines.
