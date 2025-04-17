# generation/generate_planet.py
"""
CLI entry point for procedural planet generation.
Delegates to pipeline stages: mesh, cratons, export.
"""

from generation.models.planet import Planet
from shared.logging.logger import get_logger
from generation.cli.argument_parser import parse_args
from generation.pipeline.run_mesh import run_mesh
from generation.pipeline.run_cratons import run_cratons
from generation.pipeline.run_export import run_export

logger = get_logger(__name__)


def main():
    config, output_path, input_path, cli_args = parse_args()

    if input_path:
        logger.info("Loading planet from file: %s", input_path)
        planet = Planet.load(input_path)
        logger.info("Planet loaded: %s", planet.summary())
    else:
        planet = Planet(
            radius=config.radius,
            subdivision_level=config.subdivision_level,
            seed=config.seed,
        )
        logger.info("Initialized new planet: %s", planet.summary())

        planet = run_mesh(planet, config, cli_args)
        logger.info("Planet after mesh generation:\n%s", planet.summary())

        planet = run_cratons(planet, config, cli_args)
        logger.info("Planet after craton seeding:\n%s", planet.summary())

    run_export(planet, output_path)


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
