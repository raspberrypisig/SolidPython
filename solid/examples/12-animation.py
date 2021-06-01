# ======================================================
# = add relative path to the solid package to sys.path =
# ======================================================
import sys
from pathlib import Path
solidPath = Path(__file__).absolute().parent.parent.parent.as_posix()
sys.path.append(solidPath)
#==================================================

from solid import *

view_port_magic = ("""
                       $vpt = [4, 3, 15];
                       $vpr = [60, 0, 360 * $t];
                       $vpd = 100;
                   """)

c = cube(scad_inline("$t*10"))

scad_render_to_file(c, file_header=view_port_magic)

