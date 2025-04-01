# ui/docs/UIPipeline.md
# ========================================
# UI Pipeline – Detailed Design
# ========================================

This document outlines the structure and intent of the UI pipeline for The Vassal Game (TVG2).

The UI is responsible for visualizing the planet and world state, presenting player information, and capturing input. It consumes the output of both the Planet Generation and Game Logic pipelines.

Like the other layers, the UI follows a `pipeline-as-code` design to separate data processing, rendering, and user interaction into modular, testable stages.

---

## 🖼️ Overview

- The UI receives data from `Planet` and `GameState`
- Processes that data into renderable layers and widgets
- Supports both interactive (live) and passive (replay) modes
- Initially prototyped in **Python + PySide6**
- Final implementation planned in **C/C++** or other native UI framework

---

## 🧩 Pipeline Stages

Each stage is modular and may support multiple strategies (e.g. headless test render, debug overlays, low vs high fidelity). Layout follows the standard strategy pattern:

```
ui/pipeline/<stage_name>/
  ├── base.py
  ├── default.py
  └── __init__.py
```

### 1. `LoadPlanetAsset`
- Reads `.planetbin` file or streaming data
- Produces `Planet` instance for rendering context

### 2. `LoadGameState`
- Loads `GameState` snapshot or live socket feed
- Drives dynamic UI layers like borders, economy, population

### 3. `GenerateMapLayers`
- Converts terrain, biomes, nations into renderable tile layers
- Produces layered maps for height, climate, political views

### 4. `RenderViewport`
- Renders the camera-facing portion of the map
- Handles zoom, pan, rotation, and lighting effects

### 5. `RenderUIWidgets`
- Renders tooltips, stats panels, action buttons
- Driven by player context and game mode

### 6. `HandleInput`
- Captures keyboard/mouse/controller input
- Dispatches actions back to game logic or camera controls

---

## 🧱 UIState Object

```python
@dataclass
class UIState:
    planet: Planet
    game_state: Optional[GameState]
    viewport: Viewport
    active_layer: str
    selected_tile: Optional[int]
    overlays: Dict[str, Any]
```

This object is the data core passed between UI stages.

---

## 🔧 Orchestration Example

```python
pipeline = [
    LoadPlanetAsset(path='world.planetbin'),
    LoadGameState(source='autosave.gamestate'),
    GenerateMapLayers(strategy='stacked'),
    RenderViewport(),
    RenderUIWidgets(),
    HandleInput()
]

ui_state = UIState(...)
for stage in pipeline:
    ui_state = stage.run(ui_state)
```

---

## ✅ Implementation Guidelines

- Initial pipeline will be headless-compatible for preview and testing
- Should support snapshot-to-render and frame-by-frame playback
- Each stage should render to or mutate only its own part of UIState
- Pipelines may differ between editor, gameplay, and cinematic modes
- Long-term goal: export all visuals to native C++ UI front-end

---

## 📁 Location
- Module path: `ui/pipeline/`
- Each stage in its own subfolder
- `UIState` and helpers live in `ui/models/`
- Orchestrator lives in `ui/ui_runner.py`

---

Consumes:
- `generation/models/planet.py`
- `game_logic/models/game_state.py`

Outputs:
- Rendered visuals
- Player interaction events
