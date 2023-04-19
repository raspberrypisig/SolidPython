#!/usr/bin/env python
"""Pre-build steps run before packaging solid2.

The preferred method to build solid2 is via poetry:

% poetry build
"""
import os
import sys


def check_bosl2_submodule():
    canary_file = "./solid2/libs/BOSL2/std.scad"
    if not os.path.exists(canary_file):
        print(f"Cannot find {canary_file} - probably you have not initalized the BOSL submodule")
        print("You probably need to run 'git submodule init ; git submodule update'")
        print("     (or clone with --recurse-submodules)")
        sys.exit(1)


def main():
    check_bosl2_submodule()


if __name__ == "__main__":
    main()
