# ======================================================
# = add relative path to the solid package to sys.path =
# ======================================================
import sys
from pathlib import Path
solidPath = Path(__file__).absolute().parent.parent.parent.as_posix()
sys.path.append(solidPath)
#======================================================

from solid import *

scad = ScadInterface()
scad.register_font("11-font/RichEatin.otf")

t = text(font="Rich Eatin'", text="blablub")
scad_render_to_file(t, scad_interface=scad)

