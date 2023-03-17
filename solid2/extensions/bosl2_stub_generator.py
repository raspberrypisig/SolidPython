#! /usr/bin/env python

from pathlib import Path

from solid2.core.utils import escape_openscad_identifier
from solid2.libs.py_scadparser import scad_parser

def generateStub(scadFile, outputDir):
    modules, functions, global_vars = scad_parser.parseFile(scadFile)
    escape = escape_openscad_identifier

    stubFile = Path(__file__).absolute().parent / outputDir / scadFile.name
    stubFile = stubFile.with_suffix(".py")
    with open(stubFile, "w") as f:
        f.write("from ...core.object_base import OpenSCADObject, OpenSCADConstant\n")
        f.write("from ... import import_scad\n")
        f.write("from pathlib import Path\n\n")
        f.write(f"importFile = Path(__file__).absolute().parent.parent.parent / 'libs' / 'BOSL2' / '{scadFile.name}'\n")
        f.write("_ = import_scad(f'{importFile}', use_not_include=False)\n\n")
        stub = ""
        for c in global_vars:
            f.write(f"{escape(c.name)} = OpenSCADConstant('{escape(c.name)}')\n")
        f.write("\n")

        for c in modules + functions:
            stub = f"class {escape(c.name)}(OpenSCADObject):\n    def __init__(self"

            for p in c.parameters:
                stub += f", {escape(p.name)}=None"
            stub += ", **kwargs):\n"

            stub += f'       super().__init__("{escape(c.name)}" ,{{'
            for p in c.parameters:
                if c.parameters.index(p) != 0:
                    stub += ", "
                stub += f'"{escape(p.name)}" : {escape(p.name)}'
            if len(c.parameters):
                stub += ", "
            stub += "**kwargs})\n\n"

            f.write(stub)

def generateStd(bosl2_dir, outputDir):
    stubFile = Path(__file__).absolute().parent / outputDir / "all.py"

    with open(stubFile, "w") as std_f:
        with open(bosl2_dir / "std.scad") as f:
            for l in f.readlines():
                l = l.strip()
                if not l.startswith("include <"):
                    continue
                l = l.replace("include <", "").replace(">", "")
                std_f.write(f"from .{Path(l).stem} import *\n")

            for f in bosl2_dir.iterdir():
                if not f.suffix == ".scad":
                    continue
                if f.name in ["std.scad", "builtins.scad", "bosl1compat.scad"]:
                    continue

                name = f.name.replace(".scad","")
                std_f.write(f"import solid2.extensions.{outputDir}.{name} as {name}\n")


bosl2_dir = Path(__file__).absolute().parent.parent / "libs/BOSL2"

generateStd(bosl2_dir, "bosl2")

for f in bosl2_dir.iterdir():
    if not f.suffix == ".scad":
        continue
    if f.name in ["std.scad", "builtins.scad", "bosl1compat.scad"]:
        continue

    generateStub(f, "bosl2")

