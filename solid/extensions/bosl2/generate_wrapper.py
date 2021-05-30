#!/usr/bin/python3

from pathlib import Path

def gen_wrapper(dir_name, out_dir_name):

    path = Path(dir_name)
    out_dir_path = Path(out_dir_name)

    assert(path.is_dir())

    for f in path.iterdir():
        if f.suffix != ".scad":
            continue

        out_file_path = out_dir_path / f.with_suffix(".py").name

        with out_file_path.open("w") as out:
            module_name = f.with_suffix('').name
            code = [f"from ... import include\n",
                    f"include('BOSL2/{module_name}.scad')\n"]
            out.writelines(code)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print(f'usage: {sys.argv[0]} <path/to/bosl2/> <out_dir>')
        sys.exit(0)

    gen_wrapper(sys.argv[1], sys.argv[2])
