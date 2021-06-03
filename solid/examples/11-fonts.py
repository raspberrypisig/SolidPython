# ======================================================
# = add relative path to the solid package to sys.path =
# ======================================================
import sys
from pathlib import Path
solidPath = Path(__file__).absolute().parent.parent.parent.as_posix()
sys.path.insert(0, solidPath)
#======================================================

from solid import *

scad = ScadInterface()
scad.register_font("11-font/RichEatin.otf")

text(font="Rich Eatin'", text="blablub").save_as_scad(scad_interface=scad)

