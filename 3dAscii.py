
import math
from libs.matrix import Matrix
from libs.vectors import Vector



def deg_to_rad(deg):
    return deg / 180 * math.pi



angle = deg_to_rad(90)
fov = 1 / math.tan(angle / 2)
aspect_ratio = 16/9

far = 100
near = .1

clip_matrix = Matrix(
    fov*aspect_ratio, 0, 0, 0,
    0, fov, 0, 0,
    0, 0, (far+near)/(far-near), 1,
    0, 0, (2*near*far)/(near-far), 0,
)[4,4]

point_a = Vector(0,0,0)
point_b = Vector(1,0,0)
point_c = Vector(0,0,1)
point_d = Vector(1,0,1)

print(clip_matrix)

