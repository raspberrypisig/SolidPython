#!/usr/bin/env python
"""Pre-build steps run before packaging solid2.

The preferred method to build solid2 is via poetry:

% poetry build
"""
import os
import sys


bosl2_file = "./solid2/extensions/bosl2/BOSL2/std.scad"
py_scadparser_file = "./solid2/libs/py_scadparser/README.md"

def check_submodule(canary_file):
    if not os.path.exists(canary_file):
        print(f"Cannot find {canary_file} - probably you have not initalized the submodules")
        print("You probably need to run 'git submodule init ; git submodule update'")
        print("     (or clone with --recurse-submodules)")
        sys.exit(1)


def main():
    check_submodule(bosl2_file)
    check_submodule(py_scadparser_file)

if __name__ == "__main__":
    main()
