# ======================================================
# = add relative path to the solid package to sys.path =
# ======================================================
import sys
from pathlib import Path
solidPath = Path(__file__).absolute().parent.parent.parent.as_posix()
sys.path.append(solidPath)
#==================================================

from solid import *

scad = ScadInterface()

#register all the custom variables you want to use
scad.register_customizer_var("objects", "4", "[2, 4, 6]")
scad.register_customizer_var("side", "4")
scad.register_customizer_var("cube_pos", "[5, 5, 5]")
scad.register_customizer_var("cube_size", "5")
scad.register_customizer_var("text", '"customize me!"' ,' ["customize me!", "Thank you!"]')

#use scad_inline to use them
scene = scad_inline("""
                    for (i = [1:objects]){
                        translate([2*i*side,0,0]){
                            cube(side);
                        }
                    }
                    """)

#use the customizer.get function to use them as parameters
py_factor = 2
cube_size = scad.inline(f"cube_size - cube_pos[0] * {py_factor}")

scene += translate(scad.inline("cube_pos")) (
            cube(cube_size))

scene += translate([0, -20, 0]) (
            text(scad.inline("text")))

scad_render_to_file(scene, scad_interface=scad)

