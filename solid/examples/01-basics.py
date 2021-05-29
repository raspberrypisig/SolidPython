#======================================================
#include relative path to the solid package in sys.path
#======================================================
import sys
from pathlib import Path
solidPath = Path(__file__).absolute().parent.parent.parent.as_posix()
sys.path.append(solidPath)
#======================================================

from solid import *

d = difference()(
        cube([10, 20, 30]),
        sphere(10)
    )

d.save_as_scad()

