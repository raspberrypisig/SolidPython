import sys
from pathlib import Path

solidPath = Path(__file__).absolute().parent.parent.parent.as_posix()
sys.path.append(solidPath)

from solid.builtins import *
from solid import scad_render_to_file

def demo_builtins():
    c = cube([10, 20, 30]).translate([-10, -5, 2]).debug()
    return c + debug(color("RED")(rotate(v=[0, 0, 90], a=1)(sphere(10))))

if __name__ == '__main__':
    out_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    a = demo_builtins()
    file_out = scad_render_to_file(a, out_dir=out_dir)
    print(f"{__file__}: SCAD file written to: \n{file_out}")
