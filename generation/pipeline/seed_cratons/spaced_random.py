# generation/pipeline/seed_cratons/spaced_random.py

"""
Craton seeding strategy that selects random seed faces with minimum spacing between them.
Prevents adjacent cratons and encourages natural distribution.
"""

import math
import random
from generation.models.tectonics import Craton
from generation.models.planet import Planet
from .base import SeedCratonsStrategy
from shared.logging.logger import get_logger

log = get_logger(__name__)

class SpacedRandomCratonSeeder(SeedCratonsStrategy):
    def __init__(self, count: int = None, min_distance: int = None, spacing_factor: float = 1.0):
        """
        Args:
            count (int, optional): Number of cratons to seed. If None, calculated based on planet radius.
            min_distance (int, optional): Fixed minimum adjacency distance between cratons. If None, computed dynamically.
            spacing_factor (float): Scaling factor to adjust computed spacing (used only if min_distance is None).
        """
        self.count = count
        self.min_distance = min_distance
        self.spacing_factor = spacing_factor

    def run(self, planet: Planet) -> Planet:
        mesh = planet.mesh
        adjacency = mesh.adjacency  # dict[int, list[int]]
        num_faces = len(mesh.faces)

        # Estimate craton count from surface area if not specified
        if self.count is None:
            EARTH_RADIUS = 6371  # in kilometers
            EARTH_SURFACE_AREA = 4 * math.pi * EARTH_RADIUS ** 2
            planet_surface_area = 4 * math.pi * planet.radius ** 2
            base_plate_count = 10
            self.count = round(base_plate_count * (planet_surface_area / EARTH_SURFACE_AREA))
            self.count = max(4, min(self.count, 50))  # Clamp to reasonable bounds

            log.debug("Computed craton count from surface area:")
            log.debug("    Planet radius: %.2f km", planet.radius)
            log.debug("    Planet surface area: %.2f", planet_surface_area)
            log.debug("    Earth surface area: %.2f", EARTH_SURFACE_AREA)
            log.debug("    Raw craton estimate: %.2f", base_plate_count * (planet_surface_area / EARTH_SURFACE_AREA))
            log.debug("    Final craton count: %d", self.count)

        log.info("[Craton Seeding] Starting spaced random seeding...")
        log.debug("Mesh has %d faces. Targeting %d cratons.", num_faces, self.count)

        # Compute spacing dynamically if not provided
        if self.min_distance is None:
            est_distance = (num_faces / self.count) ** 0.5
            self.min_distance = max(1, int(est_distance * self.spacing_factor))
            log.debug("Computed dynamic min_distance:")
            log.debug("    Num faces: %d", num_faces)
            log.debug("    Est base distance: %.2f", est_distance)
            log.debug("    Spacing factor: %.2f", self.spacing_factor)
            log.debug("    Final min_distance: %d", self.min_distance)
        else:
            log.debug("Using fixed min_distance: %d", self.min_distance)

        selected = []
        attempts = 0
        max_attempts = num_faces * 5

        # Initialize candidate mask (True = valid, False = within exclusion range)
        valid_faces = set(range(num_faces))

        def mask_neighbors(face_index: int):
            queue = [(face_index, 0)]
            visited = set()
            while queue:
                current, dist = queue.pop(0)
                if current in visited or dist > self.min_distance:
                    continue
                visited.add(current)
                valid_faces.discard(current)
                for neighbor in adjacency[current]:
                    if neighbor not in visited:
                        queue.append((neighbor, dist + 1))

        while len(selected) < self.count and attempts < max_attempts:
            if not valid_faces:
                break
            candidate = random.choice(list(valid_faces))
            selected.append(candidate)
            mask_neighbors(candidate)
            log.debug("Selected craton %d at face %d", len(selected) - 1, candidate)
            attempts += 1
            if attempts % 1000 == 0:
                log.debug("Tried %d candidates so far... %d accepted.", attempts, len(selected))

        if len(selected) < self.count:
            log.warning("Only %d cratons placed out of requested %d after %d attempts.",
                        len(selected), self.count, attempts)
        else:
            log.info("Successfully placed %d cratons in %d attempts.", len(selected), attempts)

        planet.cratons = [
            Craton(id=i, center_index=face_id)
            for i, face_id in enumerate(selected)
        ]
        return planet

    def _face_distance_ok(self, f1: int, f2: int, adjacency: dict[int, list[int]]) -> bool:
        """
        Check that two faces are not within the restricted adjacency range.

        Args:
            f1 (int): First face index
            f2 (int): Second face index
            adjacency (dict[int, list[int]]): Face adjacency map

        Returns:
            bool: True if the faces are at least `min_distance` apart
        """
        if f1 == f2:
            return False

        frontier = [f1]
        visited = set()
        depth = 0

        while frontier and depth < self.min_distance:
            next_frontier = []
            for f in frontier:
                visited.add(f)
                for neighbor in adjacency[f]:
                    if neighbor == f2:
                        return False
                    if neighbor not in visited:
                        next_frontier.append(neighbor)
            frontier = next_frontier
            depth += 1

        return True
