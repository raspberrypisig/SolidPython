# ======================================================
# = add relative path to the solid package to sys.path =
# ======================================================
import sys
from pathlib import Path
solidPath = Path(__file__).absolute().parent.parent.parent.as_posix()
sys.path.insert(0, solidPath)
#==================================================

from solid import *

scad = ScadInterface()

scad.register_customizer_var("rotation_speed", 1.0)

scad.set_global_var("$vpt", [4, 3, 15])
scad.set_global_var("$vpr", "[60, 0, 360 * $t * rotation_speed]")
scad.set_global_var("$vpd", 100)

c = cube(scad.inline("$t * 10"))

scad_render_to_file(c, scad_interface=scad)

