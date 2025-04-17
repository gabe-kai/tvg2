# generation/pipeline/run_export.py
"""
Pipeline stage: Planet export.
Saves the final planet to disk using the configured output path.
"""

from pathlib import Path
from shared.logging.logger import get_logger
from generation.models.planet import Planet

logger = get_logger(__name__)


def run_export(planet: Planet, output_path: str | None) -> None:
    """
    Export the planet object to disk.

    Args:
        planet (Planet): Planet model to serialize
        output_path (str | None): Path to save .planetbin file. If None, skip export.
    """
    if not output_path:
        logger.info("[Pipeline] No output path provided. Skipping export.")
        return

    logger.info("[Pipeline] Exporting planet to: %s", output_path)

    try:
        planet.save(Path(output_path))
        logger.info("[Pipeline] Planet export complete.")
    except Exception as e:
        logger.error("[Pipeline] Failed to export planet: %s", e)
        raise
