# tests/generation/pipeline/seed_cratons/test_spaced_random.py

import pytest
from generation.pipeline.seed_cratons.spaced_random import SpacedRandomCratonSeeder
from generation.models.planet import Planet
from generation.pipeline.generate_mesh.icosphere import IcosphereMeshStrategy

# Utility: create a basic planet with a small mesh for test purposes
def make_test_planet(subdivision: int = 3, seed: int = 42) -> Planet:
    planet = Planet(radius=6371.0, subdivision_level=subdivision, seed=seed)
    mesh_strategy = IcosphereMeshStrategy()
    return mesh_strategy.run(planet)

def bfs_distance(a: int, b: int, adjacency: dict[int, list[int]]) -> int:
    """Compute shortest face-to-face path distance using BFS."""
    frontier = [a]
    visited = set()
    depth = 0
    while frontier:
        next_frontier = []
        for f in frontier:
            if f == b:
                return depth
            visited.add(f)
            for neighbor in adjacency[f]:
                if neighbor not in visited:
                    next_frontier.append(neighbor)
        frontier = next_frontier
        depth += 1
    return -1  # unreachable

# === Tests ===

def test_craton_count_matches():
    planet = make_test_planet()
    strategy = SpacedRandomCratonSeeder(count=5, min_distance=2)
    planet = strategy.run(planet)
    assert len(planet.cratons) == 5

def test_cratons_are_spaced():
    planet = make_test_planet()
    min_dist = 3
    strategy = SpacedRandomCratonSeeder(count=6, min_distance=min_dist)
    planet = strategy.run(planet)
    ids = [c.center_index for c in planet.cratons]
    for i, a in enumerate(ids):
        for b in ids[i+1:]:
            dist = bfs_distance(a, b, planet.mesh.adjacency)
            assert dist >= min_dist, f"Cratons {a} and {b} are too close (dist={dist})"

def test_craton_strategy_handles_dense_spacing():
    planet = make_test_planet()
    strategy = SpacedRandomCratonSeeder(count=30, min_distance=10)
    planet = strategy.run(planet)
    assert len(planet.cratons) <= 30  # should not crash, may not reach target count
