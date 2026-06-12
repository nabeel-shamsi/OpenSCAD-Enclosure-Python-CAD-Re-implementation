from build123d import *

inner_length = 40.0
inner_width = 30.0
inner_height = 27.0
wall_thickness = 1.6
ridge_height = 1.0

outer_length = inner_length + 2 * wall_thickness
outer_width = inner_width + 2 * wall_thickness
outer_height = inner_height + 2 * wall_thickness
half_thick = wall_thickness / 2
total_t = wall_thickness + ridge_height
half_t = total_t / 2
d_circ = total_t + 0.2
d_rect = wall_thickness + 0.2
inner_y_span = inner_width - 2 * wall_thickness
ridge_z = wall_thickness + ridge_height / 2

def _rect(face, cx, cy, w, h):

    if face in ("front", "back"):
        x = half_thick if face == "front" else outer_length - half_thick
        return Box(d_rect, w, h).moved(Location((x, outer_width/2+cx, outer_height/2+cy)))
    
    y = half_thick if face == "left" else outer_width - half_thick
    return Box(w, d_rect, h).moved(Location((outer_length/2+cx, y, outer_height/2+cy)))

def _circ(face, cx, cy, dia):
    r = dia / 2
    rotations = {"front": (0, 90, 0), "back": (0, -90, 0), "left": (90, 0, 0), "right": (-90, 0, 0)}
    origins = {
        "front": (half_thick, outer_width/2+cx, outer_height/2+cy),
        "back": (outer_length - half_thick, outer_width/2+cx, outer_height/2+cy),
        "left": (outer_length/2+cx, half_thick, outer_height/2+cy),
        "right": (outer_length/2+cx, outer_width - half_thick, outer_height/2+cy),
    }
    return Cylinder(r, d_circ, rotation = rotations[face]).moved(Location(origins[face]))

def build_walls():
    with BuildPart() as bp:
        with Locations((outer_length/2, wall_thickness/2, outer_height/2)):
            Box(outer_length, wall_thickness, outer_height)

        with Locations((outer_length/2, outer_width - wall_thickness/2, outer_height/2)):
            Box(outer_length, wall_thickness, outer_height)

        with Locations((wall_thickness/2, wall_thickness + inner_width/2, outer_height/2)):
            Box(wall_thickness, inner_width, outer_width)

        with Locations((outer_length - wall_thickness/2, wall_thickness + inner_width/2, outer_height/2)):
            Box(wall_thickness, inner_width, outer_height)

        add(_rect("left", 11, 1.5, 10, 4), mode = Mode.SUBTRACT)
        add(_rect("front", 0, 3.5, 9, 3.5), mode = Mode.SUBTRACT)
        add(_circ("front", 6.5, 3.5, 1), mode = Mode.SUBTRACT)
        add(_circ("front", -6.5, 3.5, 1), mode = Mode.SUBTRACT)
        add(_circ("right", 15, -7.5, 6), mode = Mode.SUBTRACT)
    return bp.part

def build_base():
    with BuildPart() as bp:
        with Locations((outer_length/2, outer_width/2, wall_thickness/2)):
            Box(outer_length, outer_width, wall_thickness)

        with Locations((wall_thickness + inner_length/2, wall_thickness+ wall_thickness/2, ridge_z)):
            Box(inner_length, wall_thickness, ridge_height)

        with Locations((wall_thickness+inner_length/2, wall_thickness+inner_width-wall_thickness/2, ridge_z)):
            Box(inner_length, wall_thickness, ridge_height)

        with Locations((wall_thickness+wall_thickness/2, wall_thickness+wall_thickness+inner_y_span/2, ridge_z)):
            Box(wall_thickness, inner_y_span, ridge_height)

        with Locations((wall_thickness+inner_length-wall_thickness/2, wall_thickness+wall_thickness+inner_y_span/2, ridge_z)):
            Box(wall_thickness, inner_y_span, ridge_height)

        add(Cylinder(28/2, d_circ).moved(
            Location((outer_length/2, outer_width/2, half_thick))
        ), mode = Mode.SUBTRACT)
    return bp.part

def build_lid():
    with BuildPart() as bp:
        with Locations((outer_length/2, outer_width/2, wall_thickness/2)):
            Box(outer_length, outer_width, wall_thickness)

        with Locations((wall_thickness+inner_length/2, wall_thickness+wall_thickness/2, ridge_z)):
            Box(inner_length, wall_thickness, ridge_height)

        with Locations((wall_thickness+inner_length/2, wall_thickness+inner_width-wall_thickness/2, ridge_z)):
            Box(inner_length, wall_thickness, ridge_height)

        with Locations((wall_thickness+wall_thickness/2, wall_thickness+wall_thickness+inner_y_span/2, ridge_z)):
            Box(wall_thickness, inner_y_span, ridge_height)

        with Locations((wall_thickness+inner_length-wall_thickness/2, wall_thickness+wall_thickness+inner_y_span, ridge_z)):
            Box(wall_thickness, inner_y_span, ridge_height)

        add(Cylinder(3.5/2, d_circ).moved(
            Location((outer_length/2+9, outer_width/2, half_t))
        ), mode = Mode.SUBTRACT)
    return bp.part

print("Building parts_")
walls = build_walls()
base = build_base()
lid = build_lid()

flat = Compound(children = [
    walls.moved(Location((0, 0, 0))),
    base.moved(Location((outer_length + 10, 0, 0))),
    lid.moved(Location((0, outer_width + 10, 0))),
])

export_step(flat, "enclosure_assembly_flat.step")
export_stl(flat, "enclosure_assembly_flat.stl")
print("Flat assembly -> enclosure_assembly_flat.step/stl")

lid_asm = lid.rotate(Axis.X, 180).moved(
    Location((0, outer_width, outer_height + wall_thickness + ridge_height))
)
func = Compound(children = [
    walls.moved(Location((0, 0, 0))),
    base.moved(Location((0, 0, -wall_thickness))),
    lid_asm,

])

export_step(func, "enclosure_assembly_functional.step")
export_stl(func, "enclosure_assembly_functional.stl")
print("Functional assembly -> enclosure_assembly_functional.step/stl")

print(f"\nVolumes - Walls: {walls.volume:.2f} | Base: {base.volume:.2f} | Lid: {lid.volume:.2f} mm^3")