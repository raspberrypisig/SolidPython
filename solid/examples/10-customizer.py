# ======================================================
# = add relative path to the solid package to sys.path =
# ======================================================
import sys
from pathlib import Path
solidPath = Path(__file__).absolute().parent.parent.parent.as_posix()
sys.path.append(solidPath)
#==================================================

from solid import *

customizer = Customizer()

#register all the custom variables you want to use
customizer.register("objects", "4", "[2, 4, 6]")
customizer.register("side", "4")
customizer.register("cube_pos", "[5, 5, 5]")
customizer.register("cube_size", "5")
customizer.register("text", '"customize me!"' ,' ["customize me!", "Thank you!"]')

#use scad_inline to use them
scene = scad_inline("""
                    for (i = [1:objects]){
                        translate([2*i*side,0,0]){
                            cube(side);
                        }
                    }
                    """)

#use the customizer.get function to use them as parameters
scene += translate(customizer.get("cube_pos")) (
            cube(customizer.get("cube_size")))

scene += translate([0, -20, 0]) (
            text(customizer.get("text")))

scad_render_to_file(scene, file_header = customizer.header)

