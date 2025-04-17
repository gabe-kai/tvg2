# generation/pipeline/run_mesh.py
"""
Pipeline stage: Mesh generation.
Applies mesh strategy to initialize or replace the planet's mesh.
"""

from generation.models.planet import Planet
from shared.logging.logger import get_logger
from generation.cli.parameter_merge import resolve_stage_params
from generation.cli.constants import MESH_PARAMS
from generation.pipeline.generate_mesh import get_strategy

logger = get_logger(__name__)


def run_mesh(planet: Planet, config, cli_args: dict) -> Planet:
    """
    Generate a planetary mesh using the configured mesh strategy.

    Args:
        planet (Planet): The planet model to update
        config (PlanetGenConfig): Configuration object
        cli_args (dict): CLI argument overrides

    Returns:
        Planet: Updated planet with generated mesh
    """
    logger.info("[Pipeline] Running mesh generation stage...")

    params = resolve_stage_params("mesh", MESH_PARAMS, cli_args, config)
    strategy_name = params.pop("strategy")
    logger.debug("Using mesh strategy: %s", strategy_name)

    strategy = get_strategy(strategy_name)
    planet = strategy.run(planet)

    logger.info("[Pipeline] Mesh generation complete.")
    return planet
