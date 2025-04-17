# generation/pipeline/generate_mesh/icosphere.py

"""
Icosphere mesh generator.

This module defines a mesh generation strategy based on subdividing an icosahedron to form an icosphere,
which is then smoothed to reduce geometric distortion around the 12 original vertices (with degree 5 adjacency).

The strategy includes vertex normalization, midpoint caching, face adjacency mapping, and optional
Laplacian-style smoothing constrained to the surface of the sphere.
"""

import numpy as np

from generation.models.mesh import MeshData
from generation.models.planet import Planet
from shared.logging.logger import get_logger
from .base import BaseMeshStrategy

log = get_logger(__name__)


def normalize(vectors: np.ndarray) -> np.ndarray:
    """Normalize each vector (row) to unit length."""
    lengths = np.linalg.norm(vectors, axis=1, keepdims=True)
    return vectors / lengths


def midpoint(v1: np.ndarray, v2: np.ndarray) -> np.ndarray:
    """Compute the midpoint between two 3D points."""
    return (v1 + v2) / 2.0


class IcosphereMeshStrategy(BaseMeshStrategy):
    """
    Mesh generation strategy that builds an icosphere by recursively subdividing an icosahedron.
    Includes optional spherical Laplacian smoothing to even out vertex spacing.
    """

    def run(self, planet: Planet) -> Planet:
        """
        Generate and assign a spherical mesh to the given planet.

        Args:
            planet (Planet): The target planet to attach mesh data to.

        Returns:
            Planet: The planet with updated mesh data.
        """
        if planet.subdivision_level < 0:
            raise ValueError("subdivision_level must be >= 0")
        log.info("Generating icosphere mesh (subdivisions=%d)...", planet.subdivision_level)

        # Initialize from base icosahedron
        vertices, faces = self._create_icosahedron()

        # Perform recursive subdivisions
        for i in range(planet.subdivision_level):
            vertices, faces = self._subdivide(vertices, faces)
            log.debug("Subdivision %d complete: %d vertices, %d faces", i + 1, len(vertices), len(faces))

        # Project all vertices onto the sphere of given radius
        if planet.radius == 0.0:
            vertices[:] = 0.0
        else:
            vertices = normalize(vertices) * planet.radius

        # Smooth vertex positions to reduce local distortion
        if planet.radius != 0.0:
            vertices = self._relax_vertices(vertices, faces, iterations=10, radius=planet.radius)

        # Build face adjacency (used for mesh navigation, not smoothing)
        adjacency = self._build_adjacency(faces)

        face_ids = np.arange(faces.shape[0], dtype=np.int32)

        # Compute geometric centroid of each triangular face
        face_centers = vertices[faces].mean(axis=1)
        log.debug("Computed %d face centroids", len(face_centers))

        planet.mesh = MeshData(vertices=vertices, faces=faces, adjacency=adjacency, face_ids=face_ids, face_centers=face_centers)

        log.info("Icosphere mesh generation complete. Total vertices: %d, faces: %d", len(vertices), len(faces))
        return planet

    @staticmethod
    def _create_icosahedron():
        """
        Generate the 12 vertices and 20 triangular faces of a base icosahedron.

        Returns:
            (np.ndarray, np.ndarray): Tuple of (vertices, faces)
        """
        t = (1.0 + np.sqrt(5.0)) / 2.0

        raw_vertices = [
            [-1,  t,  0], [ 1,  t,  0], [-1, -t,  0], [ 1, -t,  0],
            [ 0, -1,  t], [ 0,  1,  t], [ 0, -1, -t], [ 0,  1, -t],
            [ t,  0, -1], [ t,  0,  1], [-t,  0, -1], [-t,  0,  1],
        ]

        raw_faces = [
            [0, 11, 5], [0, 5, 1], [0, 1, 7], [0, 7, 10], [0, 10, 11],
            [1, 5, 9], [5, 11, 4], [11, 10, 2], [10, 7, 6], [7, 1, 8],
            [3, 9, 4], [3, 4, 2], [3, 2, 6], [3, 6, 8], [3, 8, 9],
            [4, 9, 5], [2, 4, 11], [6, 2, 10], [8, 6, 7], [9, 8, 1],
        ]

        return np.array(raw_vertices, dtype=float), np.array(raw_faces, dtype=int)

    @staticmethod
    def _subdivide(vertices: np.ndarray, faces: np.ndarray):
        """
        Subdivide each triangle face into 4 smaller triangles by inserting midpoints.

        Caches midpoints to avoid duplication and normalizes new points onto the unit sphere.

        Args:
            vertices (np.ndarray): Original vertex array.
            faces (np.ndarray): Original face index array.

        Returns:
            (np.ndarray, np.ndarray): Updated (vertices, faces)
        """
        vertex_cache = {}
        new_faces = []

        # Keep original vertices; accumulate new ones in a separate list
        vertices = vertices.copy()
        new_vertices = []

        def get_midpoint_index(v1_idx, v2_idx):
            # Ensure each midpoint is only computed once
            key = tuple(sorted((v1_idx, v2_idx)))
            if key in vertex_cache:
                return vertex_cache[key]

            midpoint_coords = midpoint(vertices[v1_idx], vertices[v2_idx])
            midpoint_coords /= np.linalg.norm(midpoint_coords)

            new_idx = len(vertices) + len(new_vertices)
            new_vertices.append(midpoint_coords)
            vertex_cache[key] = new_idx
            return new_idx

        for tri in faces:
            v1, v2, v3 = tri
            a = get_midpoint_index(v1, v2)
            b = get_midpoint_index(v2, v3)
            c = get_midpoint_index(v3, v1)

            # Replace original triangle with 4 smaller ones
            new_faces.extend([
                [v1, a, c],
                [v2, b, a],
                [v3, c, b],
                [a, b, c],
            ])

        # Concatenate original and new vertices
        vertices = np.vstack([vertices, np.array(new_vertices)])
        return vertices, np.array(new_faces, dtype=int)

    @staticmethod
    def _build_adjacency(faces: np.ndarray):
        """
        Build a mapping from each face to its neighboring faces (sharing an edge).

        Args:
            faces (np.ndarray): Face index array.

        Returns:
            dict: Mapping from face index to list of adjacent face indices.
        """
        adjacency = {i: set() for i in range(len(faces))}
        edge_to_faces = {}

        for i, face in enumerate(faces):
            # Each face contributes 3 edges
            edges = [
                tuple(sorted((face[0], face[1]))),
                tuple(sorted((face[1], face[2]))),
                tuple(sorted((face[2], face[0]))),
            ]
            for edge in edges:
                if edge in edge_to_faces:
                    for neighbor_face in edge_to_faces[edge]:
                        adjacency[i].add(neighbor_face)
                        adjacency[neighbor_face].add(i)
                    edge_to_faces[edge].append(i)
                else:
                    edge_to_faces[edge] = [i]

        return {k: list(v) for k, v in adjacency.items()}

    @staticmethod
    def _relax_vertices(vertices: np.ndarray, faces: np.ndarray, iterations: int = 5, radius: float = 1.0) -> np.ndarray:
        """
        Apply Laplacian-like smoothing to reduce vertex distortion.

        Each vertex is moved slightly toward the average of its neighbors and reprojected onto the sphere.

        Args:
            vertices (np.ndarray): Array of vertex positions.
            faces (np.ndarray): Array of triangle indices.
            iterations (int): Number of smoothing passes to apply.
            radius (float): Radius of the output sphere.

        Returns:
            np.ndarray: Smoothed vertex array.
        """
        from collections import defaultdict

        # Build vertex adjacency map (undirected graph of neighbors)
        neighbors = defaultdict(set)
        for tri in faces:
            for i in range(3):
                v1, v2 = tri[i], tri[(i + 1) % 3]
                neighbors[v1].add(v2)
                neighbors[v2].add(v1)

        vertices = vertices.copy()
        for _ in range(iterations):
            new_vertices = vertices.copy()
            for i in range(len(vertices)):
                if not neighbors[i]:
                    continue
                # Compute average of neighbor positions
                avg = np.mean([vertices[j] for j in neighbors[i]], axis=0)
                # Reproject to sphere surface
                avg_direction = avg / np.linalg.norm(avg)
                new_vertices[i] = avg_direction * radius
            vertices = new_vertices

        return vertices
