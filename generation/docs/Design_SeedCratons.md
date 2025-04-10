# Design: Craton Seeding Pipeline (`SeedCratons`)

This document outlines the design and implementation plan for the `SeedCratons` stage in the planet generation pipeline. Craton seeding represents a foundational geological step for forming stable landmasses, which may influence tectonics, elevation, resource placement, and early civilization patterns.

---

## 🚀 Git Branch
Create a new feature branch from `main`:
```bash
git checkout -b feature/seed-cratons
```

---

## 📁 Folder & File Layout
Under `generation/pipeline/seed_cratons/`:
```
seed_cratons/
├── __init__.py              # Strategy loader
├── base.py                  # Abstract base class: SeedCratonsStrategy
├── spaced_random.py         # First implementation with minimum distance enforcement
```

Tests:
```
tests/generation/seed_cratons/
├── test_spaced_random.py
```

Overlay:
```
ui/tools/mesh_viewer/overlays/
├── craton_overlay.py
```

Register in:
```
ui/tools/mesh_viewer/overlays/__init__.py
```

---

## 🧱 Step 1: Craton Data Model
Cratons are defined in `generation/models/tectonics.py`:
```python
@dataclass
class Craton:
    center_index: int   # seed face index
    id: int             # unique ID
```

If needed for overlays or expansion algorithms, this class may be extended with:
```python
    face_ids: list[int]     # optional: tracked face region
    name: str               # optional: overlay label
```

These will be stored in `planet.cratons: list[Craton]`

---

## ⚙️ Step 2: Base Strategy Class
```python
# base.py
class SeedCratonsStrategy(ABC):
    @abstractmethod
    def run(self, planet: Planet) -> Planet:
        pass
```

---

## 🎲 Step 3: Spaced Random Implementation
We avoid placing cratons directly adjacent to one another by enforcing a minimum spacing rule.
This prevents clumping and mirrors the real-world distribution of isolated, ancient cratonic zones.

```python
# spaced_random.py
from generation.models.tectonics import Craton

class SpacedRandomCratonSeeder(SeedCratonsStrategy):
    def __init__(self, count: int = 10, min_distance: int = 3):
        self.count = count
        self.min_distance = min_distance

    def run(self, planet: Planet) -> Planet:
        mesh = planet.mesh
        selected = []
        used = set()

        while len(selected) < self.count:
            candidate = random.randint(0, len(mesh.faces) - 1)
            if all(self._face_distance_ok(candidate, other, mesh.adjacency) for other in selected):
                selected.append(candidate)

        planet.cratons = [
            Craton(id=i, center_index=face_id)
            for i, face_id in enumerate(selected)
        ]
        return planet

    def _face_distance_ok(self, f1, f2, adjacency):
        # Simple BFS up to min_distance to check if f2 is reachable from f1
        if f1 == f2:
            return False
        frontier = [f1]
        visited = set()
        depth = 0
        while frontier and depth < self.min_distance:
            next_frontier = []
            for f in frontier:
                visited.add(f)
                for neighbor in adjacency.get(f, []):
                    if neighbor == f2:
                        return False
                    if neighbor not in visited:
                        next_frontier.append(neighbor)
            frontier = next_frontier
            depth += 1
        return True
```

---

## 👁️ Step 4: Craton Viewer Overlay
```python
# craton_overlay.py
class CratonOverlay(Overlay):
    def get_name(self): return "Cratons"
    def get_category(self): return "Geology"
    def get_description(self): return "Displays seeded craton regions."

    def update_data(self, mesh_data: MeshRenderData):
        self.face_map = {c.center_index: c.id for c in mesh_data.planet.cratons}

    def render(self, gl_widget):
        # Use face_map to color mesh faces
        pass
```

Update `__init__.py` to include:
```python
from .craton_overlay import CratonOverlay
ALL_OVERLAYS.append(CratonOverlay)
```

---

## 🧪 Step 5: Unit Tests
```python
# test_spaced_random.py
def test_cratons_are_spaced():
    planet = make_test_planet()
    strategy = SpacedRandomCratonSeeder(count=5, min_distance=3)
    planet = strategy.run(planet)
    ids = [c.center_index for c in planet.cratons]
    for i, a in enumerate(ids):
        for b in ids[i+1:]:
            assert bfs_face_distance(a, b, planet.mesh.adjacency) >= 3
```
Add tests for:
- Seed count
- Minimum spacing
- Edge cases (too many cratons for spacing constraint)

---

## 📥 Step 6: Integration into Planet Pipeline
In `generation/pipeline/generate_planet.py`:
```python
from generation.pipeline.seed_cratons import get_strategy
...
planet = get_strategy("spaced_random").run(planet)
```

---

## ✅ Final Checklist
- [ ] Branch created
- [ ] File structure added
- [ ] Strategy base + spaced random impl complete
- [ ] Craton data stored in Planet
- [ ] Overlay registered and visible
- [ ] Unit tests passing
- [ ] Pipeline integration tested

---

Ready to begin!
