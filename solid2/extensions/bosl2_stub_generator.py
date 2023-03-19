#! /usr/bin/env python

from pathlib import Path
from openscad_extension_generator import generateStub

headerTemplate = """\
from solid2.core.object_base import OpenSCADObject, OpenSCADConstant
from solid2.core.scad_import import extra_scad_include
from pathlib import Path
from .bosl2_mixin import Bosl2Mixin

extra_scad_include(f"{{Path(__file__).parent.parent / '{scadFile}'}}", use_not_include={use_not_include})

"""

callableTemplate = """\
class {name}(OpenSCADObject, Bosl2Mixin):
    def __init__({paramStr}):
       super().__init__({initStr})

"""


def generateBoslStd(bosl2_dir):
    stubFile = Path(__file__).absolute().parent / "bosl2" / "std.py"

    with open(stubFile, "w") as std_f:
        stdlibs = []
        with open(bosl2_dir / "std.scad") as f:
            for l in f.readlines():
                l = l.strip()
                if not l.startswith("include <"):
                    continue
                l = l.replace("include <", "").replace(">", "")
                std_f.write(f"from .{Path(l).stem} import *\n")
                stdlibs.append(l)

bosl2_dir = Path("../libs/BOSL2")

generateBoslStd(bosl2_dir)

for f in bosl2_dir.iterdir():
    if not f.suffix == ".scad":
        continue
    if f.name in ["std.scad", "builtins.scad", "bosl1compat.scad"]:
        continue

    generateStub(f, Path(__file__).parent / "bosl2", False,
                 headerTemplate=headerTemplate,
                 callableTemplate=callableTemplate)

