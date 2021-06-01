# ======================================================
# = add relative path to the solid package to sys.path =
# ======================================================
import sys
from pathlib import Path
solidPath = Path(__file__).absolute().parent.parent.parent.as_posix()
sys.path.append(solidPath)
#==================================================
import numpy as np

from solid import *

ball_radius = 100

def get_bouncing_ball_data(pos=np.array([0.0, 0.0, 0.0]), vel=np.array([5.0, 5.0, 100.0])):
    data = []
    gravity = np.array([0.0, 0.0, -4.0])
    for t in range(1000):
        vel = (vel + gravity) * 0.998
        pos += vel
        if pos[2] < ball_radius:
            vel[2] = vel[2] * -1
            pos[2] = ball_radius

        data.append(pos.tolist())

    return data

ball_data = f'bouncing_ball_data = {get_bouncing_ball_data()};'

ball_pos_over_time = scad_inline("bouncing_ball_data[$t * 1000]")

ball = translate(ball_pos_over_time)(sphere(ball_radius))
floor = background(cube([2000, 2000, 0.01]))

scad_render_to_file(ball + floor, file_header=ball_data)

