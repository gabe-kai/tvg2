# generation/pipeline/run_cratons.py
"""
Pipeline stage: Craton seeding.
Applies configured craton strategy to generate tectonic seed regions.
"""

from generation.models.planet import Planet
from shared.logging.logger import get_logger
from generation.cli.parameter_merge import resolve_stage_params
from generation.cli.constants import CRATON_PARAMS
from generation.pipeline.seed_cratons import get_strategy

logger = get_logger(__name__)


def run_cratons(planet: Planet, config, cli_args: dict) -> Planet:
    """
    Seed tectonic cratons using the configured seeding strategy.

    Args:
        planet (Planet): The planet model to update
        config (PlanetGenConfig): Configuration object
        cli_args (dict): CLI argument overrides

    Returns:
        Planet: Updated planet with seeded cratons
    """
    logger.info("[Pipeline] Running craton seeding stage...")

    params = resolve_stage_params("craton_seeding", CRATON_PARAMS, cli_args, config)
    strategy_name = params.pop("strategy")
    logger.debug("Using craton strategy: %s", strategy_name)

    strategy = get_strategy(strategy_name, **params)
    planet = strategy.run(planet)

    logger.info("[Pipeline] Craton seeding complete. Seeded %d cratons.", len(planet.cratons))
    return planet
