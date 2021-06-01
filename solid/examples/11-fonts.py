# ======================================================
# = add relative path to the solid package to sys.path =
# ======================================================
import sys
from pathlib import Path
solidPath = Path(__file__).absolute().parent.parent.parent.as_posix()
sys.path.append(solidPath)
#======================================================

from solid import *

use("11-font/RichEatin.otf")

text(font="Rich Eatin'", text="blablub").save_as_scad()

