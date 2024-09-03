
from cyutils.ascii.ascii3d import *

### SCENE

scene = Ascii_Canvas(90, 30)

cube = Model(
    Vector(-1,-1,-1),
    Vector(-1,-1,1),
    Vector(-1,1,-1),
    Vector(1,-1,-1),
    Vector(1,1,-1),
    Vector(1,-1,1),
    Vector(-1,1,1),
    Vector(1,1,1),
    
    Vector(0,0,0),
    Vector(0,-1,0),
    Vector(1,0,0),
    
    Line(Vector(-1,-1,-1), Vector(1,1,1)),
)
cube2 = Model(
    Vector(-1,-1,-1),
    Vector(-1,-1,1),
    Vector(-1,1,-1),
    Vector(1,-1,-1),
    Vector(1,1,-1),
    Vector(1,-1,1),
    Vector(-1,1,1),
    Vector(1,1,1),
).move(Vector(5,0,4)).default()

cube3 = Model(
    Line(Vector(-1,-1,-1), Vector(-1,-1,1)),
    Line(Vector(-1,-1,1),  Vector(1,-1,1)),
    Line(Vector(1,-1,1),   Vector(1,-1,-1)),
    Line(Vector(1,-1,-1),  Vector(-1,-1,-1)),
    
    Line(Vector(-1,1,-1),  Vector(-1,1,1)),
    Line(Vector(-1,1,1),   Vector(1,1,1)),
    Line(Vector(1,1,1),    Vector(1,1,-1)),
    Line(Vector(1,1,-1),   Vector(-1,1,-1)),
    
    Line(Vector(1,-1,1),   Vector(1,1,1)),
    Line(Vector(1,-1,-1),  Vector(1,1,-1)),
    Line(Vector(-1,-1,1),  Vector(-1,1,1)),
    Line(Vector(-1,-1,-1), Vector(-1,1,-1)),
)

def vol_eval_pyramide(x,y,z):
    return -y-abs(x)-abs(z)

def vol_eval_ball(x,y,z):
    return -x**2-y**2-z**2+1

def vol_eval_triangle(x,y,z):
    return x-y

def vol_eval_a(x,y,z):
    return math.cos(x+z)-math.cos(y)

vol_a = scene + Volumetric(vol_eval_pyramide, (0,0,0), (5,5,5), 2)
vol_b = scene + Volumetric(vol_eval_ball,    (10,0,0), (5,5,5), 2)
vol_c = scene + Volumetric(vol_eval_triangle,(20,0,0), (5,5,5), 2)

def update(delta):
    cube.rotate(Vector(delta, 0, delta))
    cube2.rotate(Vector(0, delta, 0))

    cube3().rotate_around_axis(Vector(0,1,0), time.time())
    
    scene.display_world_points_to_canvas(* cube.vertices)
    scene.display_world_points_to_canvas(* cube2.vertices)
    scene.display_world_points_to_canvas(* cube3.vertices)
    

scene.update(update)
