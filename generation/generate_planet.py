# generation/generate_planet.py

import argparse
import json
from pathlib import Path

from generation.models.planet import Planet
from generation.pipeline.generate_mesh import get_strategy as get_mesh_strategy
from generation.pipeline.export_planet import get_strategy as get_export_strategy
from shared.config.planet_gen_config import PlanetGenConfig
from shared.logging.logger import get_logger

log = get_logger(__name__)


def parse_args() -> tuple[PlanetGenConfig, str, str]:
    parser = argparse.ArgumentParser(description="Generate a procedural planet.")
    parser.add_argument("--config", type=str, help="Path to JSON config file")
    parser.add_argument("--radius", type=float, help="Planet radius in kilometers")
    parser.add_argument("--subdivision", type=int, help="Mesh subdivision level")
    parser.add_argument("--seed", type=int, help="Random seed for deterministic generation")
    parser.add_argument("--strategy", type=str, help="Mesh generation strategy")
    parser.add_argument("--output", type=str, help="Output file path for .planetbin export")
    parser.add_argument("--input", type=str, help="Path to existing .planetbin file to load instead of generating")
    args = parser.parse_args()

    config = PlanetGenConfig()  # Start with defaults

    if args.config:
        path = Path(args.config)
        if not path.is_file():
            raise FileNotFoundError(f"Config file not found: {args.config}")
        with path.open("r", encoding="utf-8") as f:
            config = PlanetGenConfig.from_dict(json.load(f))
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

    return config, args.output, args.input


def main():
    config, output_path, input_path = parse_args()

    # Load from .planetbin if requested
    if input_path:
        log.info("Loading planet from file: %s", input_path)
        planet = Planet.load(input_path)
        log.info("Planet loaded: %s", planet.summary())
        return  # Skip generation if loading
    else:
        # Create planet object
        planet = Planet(
        radius=config.radius,
        subdivision_level=config.subdivision_level,
        seed=config.seed,
    )
    log.info("Initialized planet: %s", planet.summary())

    # Run mesh generation stage
    if not input_path:
        mesh_strategy = get_mesh_strategy(config.mesh_strategy)
        planet = mesh_strategy.run(planet)

    # Show summary after mesh stage
    log.info("Planet after mesh generation:\n%s", planet.summary())

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
# python -m generation.generate_planet --output planet_output.planetbin

# Load and print summary from file:
# python -m generation.generate_planet --input planet_output.planetbin
