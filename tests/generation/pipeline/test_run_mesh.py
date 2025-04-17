# tests/generation/pipeline/test_run_mesh.py
"""
Unit tests for the mesh generation pipeline stage.
"""

from generation.pipeline.run_mesh import run_mesh
from shared.config.planet_gen_config import PlanetGenConfig
from generation.models.planet import Planet


def test_run_mesh_generates_faces():
    config = PlanetGenConfig(radius=5000, subdivision_level=2, seed=123)
    planet = Planet(radius=config.radius, subdivision_level=config.subdivision_level, seed=config.seed)
    cli_args = {}  # no CLI overrides

    planet = run_mesh(planet, config, cli_args)

    assert planet.mesh is not None
    assert hasattr(planet.mesh, "faces")
    import numpy as np
    assert isinstance(planet.mesh.faces, (list, np.ndarray))
    assert len(planet.mesh.faces) > 0
