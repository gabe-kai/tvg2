# generation/cli/parameter_merge.py
"""
Merges CLI and config parameters for a given pipeline stage.
Resolves final values using schema defaults and type enforcement.
"""

from typing import Any, Dict
from shared.logging.logger import get_logger
from shared.config.planet_gen_config import PlanetGenConfig

logger = get_logger(__name__)


def resolve_stage_params(stage_key: str, schema: dict, cli_args: dict[str, Any], config: PlanetGenConfig) -> dict[str, Any]:
    """
    Merge config-stage parameters with CLI overrides and schema defaults.

    Args:
        stage_key (str): Key for the stage section in config (e.g., "craton_seeding")
        schema (dict): Parameter schema with 'type' and 'default' entries
        cli_args (dict): Parsed CLI arguments
        config (PlanetGenConfig): Main config object

    Returns:
        dict[str, Any]: Final parameter set for the stage
    """
    config_block = getattr(config, stage_key, {}) or {}
    resolved = {}

    for param_key, param_info in schema.items():
        expected_type = param_info["type"]
        default_value = param_info.get("default")

        value = cli_args.get(param_key)
        if value is None:
            value = config_block.get(param_key)
        if value is None:
            value = default_value

        if value is not None and not isinstance(value, expected_type):
            try:
                value = expected_type(value)
                logger.debug("Coerced '%s' to %s via %s", param_key, value, expected_type.__name__)
            except Exception as e:
                logger.warning("Could not coerce '%s' to %s: %s", param_key, expected_type.__name__, e)

        resolved[param_key] = value

    logger.debug("Resolved parameters for stage '%s': %s", stage_key, resolved)
    return resolved
