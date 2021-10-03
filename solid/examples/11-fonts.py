#! /usr/bin/env python

from solid import *

scad = ScadInterface()
scad.register_font("11-font/RichEatin.otf")

text(font="Rich Eatin'", text="blablub").save_as_scad(scad_interface=scad)

