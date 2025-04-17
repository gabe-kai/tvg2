# Refactor Plan – generate_mesh to Calculate and Store Face Centroids

This refactor plan formalizes the calculation and inclusion of face centroids as part of the mesh generation pipeline.
Although the centroid logic is already implemented within the `IcosphereMeshStrategy`, this plan ensures it is:
- Clearly treated as a required output of the mesh stage
- Properly integrated with all downstream save/load operations
- Easily accessible for later overlay and tectonic processing

---

## ✅ Objective
Ensure every generated mesh includes `face_centers` (i.e., geometric centroids of all faces) and that they are saved, loaded, and summarized as part of the `Planet` object.

---

## 🔧 Implementation Steps

### 1. **Formalize `face_centers` Calculation in Strategy**
- [x] Confirm that `vertices[faces].mean(axis=1)` correctly computes centroids
- [x] Add clarifying comment: `# Compute geometric centroid of each triangular face`
- [x] Add debug log line to confirm number of centroids generated

### 2. **Store `face_centers` in MeshData**
- [x] Ensure `face_centers` is passed into the `MeshData` constructor
- [x] Confirm that its type and usage are consistent with existing mesh fields

### 3. **Support `face_centers` in Save/Load Logic**
- [x] In `planet.save()`, write the dataset if it exists:
  ```python
  if self.mesh.face_centers is not None:
      mesh_grp.create_dataset("face_centers", data=self.mesh.face_centers)
  ```
- [x] In `planet.load()`, restore the dataset if present:
  ```python
  face_centers = mesh_grp["face_centers"][:] if "face_centers" in mesh_grp else None
  ```

### 4. **Update `Planet.summary()` Diagnostic Output**
- [x] Add `face_centers` presence check in the mesh info summary
- [x] Output line includes `face_ids`, `face_centers`, and `adjacency`

---

## 🧪 Validation
- Regenerate a planet with the mesh stage
- Call `planet.summary()` to verify centroids appear as `✔`
- Confirm `.planetbin` file includes `/mesh/face_centers` dataset
- Reload the file and ensure `face_centers` are restored accurately

---

## 🔄 Optional Future Enhancements
- Make `face_centers` a required field on all `MeshData`
- Add overlays or plate motion strategies that directly consume centroid data
- Use centroid-weighted averaging for motion vector clustering

---

This completes the mesh refactor, setting the foundation for tectonic simulation and better overlay rendering.
