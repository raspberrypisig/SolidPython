#! /usr/bin/env python

from pathlib import Path

from solid2.core.utils import escape_openscad_identifier as escape
from solid2.libs.py_scadparser import scad_parser

from openscad_extension_generator import generateStub

headerTemplate = """\
from solid2.core.object_base import OpenSCADObject as _OpenSCADObject,\
                                    OpenSCADConstant as _OpenSCADConstant
from solid2.core.scad_import import extra_scad_include as _extra_scad_include
from pathlib import Path as _Path
from .bosl2_mixin import Bosl2Mixin as _Bosl2Mixin

_extra_scad_include(f"{{_Path(__file__).parent.parent / '{scadFile}'}}", use_not_include={use_not_include})

"""

callableTemplate = """\
class {name}(_OpenSCADObject, _Bosl2Mixin):
    def __init__({paramStr}):
       super().__init__({initStr})

"""


def generateBosl2Std(bosl2_dir):
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

            # for f in bosl2_dir.iterdir():
            #     if not f.suffix == ".scad" or f.name in stdlibs:
            #         continue
            #     std_f.write(f"from . import {f.stem}\n")


mixinHeader = """
def std():
    from . import std
    return std

class Bosl2Mixin:
"""
mixinTemplate = """
    def {name}(self, {paramListWithDefaults}**kwargs):
        return std().{name}({paramList}**kwargs)(self)
"""
def generateBosl2Mixin(bosl2_dir, outputDir):
    def generateCallable(c):
        name = escape(c.name)
        paramNames = [escape(p.name) for p in c.parameters]

        paramListWithDefaults = ", ".join([f"{p}=None" for p in paramNames])
        paramList = ", ".join([f'{p}' for p in paramNames])

        if paramListWithDefaults: paramListWithDefaults += ", "
        if paramList: paramList += ", "

        return mixinTemplate.format(name=name,
                                    paramListWithDefaults=paramListWithDefaults,
                                    paramList=paramList)

    mixinFiles = ["transforms", "attachments", "mutators",
                  "distributors", "partitions", "color"]
    modules = []
    for f in mixinFiles:
        m, _, _ = scad_parser.parseFile((bosl2_dir / f).with_suffix(".scad"))
        modules += m


    with open(outputDir / "bosl2_mixin.py", "w") as f:
        f.write(mixinHeader)

        for c in modules:
            if c.name.startswith("_"):
                continue
            f.write(generateCallable(c))

bosl2_dir = Path("../libs/BOSL2")
output_dir = Path(__file__).parent / "bosl2"

generateBosl2Std(bosl2_dir)
generateBosl2Mixin(bosl2_dir, output_dir)

for f in bosl2_dir.iterdir():
    if not f.suffix == ".scad":
        continue
    if f.name in ["std.scad", "builtins.scad", "bosl1compat.scad"]:
        continue

    generateStub(f, output_dir, False,
                 headerTemplate=headerTemplate,
                 callableTemplate=callableTemplate)

