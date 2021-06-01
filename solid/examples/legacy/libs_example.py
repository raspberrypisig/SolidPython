# ======================================================
# = add relative path to the solid package to sys.path =
# ======================================================
import sys
from pathlib import Path
solidPath = Path(__file__).absolute().parent.parent.parent.parent.as_posix()
sys.path.append(solidPath)
#==================================================

from solid import import_scad, scad_render_to_file

#MCAD = import_scad("MCAD")
BOSL = import_scad("BOSL")
#BOSL2 = import_scad("BOSL2")

b = BOSL.linear_bearings.linear_bearing_housing()
c = BOSL.shapes.cuboid([20, 20, 30], chamfer=2)

scad_render_to_file(b.right(50) + c)
