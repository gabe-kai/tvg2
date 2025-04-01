# generation/generate_planet.py

import argparse
import json
from pathlib import Path

from generation.models.planet import Planet
from generation.pipeline.generate_mesh import get_strategy
from shared.config.planet_gen_config import PlanetGenConfig
from shared.logging.logger import get_logger

log = get_logger(__name__)


def parse_args() -> PlanetGenConfig:
    parser = argparse.ArgumentParser(description="Generate a procedural planet.")
    parser.add_argument("--config", type=str, help="Path to JSON config file")
    parser.add_argument("--radius", type=float, help="Planet radius in kilometers")
    parser.add_argument("--subdivision", type=int, help="Mesh subdivision level")
    parser.add_argument("--seed", type=int, help="Random seed for deterministic generation")
    parser.add_argument("--strategy", type=str, help="Mesh generation strategy")
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

    return config


def main():
    config = parse_args()

    # Create planet object
    planet = Planet(
        radius=config.radius,
        subdivision_level=config.subdivision_level,
        seed=config.seed,
    )
    log.info("Initialized planet: %s", planet.summary())

    # Run mesh generation stage
    mesh_strategy = get_strategy(config.mesh_strategy)
    planet = mesh_strategy.run(planet)

    # Show summary after mesh stage
    log.info("Planet after mesh generation:\n%s", planet.summary())


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
