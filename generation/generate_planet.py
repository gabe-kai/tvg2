# generation/generate_planet.py

import argparse
import json
from pathlib import Path

from generation.models.planet import Planet
from generation.pipeline.generate_mesh import get_strategy as get_mesh_strategy
from generation.pipeline.export_planet import get_strategy as get_export_strategy
from generation.pipeline.seed_cratons import get_strategy as get_craton_strategy
from shared.config.planet_gen_config import PlanetGenConfig

from shared.logging.logger import get_logger
log = get_logger(__name__)


def parse_args() -> tuple[PlanetGenConfig, str, str, dict]:
    parser = argparse.ArgumentParser(description="Generate a procedural planet.")

    # === IO CLI Support ===
    parser.add_argument("--config", type=str, help="Path to JSON config file")
    parser.add_argument("--output", type=str, help="Output file path for .planetbin export")
    parser.add_argument("--input", type=str, help="Path to existing .planetbin file to load instead of generating")

    # === Mesh Generation CLI Support ===
    parser.add_argument("--radius", type=float, help="Planet radius in kilometers")
    parser.add_argument("--subdivision", type=int, help="Mesh subdivision level")
    parser.add_argument("--seed", type=int, help="Random seed for deterministic generation")
    parser.add_argument("--strategy", type=str, help="Mesh generation strategy")

    # === Craton Seeding CLI Support ===
    parser.add_argument("--craton_strategy", type=str, help="Craton seeding strategy (e.g. spaced_random)")
    parser.add_argument("--craton_count", type=int, help="Number of cratons to seed")
    parser.add_argument("--craton_spacing", type=float, help="Spacing factor between cratons")

    args = parser.parse_args()

    config = PlanetGenConfig()  # Start with defaults
    craton_args = {}

    if args.config:
        path = Path(args.config)
        if not path.is_file():
            raise FileNotFoundError(f"Config file not found: {args.config}")
        with path.open("r", encoding="utf-8") as f:
            raw_data = json.load(f)
            config = PlanetGenConfig.from_dict(raw_data)
            config.raw = raw_data
        log.info("Loaded config from %s", args.config)

    # Override with CLI args if provided
    if args.radius is not None:
        config.radius = args.radius
    if args.subdivision is not None:
        config.subdivision_level = args.subdivision
    if args.seed is not None:
        config.seed = args.seed
    if args.strategy is not None:
        config.mesh_strategy = args.strategy

    if args.craton_strategy:
        craton_args["strategy"] = args.craton_strategy
    if args.craton_count is not None:
        craton_args["count"] = args.craton_count
    if args.craton_spacing is not None:
        craton_args["spacing_factor"] = args.craton_spacing

    return config, args.output, args.input, craton_args


def main():
    config, output_path, input_path, craton_args = parse_args()

    # Load from .planetbin if requested
    if input_path:
        log.info("Loading planet from file: %s", input_path)
        planet = Planet.load(input_path)
        log.info("Planet loaded: %s", planet.summary())
        return  # Skip generation if loading

    # Create new planet
    planet = Planet(
        radius=config.radius,
        subdivision_level=config.subdivision_level,
        seed=config.seed,
    )
    log.info("Initialized planet: %s", planet.summary())

    # Run mesh generation stage
    mesh_strategy = get_mesh_strategy(config.mesh_strategy)
    planet = mesh_strategy.run(planet)
    log.info("Planet after mesh generation:\n%s", planet.summary())

    # Run craton seeding stage
    strategy_name = craton_args.get("strategy") \
        or (config.raw.get("craton_seeding", {}).get("strategy") if hasattr(config, "raw") else None) \
        or "spaced_random"

    config_block = config.raw.get("craton_seeding", {}) if hasattr(config, "raw") else {}
    kwargs = {**config_block, **craton_args}
    kwargs.pop("strategy", None)

    craton_strategy = get_craton_strategy(strategy_name, **kwargs)
    planet = craton_strategy.run(planet)
    log.info("Planet after craton seeding:\n%s", planet.summary())

    # Export to .planetbin if requested
    if output_path:
        exporter = get_export_strategy("hdf5", output_path=output_path)
        planet = exporter.run(planet)


if __name__ == "__main__":
    main()


# === Example Command-Line Usage ===
# Run with all default values:
# python -m generation.generate_planet

# Run with custom radius and seed:
# python -m generation.generate_planet --radius 5000 --seed 99

# Run with a specific subdivision level and mesh strategy:
# python -m generation.generate_planet --subdivision 4 --strategy icosphere

# Run using a config file:
# python -m generation.generate_planet --config config/earthlike_default.json

# Run using config file, but override subdivision level:
# python -m generation.generate_planet --config config/earthlike_default.json --subdivision 3

# Run and export to file:
# python -m generation.generate_planet --config config/earthlike_default.json --subdivision 3 --output testplanet.planetbin

# Load and print summary from file:
# python -m generation.generate_planet --input testplanet.planetbin

# Run with craton seeding via CLI (not the config file):
# python -m generation.generate_planet --craton_strategy spaced_random --craton_count 10 --craton_spacing 1.2 --output testplanet.planetbin
