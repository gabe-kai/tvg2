# Refactor Plan: Modularize `generate_planet.py` CLI and Pipeline Logic

## 📌 Branch Info
- **Branch Name:** `refactor/split-generate-planet`
- **Type:** Structural refactor (tracked in `Status.md`)
- **Scope:** Modularization of CLI parsing, config handling, and pipeline stages from `generate_planet.py`

---

## 🧠 Motivation
The `generate_planet.py` file currently mixes CLI parsing, parameter merging, planet creation, and pipeline orchestration. As feature complexity increases (e.g. craton seeding, elevation, climate), this structure becomes harder to maintain and test.

---

## 🧩 Goals
- Separate CLI parsing from pipeline logic
- Separate parameter merging from core logic
- Ensure CLI and config parameters stay in sync
- Prepare for scalable, stage-based config handling
- Keep entry point minimal and import-safe

---

## 🗂️ New File Structure
```
generation/
├── generate_planet.py              ← CLI entry point (minimal glue)
├── cli/
│   ├── argument_parser.py          ← Defines CLI arguments and parsing
│   ├── parameter_merge.py          ← Merges CLI + config by stage
│   └── constants.py                ← Parameter schemas / stage keys
└── pipeline/
    ├── run_mesh.py                 ← Mesh generation stage
    ├── run_cratons.py              ← Craton seeding stage
    └── run_export.py               ← Export stage
```

---

## 📜 Task Breakdown

### ✅ 1. Create `cli/argument_parser.py`
- Extract `argparse` setup
- Implement:
  ```python
  def parse_args(argv=None) -> tuple[PlanetGenConfig, dict[str, Any]]:
  ```
- Returns a `PlanetGenConfig` object and a dict of user CLI args

---

### ✅ 2. Create `cli/constants.py`
- Define reusable param schemas for each pipeline stage:
  ```python
  CRATON_PARAMS = {
      "strategy": {"type": str, "default": "spaced_random"},
      "count": {"type": int, "default": 8},
      "spacing_factor": {"type": float, "default": 1.0}
  }
  ```
- Enables consistent defaults, CLI argument auto-gen, validation, and logging

---

### ✅ 3. Create `cli/parameter_merge.py`
- Implement:
  ```python
  def resolve_stage_params(stage_key: str, schema: dict, cli_args: dict, config: PlanetGenConfig) -> dict
  ```
- Merge: CLI → config → schema defaults
- Ignores unrelated keys, supports logging of resolved values

---

### ✅ 4. Create `pipeline/run_<stage>.py` for each stage
**Example: `pipeline/run_cratons.py`**
```python
def run_cratons(planet, config, cli_args):
    from cli.constants import CRATON_PARAMS
    from cli.parameter_merge import resolve_stage_params
    from generation.pipeline.seed_cratons import get_strategy

    params = resolve_stage_params("craton_seeding", CRATON_PARAMS, cli_args, config)
    strategy = get_strategy(params.pop("strategy"), **params)
    return strategy.run(planet)
```
Repeat for:
- `run_mesh.py`
- `run_export.py`

---

### ✅ 5. Update `generate_planet.py` to delegate only
```python
from cli.argument_parser import parse_args
from pipeline.run_mesh import run_mesh
from pipeline.run_cratons import run_cratons
from pipeline.run_export import run_export

if __name__ == '__main__':
    config, cli_args = parse_args()
    planet = Planet(config.radius, config.subdivision, config.seed)

    planet = run_mesh(planet, config, cli_args)
    planet = run_cratons(planet, config, cli_args)
    planet = run_export(planet, config, cli_args)
```

---

## 🧪 Validation
- Run: `python -m generation.generate_planet --radius 25500 --subdivision 6 --output out.planetbin`
- Confirm: logging, mesh generation, cratons, and export succeed

---

## ✅ Conventions and Logging
- Add top-of-file path headers to all new modules
- Add `logger = get_logger(__name__)` to each
- Full docstrings for all functions
- Inline comments per `Status.md` guidelines

---

## ✅ Commit Strategy
Suggested commit message:
```text
Refactor generate_planet into modular CLI and stage pipeline

- Moved CLI arg/config logic to cli/
- Separated per-stage runners into pipeline/
- Minimal entry-point in generate_planet.py
- Preserved CLI behavior and logging setup
```

---

## 📦 Optional Future Enhancements
- Auto-generate config templates from param schemas
- Add pydantic validation for config files
- Implement `--dry-run` or `--print-config`
- Support dynamic stage registration (plugin registry)
- Add `test_argument_parser.py` and `test_run_pipeline.py`
