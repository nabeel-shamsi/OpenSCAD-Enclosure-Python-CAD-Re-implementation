/*
Parametric box with removable lid and bottom, 3mm walls, and ridge frames.
Holes via make_hole_circ() and make_hole_rect().
All parts arranged flat for single-bed printing.
*/

// Parameters
$fn=512;
inner_length   = 40;
inner_width    = 30;
inner_height   = 27;
wall_thickness = 1.6;
ridge_height   = 1;

// Derived
outer_length = inner_length + 2*wall_thickness;
outer_width  = inner_width  + 2*wall_thickness;
outer_height = inner_height + 2*wall_thickness;
half_thick   = wall_thickness/2;

// Hole modules (origin at face center)
// face: "front"/"back" = X faces; "left"/"right" = Y faces; "bottom"/"top" = Z faces
module make_hole_circ(face="front", cx=0, cy=0, dia=5) {
    // hole depth and radius
    total_t = wall_thickness + ridge_height;
    d       = total_t + 0.2;
    half_t  = total_t / 2;
    r       = dia/2;
    // front/back/left/right/bottom as before
    if (face == "front") {
        translate([half_thick, outer_width/2 + cx, outer_height/2 + cy])
            rotate([0,90,0]) cylinder(h=d, r=r, center=true);
    } else if (face == "back") {
        translate([outer_length - half_thick, outer_width/2 + cx, outer_height/2 + cy])
            rotate([0,-90,0]) cylinder(h=d, r=r, center=true);
    } else if (face == "left") {
        translate([outer_length/2 + cx, half_thick, outer_height/2 + cy])
            rotate([90,0,0]) cylinder(h=d, r=r, center=true);
    } else if (face == "right") {
        translate([outer_length/2 + cx, outer_width - half_thick, outer_height/2 + cy])
            rotate([-90,0,0]) cylinder(h=d, r=r, center=true);
    } else if (face == "bottom") {
        translate([outer_length/2 + cx, outer_width/2 + cy, half_thick])
            cylinder(h=d, r=r, center=true);
    } else if (face == "top") {
        // top: cut centered through combined panel+ridge
        translate([outer_length/2 + cx, outer_width/2 + cy, half_t])
            cylinder(h=d, r=r, center=true);
    }
}

module make_hole_rect(face="front", cx=0, cy=0, w=5, h=10) {
    d = wall_thickness + 0.2;
    if (face == "front" || face == "back") {
        x = (face == "front") ? half_thick : outer_length - half_thick;
        translate([x, outer_width/2 + cx, outer_height/2 + cy])
            cube([d, w, h], center=true);
    } else if (face == "left" || face == "right") {
        y = (face == "left") ? half_thick : outer_width - half_thick;
        translate([outer_length/2 + cx, y, outer_height/2 + cy])
            cube([w, d, h], center=true);
    } else if (face == "bottom" || face == "top") {
        z = (face == "bottom") ? half_thick : ridge_height + half_thick;
        translate([outer_length/2 + cx, outer_width/2 + cy, z])
            cube([w, h, d], center=true);
    }
}

// Base: bottom panel + ridge frame
module base() {
    difference() {
        union() {
            cube([outer_length, outer_width, wall_thickness]);
            translate([wall_thickness, wall_thickness, wall_thickness]) {
                cube([inner_length, wall_thickness, ridge_height]);
                translate([0, inner_width - wall_thickness, 0]) cube([inner_length, wall_thickness, ridge_height]);
                translate([0, wall_thickness, 0]) cube([wall_thickness, inner_width - 2*wall_thickness, ridge_height]);
                translate([inner_length - wall_thickness, wall_thickness, 0]) cube([wall_thickness, inner_width - 2*wall_thickness, ridge_height]);
            }
        }
        // make_hole_circ("bottom", cx, cy, dia);
        // make_hole_rect("bottom", cx, cy, w, h);
        //make_hole_circ("bottom", 7, 0, 28);
        make_hole_circ("bottom", 0, 0, 28);
    }
}

// Lid: panel + ridge frame on top
module lid() {
    difference() {
        union() {
            // flat panel
            cube([outer_length, outer_width, wall_thickness]);
            // ridge frame on top of panel
            translate([wall_thickness, wall_thickness, wall_thickness]) {
                cube([inner_length, wall_thickness, ridge_height]);
                translate([0, inner_width - wall_thickness, 0]) cube([inner_length, wall_thickness, ridge_height]);
                translate([0, wall_thickness, 0]) cube([wall_thickness, inner_width - 2*wall_thickness, ridge_height]);
                translate([inner_length - wall_thickness, wall_thickness, 0]) cube([wall_thickness, inner_width - 2*wall_thickness, ridge_height]);
            }
        }
        // make_hole_circ("top", cx, cy, dia);
        // make_hole_rect("top", cx, cy, w, h);
        make_hole_circ("top", 9, 0, 3.5);
    }
}

// Walls: 4-sided frame
module walls() {
    difference() {
        union() {
            cube([outer_length, wall_thickness, outer_height]);
            translate([0, outer_width - wall_thickness, 0]) cube([outer_length, wall_thickness, outer_height]);
            translate([0, wall_thickness, 0]) cube([wall_thickness, inner_width, outer_height]);
            translate([outer_length - wall_thickness, wall_thickness, 0]) cube([wall_thickness, inner_width, outer_height]);
        }
        // make_hole_circ("front", cx, cy, dia);
        // make_hole_circ("back", cx, cy, dia);
        // make_hole_circ("left", cx, cy, dia);
        // make_hole_circ("right", cx, cy, dia);
        // make_hole_rect("front", cx, cy, w, h);
        // make_hole_rect("back", cx, cy, w, h);
        // make_hole_rect("left", cx, cy, w, h);
        // make_hole_rect("right", cx, cy, w, h);
        make_hole_rect("left", 11, 1.5, 10, 4);
        make_hole_rect("front", 0, 3.5, 9, 3.5);
        make_hole_circ("front", 6.5, 3.5, 1);
        make_hole_circ("front", -6.5, 3.5, 1);
        make_hole_circ("right", 15, -7.5, 6);
    }
}

// Arrange for single-bed printing
module arranged_parts() {
    walls();
    translate([outer_length + 10, 0, 0]) base();
    translate([0, outer_width + 10, 0]) lid();
}

arranged_parts();
