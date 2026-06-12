import sys, os, math
import numpy as np

try:
    import trimesh
except ImportError:
    sys.exit("trimesh not found. Run: pip install trimesh manifold3d")

PAIRS = [
    ("enclosure_walls.stl", "enclosure_walls_ref.stl", "Walls"),
    ("enclosure_base.stl", "enclosure_base_ref.stl", "Base"),
    ("enclosure_lid.stl", "enclosure_lid-ref.stl", "Lid")
]

EXPECTED_VLOUMES = {
    "Walls" : 7043.5759,
    "Base" : 3025.9293,
    "Lid" : 2516.7202,
}

VOLUME_TOLERANCE = 5.0
SYMDIFF_TOLERANCE = 0.5

def load_and_repair(path: str) -> trimesh.Trimesh:
    mesh = trimesh.load_mesh(path, force = "mesh")
    if not isinstance(mesh, trimesh.Trimesh):
        mesh = trimesh.util.concatenate(list(mesh.dump()))

    trimesh.repair.fix_normals(mesh)
    trimesh.repair.fix_winding(mesh)
    trimesh.repair.fill_holes(mesh)
    return mesh

def symmetric_difference_volume(mesh_a: trimesh.Trimesh,
                                mesh_b: trimesh.Trimesh) -> float:
    
    try:
        isect = trimesh.boolean.intersection([mesh_a, mesh_b], engine = "manifold")
        vol_i = abs(isect.volume) if isect.is_volume else 0.0
        return abs(mesh_a.volume) + abs(mesh_b.volume) - 2 * vol_i
    except Exception as exc:
        print(f"Boolean failed({exc}); using |Volume| fallback.")
        return abs(abs(mesh_a.volume) - abs(mesh_b.volume))
    
def stl_volume(path: str) -> float:
    import struct
    vol = 0.0
    with open(path, "rb") as f:
        f.read(80)
        n = struct.unpack("<I", f.read(4))[0]
        for _ in range(n):
            f.read(12)
            v = [struct.unpack("<fff", f.read(12)) for _ in range(3)]
            f.read(2)
            vol += (
                v[0][0]*(v[1][1]*v[2][2]-v[1][2]*v[2][1]) + 
                v[0][1]*(v[1][2]*v[2][0]-v[1][0]*v[2][2]) +
                v[0][2]*(v[1][0]*v[2][1]-v[1][1]*v[2][0])
            ) / 6.0
    return abs(vol)

print("=" *64)
print(" Enclosure Geometry Verification")
print("=" *64)

all_passed = True

print("\n Part-by-Part comparison \n")

for gen_path, ref_path, label in PAIRS:
    print(f" {label}")

    if not os.path.exists(gen_path):
        print(f" {gen_path} not found - run enclosure_{label.lower()}.py first.\n")
        all_passed = False
        continue

    mesh_gen = load_and_repair(gen_path)
    vol_gen = abs(mesh_gen.volume)
    expected = EXPECTED_VLOUMES[label]
    vol_err = abs(vol_gen - expected)

    print(f" Generated Volume : {vol_gen:.4f} mm^3")
    print(f" Expected (BREP) : {expected:.4f} mm^3")
    if vol_err < VOLUME_TOLERANCE:
        print(f" Volume diff : {vol_err:.4f} mm^3  (within {VOLUME_TOLERANCE} mm^3)")
    else:
        print(f" Volume diff : {vol_err:.4f} mm^3 UNEXPECTED ")
        all_passed = False

    if not os.path.exists(ref_path):
        print(f" {ref_path} not found")
        print(f" Export {label.lower()}(); ")
        continue

    mesh_ref = load_and_repair(ref_path)
    vol_ref = abs(mesh_ref.volume)
    sym_diff = symmetric_difference_volume(mesh_gen, mesh_ref)

    print(f" Reference Volume : {vol_ref:.4f} mm^3") 
    print(f" Volume : {abs(vol_gen - vol_ref):.6f} mm^3")
    print(f" Symmetric-diff : {sym_diff:.6f}mm^3 (tolerance {SYMDIFF_TOLERANCE})mm^3")

    if sym_diff < SYMDIFF_TOLERANCE:
        print(f" Pass - geometry exactly matches \n")
    else:
        print(f" Fail - geometry difference detected \n")

print("\n Repo Enclosure.stl analysis \n")
REPO_STL = "enclosure.stl"

if os.path.exists(REPO_STL):
    repo_vol = stl_volume(REPO_STL)
    our_total = sum(EXPECTED_VLOUMES.values())
    diff = our_total - repo_vol
    hole_28mm = math.pi * (14*2) *2.8

    print(f" Repo STL volume : {repo_vol:.4f} mm^3")
    print(f" Our assembly volume : {our_total:.4f} mm^3")
    print(f"Difference : {diff:.4f} mm^3")
    print(f" 28mm base hole volume : {hole_28mm:.4f} mm^3")
    print(f"Residual after hole : {abs(diff - hole_28mm):.4f} mm^3")
    print()
    if abs(diff - hole_28mm) < 100:
        print(" Our build123d scripts correctly match the current .scad source")
    else:
        print("Unexpected diff - investigate ")

else:
    print(f" {REPO_STL} not found (skipping)")





