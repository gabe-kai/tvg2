# tests/generation/models/test_planet_io.py

import numpy as np
import pytest

from generation.models.planet import Planet
from generation.models.mesh import MeshData


def create_test_planet() -> Planet:
    vertices = np.array([
        [0, 0, 1], [0, 1, 0], [1, 0, 0],
        [0, 0, -1], [0, -1, 0], [-1, 0, 0]
    ], dtype=np.float32)
    faces = np.array([
        [0, 1, 2], [3, 4, 5]
    ], dtype=np.int32)
    adjacency = {
        0: [1],
        1: [0]
    }
    mesh = MeshData(vertices=vertices, faces=faces, adjacency=adjacency)

    return Planet(radius=1000, subdivision_level=1, seed=123, mesh=mesh)


def test_planet_save_and_load(tmp_path):
    original = create_test_planet()
    file_path = tmp_path / "planet_test.planetbin"

    original.save(file_path)
    loaded = Planet.load(file_path)

    assert isinstance(loaded, Planet)
    assert loaded.radius == original.radius
    assert loaded.subdivision_level == original.subdivision_level
    assert loaded.seed == original.seed
    assert loaded.mesh is not None

    np.testing.assert_array_equal(loaded.mesh.vertices, original.mesh.vertices)
    np.testing.assert_array_equal(loaded.mesh.faces, original.mesh.faces)
    assert loaded.mesh.adjacency == original.mesh.adjacency
