# tests/generation/pipeline/test_run_cratons.py
"""
Unit tests for the craton seeding pipeline stage.
"""

from generation.pipeline.run_cratons import run_cratons
from generation.pipeline.run_mesh import run_mesh
from shared.config.planet_gen_config import PlanetGenConfig
from generation.models.planet import Planet


def test_run_cratons_seeds_cratons():
    config = PlanetGenConfig(radius=6371, subdivision_level=2, seed=42)
    planet = Planet(radius=config.radius, subdivision_level=config.subdivision_level, seed=config.seed)

    # Run mesh first to initialize faces and adjacency
    planet = run_mesh(planet, config, cli_args={})

    cli_args = {"count": 8, "spacing_factor": 1.0, "strategy": "spaced_random"}
    planet = run_cratons(planet, config, cli_args)

    assert planet.cratons is not None
    assert isinstance(planet.cratons, list)
    assert len(planet.cratons) == 8
    for craton in planet.cratons:
        assert hasattr(craton, "center_index")
        assert isinstance(craton.center_index, int)
