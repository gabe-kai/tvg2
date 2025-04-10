# Refactor Plan: Modularize `generate_planet.py` CLI and Pipeline Logic

## 🧠 Motivation

The `generate_planet.py` file currently mixes CLI parsing, parameter merging, planet creation, and pipeline orchestration. As feature complexity increases (e.g. craton seeding, elevation, climate), this structure becomes harder to maintain.

---

## 🧩 Goals

- Separate CLI parsing from pipeline logic
- Separate parameter merging from core logic
- Ensure CLI and config parameters stay in sync
- Prepare for scalable, stage-based config handling

---

## 🗂️ New File Structure

```
generation/
├── generate_planet.py              ← Main entry point (orchestrates)
├── cli/
│   ├── argument_parser.py          ← Defines all CLI arguments
│   ├── parameter_merge.py          ← Merges CLI + config for each stage
│   └── constants.py                ← Parameter schemas / stage keys
└── pipeline/
    ├── run_mesh.py                 ← Mesh generation stage
    ├── run_cratons.py              ← Craton seeding stage
    └── run_export.py               ← Export stage
```

---

## 📜 Task Breakdown

### ✅ 1. Move CLI logic to `cli/argument_parser.py`

- Extract all `argparse.ArgumentParser` setup and parsing into a function:
  ```python
  def parse_args() -> tuple[PlanetGenConfig, dict[str, Any]]:
  ```

- Return `config` and `cli_args` (clean dict of user input)

---

### ✅ 2. Create `cli/constants.py`

- Define reusable schemas per stage:
  ```python
  CRATON_PARAMS = {
      "strategy": {"type": str, "default": "spaced_random"},
      "count": {"type": int, "default": 8},
      "spacing_factor": {"type": float, "default": 1.0}
  }
  ```

- Used for:
  - Auto-generating CLI arguments
  - Applying consistent defaults
  - Logging user-visible parameter resolution

---

### ✅ 3. Create `cli/parameter_merge.py`

- Implement:
  ```python
  def resolve_stage_params(stage_key: str, schema: dict, cli_args: dict, config: PlanetGenConfig) -> dict
  ```

- This merges:
  - CLI → config → schema defaults
  - Ignores unrelated keys
  - Optionally logs resolved values for debugging

---

### ✅ 4. Move each pipeline step to its own file

Example: `pipeline/run_cratons.py`

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

### ✅ 5. Update `generate_planet.py` to delegate

New version becomes a clean pipeline controller:

```python
def main():
    config, cli_args = parse_args()
    planet = Planet(...)

    planet = run_mesh(planet, config, cli_args)
    planet = run_cratons(planet, config, cli_args)
    planet = run_export(planet, config, cli_args)
```

---

## 📦 Optional Future Enhancements

- Auto-generate config file templates from param schemas
- Validate config values with `pydantic` or a typed wrapper
- Implement `--dry-run` and `--print-config` support
- Add dynamic pipeline steps from plugin registry

---

## ✅ Done When

- `generate_planet.py` is <100 lines and mostly glue
- CLI and config param sync is unified
- Stage-specific logic is cleanly separated and testable
