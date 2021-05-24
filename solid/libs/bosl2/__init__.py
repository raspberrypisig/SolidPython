from pathlib import Path
from ...scad_import import import_scad
from ...helpers import calling_module

bosl2_path = Path(__file__).parent / "BOSL2_scad"
import_scad(bosl2_path, calling_module(1))

