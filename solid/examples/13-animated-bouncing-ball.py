#! /usr/bin/env python

import numpy as np

from solid import *

#set steps in OpenSCAD to 1000

ball_radius = 100

#this is our little physics engine
def get_bouncing_ball_data(pos=np.array([0.0, 0.0, 0.0]), vel=np.array([5.0, 5.0, 200.0])):
    data = []
    gravity = np.array([0.0, 0.0, -8.0])
    for t in range(1000):
        vel = (vel + gravity) * 0.995
        pos += vel
        if pos[2] < ball_radius:
            vel[2] = vel[2] * -1
            pos[2] = ball_radius

        data.append(pos.tolist())

    return data

scad = ScadInterface()
scad.set_global_var("$vpt", [700, 900, 200])
scad.set_global_var("$vpr", [80, 0, 20])
scad.set_global_var("$vpd", 6000)

#store pre computed data in global OpenSCAD variable
scad.set_global_var("bouncing_ball_data", get_bouncing_ball_data())

#get "dynamic ball position over time" from the data set
ball_pos_over_time = scad.inline("bouncing_ball_data[$t * 1000]")

#do some regular solid stuff with it
ball = translate(ball_pos_over_time)(sphere(ball_radius))
floor = background(cube([2000, 2000, 0.01]))

#render it with the pre computed data stored in the header
scad_render_to_file(ball + floor)

# I think if you really want to do something like this you could put the data
# into a seprate .scad file and include it into the main .scad file. You should
# also be able inject OpenSCAD functions (or modules) and use them...
#
# No clue what this could be good for, but....... I guess it might be possible
# to plug a -- more complex :-p -- physics engine into it and render animated
# movies....
#
# ....and print them with a 4d printer....?!?

