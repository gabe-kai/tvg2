# game_logic/docs/GamePipeline.md
# ============================================
# Game Logic Pipeline – Detailed Design
# ============================================

This document outlines the structure and purpose of the game logic pipeline for The Vassal Game (TVG2).

This layer simulates world behavior and history over time, operating on a static, immutable planet and evolving a dynamic `GameState` object.

Each stage is implemented as a modular class with a `run(game_state: GameState) -> GameState` method, and follows the `pipeline-as-code` model from [`docs/PipelineDesign.md`](../../docs/PipelineDesign.md).

---

## 🧠 Overview

The game logic pipeline applies turn-based simulation to civilizations, diplomacy, culture, events, and historical development. This logic is intended to run both offline and during live gameplay.

Stages are stateless processors that incrementally update the `GameState` object. The pipeline is fully deterministic given a fixed seed + planet.

---

## 🔁 Pipeline Stages

Each stage lives in its own folder within `game_logic/pipeline/` using a strategy-based pattern:

```
game_logic/pipeline/<stage_name>/
  ├── base.py            # Abstract base class (e.g. DiplomacyStrategy)
  ├── default.py         # Default reference implementation
  └── __init__.py        # get_strategy(name: str) -> strategy instance
```

### 1. `InitializeGameState`
- Inputs: `Planet` + seed
- Outputs: initial `GameState`
- Assigns initial civs, borders, traits, and technologies

### 2. `TickCivilizations`
- Updates population, tech, economy, and ideologies
- Handles internal development of each nation

### 3. `ProcessDiplomacy`
- Evaluates alliances, treaties, rivalries, and conflicts
- Updates international state matrix

### 4. `ExecuteActions`
- Applies AI decisions and player inputs
- Includes expansion, warfare, resource usage, reforms

### 5. `ApplyEvents`
- Random or deterministic global/local events
- Includes disasters, migrations, discoveries, revolts

### 6. `UpdateWorldState`
- Aggregates deltas and commits to world snapshot
- Updates persistent records and archives

### 7. `ExportGameState`
- Serializes current state to file, stream, or UI memory

---

## 📦 GameState Object

The simulation operates over a central `GameState` container:
```python
@dataclass
class GameState:
    turn: int
    seed: int
    planet: Planet
    civilizations: List[Civilization]
    diplomacy_matrix: DiplomacyMatrix
    events: List[WorldEvent]
    logs: List[TurnLog]
```

Each simulation stage modifies this state and returns a copy (or applies deltas).

---

## 🔧 Orchestration Example

```python
pipeline = [
    InitializeGameState(strategy='default'),
    TickCivilizations(strategy='standard'),
    ProcessDiplomacy(strategy='matrix_v1'),
    ExecuteActions(strategy='priority_ai'),
    ApplyEvents(strategy='stochastic'),
    UpdateWorldState(),
    ExportGameState()
]

game_state = None
for stage in pipeline:
    game_state = stage.run(game_state)
```

---

## ✅ Implementation Guidelines

- Each stage must be idempotent and independent
- GameState should be versioned or snapshot-able for undo/redo or playback
- Prefer shallow diffs and deltas for performance
- Strategies should be hot-swappable and testable in isolation
- Consider separating AI planning from action execution stages

---

## 📁 Location
- Module path: `game_logic/pipeline/`
- Each stage is a subfolder
- Models live in `game_logic/models/`
- Orchestrator lives in `game_logic/orchestrator.py`

---

For Planet input schema, see `generation/models/planet.py`
For GameState schema, see `game_logic/models/game_state.py`
