# tests/generation/pipeline/generate_mesh/test_icosphere.py

import numpy as np
import pytest

from generation.models.planet import Planet
from generation.pipeline.generate_mesh import get_strategy


def test_icosphere_mesh_generation():
    planet = Planet(radius=1.0, subdivision_level=2, seed=42)
    strategy = get_strategy("icosphere")
    planet = strategy.run(planet)

    mesh = planet.mesh
    assert mesh is not None, "Mesh should not be None after generation"

    # Check vertex and face shape
    assert isinstance(mesh.vertices, np.ndarray)
    assert isinstance(mesh.faces, np.ndarray)
    assert mesh.vertices.shape[1] == 3, "Vertices should have shape (N, 3)"
    assert mesh.faces.shape[1] == 3, "Faces should have shape (M, 3)"

    # Check all face indices are valid
    num_vertices = mesh.vertices.shape[0]
    assert np.all(mesh.faces < num_vertices), "All face indices must be valid vertex indices"

    # Check adjacency map
    assert isinstance(mesh.adjacency, dict)
    assert len(mesh.adjacency) == mesh.faces.shape[0], "Each face should have an adjacency list"
    for neighbors in mesh.adjacency.values():
        assert isinstance(neighbors, list), "Each adjacency entry should be a list"
        for neighbor in neighbors:
            assert isinstance(neighbor, int), "Adjacent face indices should be integers"
            assert 0 <= neighbor < mesh.faces.shape[0], "Neighbor index out of bounds"


def test_icosphere_minimal_subdivision():
    planet = Planet(radius=1.0, subdivision_level=0, seed=99)
    strategy = get_strategy("icosphere")
    planet = strategy.run(planet)

    mesh = planet.mesh
    assert mesh is not None, "Mesh should be generated even with subdivision_level=0"

    # Expect the base icosahedron: 12 vertices, 20 faces
    assert mesh.vertices.shape == (12, 3), f"Expected 12 vertices, got {mesh.vertices.shape[0]}"
    assert mesh.faces.shape == (20, 3), f"Expected 20 triangular faces, got {mesh.faces.shape[0]}"

    # Adjacency should still be complete
    assert len(mesh.adjacency) == 20, "Each face in base icosahedron should have adjacency entries"
    for neighbors in mesh.adjacency.values():
        assert isinstance(neighbors, list)
        for neighbor in neighbors:
            assert 0 <= neighbor < 20, "Invalid neighbor index in base mesh adjacency"


def test_icosphere_negative_subdivision():
    planet = Planet(radius=1.0, subdivision_level=-1, seed=7)
    strategy = get_strategy("icosphere")
    with pytest.raises(ValueError, match="subdivision_level must be >= 0"):
        strategy.run(planet)


def test_icosphere_zero_radius():
    planet = Planet(radius=0.0, subdivision_level=1, seed=123)
    strategy = get_strategy("icosphere")
    planet = strategy.run(planet)

    mesh = planet.mesh
    assert mesh is not None, "Mesh should be generated even with radius=0"
    assert np.allclose(mesh.vertices, 0), "All vertices should collapse to the origin when radius is 0"
