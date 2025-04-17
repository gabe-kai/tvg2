# generation/cli/argument_parser.py
"""
CLI argument parser for planet generation.
Parses and merges command-line arguments and config file inputs.
"""

import argparse
import json
from pathlib import Path
from typing import Any, Optional, Tuple

from shared.logging.logger import get_logger
from shared.config.planet_gen_config import PlanetGenConfig

logger = get_logger(__name__)


def parse_args(argv: Optional[list[str]] = None) -> Tuple[PlanetGenConfig, Optional[str], Optional[str], dict[str, Any]]:
    """
    Parse CLI arguments and optionally merge with config file.

    Args:
        argv (Optional[list[str]]): Arguments list to parse, or None to use sys.argv

    Returns:
        Tuple[PlanetGenConfig, Optional[str], Optional[str], dict[str, Any]]:
            Planet config, output path, input path, craton argument overrides
    """
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

    args = parser.parse_args(argv)
    cli_dict = vars(args)

    # === Load config file if provided ===
    config_data = {}
    if args.config:
        config_path = Path(args.config)
        if not config_path.is_file():
            raise FileNotFoundError(f"Config file not found: {args.config}")
        try:
            config_data = json.loads(config_path.read_text())
            logger.info("Loaded config from %s", args.config)
        except Exception as e:
            logger.error("Failed to load config file %s: %s", args.config, e)
            raise

    # === Create PlanetGenConfig, override with CLI ===
    config = PlanetGenConfig.from_dict(config_data) if config_data else PlanetGenConfig()

    if args.radius is not None:
        config.radius = args.radius
    if args.subdivision is not None:
        config.subdivision_level = args.subdivision
    if args.seed is not None:
        config.seed = args.seed
    if args.strategy is not None:
        config.mesh_strategy = args.strategy

    # === Build craton args override dict ===
    craton_args = {}
    if args.craton_strategy:
        craton_args["strategy"] = args.craton_strategy
    if args.craton_count is not None:
        craton_args["count"] = args.craton_count
    if args.craton_spacing is not None:
        craton_args["spacing_factor"] = args.craton_spacing

    return config, args.output, args.input, craton_args
