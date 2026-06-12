# OpenSCAD Enclosure — Python CAD Re-implementation

> **A parametric electronics enclosure originally designed in OpenSCAD, fully re-implemented as a multi-file Python CAD pipeline using [build123d](https://github.com/gumyr/build123d), with automated geometry verification.**

---

## Project Overview

This project takes an existing OpenSCAD parametric enclosure design and reconstructs it programmatically in Python — producing watertight, print-ready STL and STEP files for each component, along with a full assembly in two configurations.

The enclosure is a 3-part snap-fit box (walls, base, lid) with parametric apertures (circular and rectangular cutouts) on any face — suitable for housing electronics like microcontrollers, connectors, and buttons.

**Key dimensions:**
- Interior: 40 × 30 × 27 mm
- Wall thickness: 1.6 mm
- Ridge height: 1.0 mm (for lid/base alignment)

---

## Skills Demonstrated

### 1. Parametric 3D CAD with Python (`build123d`)
Rather than relying on a GUI or declarative DSL, each part is constructed using the `build123d` BREP (Boundary Representation) library — the same kernel used by professional CAD tools. This involves:

- Programmatic solid construction using `Box`, `Cylinder`, and boolean `SUBTRACT` operations
- Precise coordinate math to locate holes relative to face centres, accounting for wall thickness and ridge offsets
- Reusable helper functions (`_circ`, `_rect`) that abstract hole placement across any named face (`"front"`, `"back"`, `"left"`, `"right"`, `"top"`, `"bottom"`)
- Context-managed `BuildPart` workflows for clean, composable geometry

### 2. Multi-Part Assembly & Export Pipeline
The assembly script (`enclosure_assembly.py`) composes all three parts into two configurations:

- **Flat layout** — parts arranged side-by-side for single-bed 3D printing
- **Functional layout** — lid and base positioned as they would sit on the assembled enclosure

Both configurations are exported as `.stl` (mesh) and `.step` (solid BREP) files, giving flexibility for different downstream toolchains.

### 3. Geometry Verification (`verify_geometry.py`)
A standalone verification script provides confidence that the generated geometry is correct:

- Loads each STL using `trimesh`, repairs normals/winding/holes automatically
- Compares generated volume against expected BREP values within a configurable tolerance (±5 mm³)
- Computes **symmetric difference volume** between generated and reference meshes using manifold boolean intersection — a rigorous shape-equivalence check (not just a volume check)
- Falls back gracefully to a volume-delta check if the boolean engine is unavailable
- Cross-validates against the original `enclosure.stl` from the OpenSCAD source, accounting for the 28 mm base hole

### 4. OpenSCAD → Python Fidelity
All aperture geometry from the original `.scad` source is faithfully reproduced:

| Aperture | Face | Position | Size |
|----------|------|----------|------|
| Rectangular cutout | Left | cx=11, cy=1.5 | 10 × 4 mm |
| Rectangular cutout | Front | cx=0, cy=3.5 | 9 × 3.5 mm |
| Circular hole ×2 | Front | cx=±6.5, cy=3.5 | ∅1 mm |
| Circular hole | Right | cx=15, cy=−7.5 | ∅6 mm |
| Circular hole | Base | centre | ∅28 mm |
| Circular hole | Lid | cx=9 | ∅3.5 mm |

---

## File Structure

```
OpenSCAD-Enclosure/
│
├── Enclosure.scad               # Original OpenSCAD source (reference design)
│
├── enclosure_walls.py           # build123d script → walls.stl / .step
├── enclosure_base.py            # build123d script → base.stl / .step
├── enclosure_lid.py             # build123d script → lid.stl / .step
│
├── enclosure_assembly.py        # Composes all 3 parts into flat + functional assemblies
│                                #   → enclosure_assembly_flat.stl / .step
│                                #   → enclosure_assembly_functional.stl / .step
│
├── verify_geometry.py           # Automated volume + symmetric-difference verification
│
├── enclosure_walls.stl/.step
├── enclosure_base.stl/.step
├── enclosure_lid.stl/.step
├── enclosure_assembly_flat.stl/.step
└── enclosure_assembly_functional.stl/.step
```

---

## How to Run

### Prerequisites

```bash
pip install build123d trimesh manifold3d numpy
```

> OpenSCAD is **not** required to run the Python scripts — only to view or modify the original `.scad` reference.

### Generate Parts

```bash
python enclosure_walls.py      # → enclosure_walls.stl, enclosure_walls.step
python enclosure_base.py       # → enclosure_base.stl, enclosure_base.step
python enclosure_lid.py        # → enclosure_lid.stl, enclosure_lid.step
```

### Generate Assemblies

```bash
python enclosure_assembly.py
# → enclosure_assembly_flat.stl/.step
# → enclosure_assembly_functional.stl/.step
```

### Verify Geometry

```bash
python verify_geometry.py
```

Expected output (if reference STLs are present):

```
================================================================
 Enclosure Geometry Verification
================================================================

 Part-by-Part comparison

 Walls
 Generated Volume : 7043.5759 mm^3
 Expected (BREP)  : 7043.5759 mm^3
 Volume diff      : 0.0000 mm^3  (within 5.0 mm^3)
 Pass - geometry exactly matches

 ...

 Our build123d scripts correctly match the current .scad source
```

---

## Technical Notes

- **Ridge frames** on the base and lid act as alignment features — the ridge sits inside the walls when assembled, preventing lateral movement.
- **Hole depth** includes a 0.2 mm clearance overcut (`wall_thickness + 0.2`) to ensure clean boolean subtraction without z-fighting artefacts.
- The `$fn=512` resolution in OpenSCAD is matched implicitly by build123d's BREP kernel, which represents circles analytically rather than as polygonal approximations.
- The flat assembly uses a 10 mm gap between parts — matching the OpenSCAD `arranged_parts()` layout — to facilitate slicing without manual repositioning.

---

## Relation to Original OpenSCAD Project

This repository builds on the enclosure design by [astromikemerri](https://github.com/astromikemerri/OpenSCAD-Enclosure). The Python re-implementation:

- Preserves all parametric dimensions and aperture geometry exactly
- Adds STEP export (not available from OpenSCAD directly) for use in Fusion 360, FreeCAD, or other BREP-aware tools
- Introduces automated geometry verification absent from the original
- Separates parts into individual scripts for cleaner iteration

---

## License

See [LICENSE](LICENSE) for terms inherited from the upstream project.
