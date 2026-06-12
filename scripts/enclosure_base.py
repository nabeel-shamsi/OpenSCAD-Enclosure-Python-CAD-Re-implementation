from build123d import *

inner_length = 40.0
inner_width = 30.0
wall_thickness = 1.6
ridge_height = 1.0

outer_length = inner_length + 2 * wall_thickness
outer_width = inner_width + 2 * wall_thickness
half_thick = wall_thickness / 2
total_t = wall_thickness + ridge_height
d_circ = total_t + 0.2
inner_y_span = inner_width - 2 * wall_thickness
ridge_z = wall_thickness + ridge_height / 2

with BuildPart() as base_part:
    with Locations((outer_length/2, outer_width/2, wall_thickness/2)):
        Box(outer_length, outer_width, wall_thickness)

    with Locations((wall_thickness + inner_length/2, wall_thickness + wall_thickness/2, ridge_z)):
        Box(inner_length, wall_thickness, ridge_height)

    with Locations((wall_thickness + inner_length/2, wall_thickness + inner_width - wall_thickness/2, ridge_z)):
        Box(inner_length, wall_thickness, ridge_height)

    with Locations((wall_thickness + wall_thickness/2, wall_thickness + wall_thickness + inner_y_span/2, ridge_z)):
        Box(wall_thickness, inner_y_span, ridge_height)

    with Locations((wall_thickness + inner_length - wall_thickness/2, wall_thickness + wall_thickness + inner_y_span/2, ridge_z)):
        Box(wall_thickness, inner_y_span, ridge_height)

    add(Cylinder(28/2, d_circ).moved(
        Location((outer_length/2, outer_width/2, half_thick))
    ), mode = Mode.SUBTRACT)

base = base_part.part

export_step(base, "enclosure_base.step")
export_stl(base, "enclosure_base.stl")
print("Base Exported")
print(f"Volume : {base.volume:.4f} mm^3")


