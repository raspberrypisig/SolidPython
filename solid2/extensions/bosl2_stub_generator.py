#! /usr/bin/env python

from pathlib import Path

from solid2.core.utils import escape_openscad_identifier as escape
from solid2.libs.py_scadparser import scad_parser

headerTemplate = """\
from ...core.object_base import OpenSCADObject, OpenSCADConstant
from ... import import_scad
from pathlib import Path

baseDir = Path(__file__).absolute().parent.parent.parent
importFile = baseDir / "libs" / "BOSL2" / "{scadFile.name}"
_ = import_scad(f"{{importFile}}", use_not_include=False)

"""

constantTemplate = "{name} = OpenSCADConstant('{name}')"

callableTemplate = """\
class {name}(OpenSCADObject):
    def __init__({paramStr}):
       super().__init__({initStr})

"""

def generateStub(scadFile, outputDir):
    def generateHeader():
        return headerTemplate.format(__file__=__file__, scadFile=scadFile)

    def generateConstant(c):
        return constantTemplate.format(name=escape(c.name)) + "\n"

    def generateCallable(c):
        name = escape(c.name)
        paramNames = [escape(p.name) for p in c.parameters]

        paramStr = ", ".join(["self"] +
                             [f"{p}=None" for p in paramNames] +
                             ["**kwargs"])
        initList = [f'"{p}" : {p}' for p in paramNames]
        initList.append("**kwargs")
        initStr = f'"{name}", {{{", ".join(initList)}}}'
        return callableTemplate.format(name=name, paramStr=paramStr, initStr=initStr)

    modules, functions, global_vars = scad_parser.parseFile(scadFile)

    with open(outputDir / scadFile.with_suffix(".py").name, "w") as f:
        f.write(generateHeader())

        for c in global_vars:
            f.write(generateConstant(c))

        for c in modules + functions:
            f.write(generateCallable(c))

def generateBoslStd(bosl2_dir):
    stubFile = Path(__file__).absolute().parent / "bosl2" / "all.py"

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

        for f in bosl2_dir.iterdir():
            if not f.suffix == ".scad" or f.name in stdlibs:
                continue
            if f.name in ["std.scad", "builtins.scad", "bosl1compat.scad"]:
                continue

            name = f.name.replace(".scad","")
            std_f.write(f"import solid2.extensions.bosl2.{name} as {name}\n")


bosl2_dir = Path(__file__).absolute().parent.parent / "libs/BOSL2"

generateBoslStd(bosl2_dir)

for f in bosl2_dir.iterdir():
    if not f.suffix == ".scad":
        continue
    if f.name in ["std.scad", "builtins.scad", "bosl1compat.scad"]:
        continue

    generateStub(f, Path(__file__).absolute().parent / "bosl2")

