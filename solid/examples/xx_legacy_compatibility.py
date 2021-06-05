# ======================================================
# = add relative path to the solid package to sys.path =
# ======================================================
import sys
from pathlib import Path
solidPath = Path(__file__).absolute().parent.parent.parent.as_posix()
sys.path.append(solidPath)
#==================================================

from solid import *
from solid.extensions.legacy import *

c = cylinder(1, 5)

c.set_modifier("#")
c.set_modifier("%")

c.add_param("segments", 3)

c.add_trait("blub", 4)
assert(c.get_trait("blub") == 4)

cc = 0 + c

print(c.as_scad())
assert(c.as_scad() == "%cylinder($fn = 3, h = 5, r = 1);")
