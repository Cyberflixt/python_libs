
"""

https://stackoverflow.com/questions/724219
https://en.wikipedia.org/wiki/Rotation_matrix

"""

import math
import sys
import os
import time

from ctypes import windll

# local
from matrix import *
from vectors import Vector
from input_simple import Keyboard, Mouse



""" CLASSES """



class Ascii_Canvas:
    def __init__(self, width, height):
        
        # SETTINGS
        
        self.pos = Vector(0,0,-5)
        
        self.auto_clear = False
        self.fullscreen = True
        self.chars = ['.',':','/','#']

        self.sens_rot = -5
        self.sens_move = 5

        self.keyboard = Keyboard()
        self.mouse = Mouse()

        # INIT

        self.canvas_lines = []
        
        self.renders = 0
        self.rotation = None
        self.delta = .03
        self.run = False
        self.scene = []

        self.refresh_screen_size()
        self.set_size(width, height)

    def refresh_screen_size(self):
        self.screen_size = (
            windll.user32.GetSystemMetrics(0),
            windll.user32.GetSystemMetrics(1),
        )
        
    def mouse_center(self):
        mp = self.mouse.get()
        return (mp[0] - self.screen_size[0]//2, mp[1] - self.screen_size[1]//2)

    def update_controls(self):
        # ROTATE: Mouse controls
        mp = self.mouse_center()
        fac = self.sens_rot*.001
        ry = Matrix.euler_y(mp[0]*fac)
        self.rotation = Matrix.euler_x(mp[1]*fac)*ry
        inv = self.rotation.inverse()

        # MOVE: Key controls
        kb = self.keyboard
        z = 1 if kb.get('w') or kb.get('z') else 0
        z -= 1 if kb.get('s') else 0
        x = 1 if kb.get('d') else 0
        x -= 1 if kb.get('a') or kb.get('q') else 0
        y = 1 if kb.get('e') else 0
        y -= 1 if kb.get('c') else 0
        fac = self.delta * self.sens_move
        move = Vector(x*fac, y*fac, z*fac)

        self.pos += inv*move
        

    def set_size(self, x=0, y=0):
        if self.fullscreen:
            size = self.get_size_fullscreen()
            if size:
                x,y = size
        self.width = max(x,1)
        self.height = max(y,1)
        self.refresh_ratio()

    def refresh_ratio(self):
        char_deform = 2 # characters in the cmd aren't squares
        self.ratio = self.width/self.height
        self.ratio_fac = char_deform*(1/self.ratio)

    def get_size_fullscreen(self):
        try:
            x,y = os.get_terminal_size()
            return x,y
        except Exception:
            pass

    def pos_to_int(self, pos):
        return pos[1]*self.width + pos[0]

    def int_to_pos(self, i):
        return [i%self.width, i//self.width]

    def new(self):
        char = self.chars[0]
        self.canvas_lines = []
        for y in range(self.height):
            line = []
            for x in range(self.width):
                line.append(char)
            self.canvas_lines.append(line)

    def __str__(self):
        s = ''
        for line in self.canvas_lines:
            if self.fullscreen:
                s += ''.join(line)
            else:
                s += '\n'+''.join(line)
        
        return s

    def __repr__(self):
        return str(self)

    def print(self):
        if self.auto_clear and self.renders % 1000 == 0:
            os.system('cls')
        sys.stdout.flush()
        sys.stdout.write(str(self))
        self.renders += 1
        

    def display_screen_point_to_canvas(self, v):
        char = self.chars[len(self.chars)-1]
        if 0<v[0]<self.width and 0<v[1]<self.height:
            self.canvas_lines[v[1]][v[0]] = char

    def display_screen_points_to_canvas(self, *points):
        for v in points:
            self.display_screen_point_to_canvas(v)

    def world_point_to_canvas(self, v):
        # Camera rotation
        if self.rotation:
            v = self.rotation*(v-self.pos)+self.pos
            
        z = v[2]-self.pos[2]
        if z==0:
            z += .01
        x = int(((v[0]-self.pos[0])/z*self.ratio_fac + .5) *self.width)
        y = int((.5 - (v[1]-self.pos[1])/z) *self.height)
        return (x,y,z)

    def display_world_points_to_canvas(self, *points):
        char = self.chars[len(self.chars)-1]
        for v in points:
            if isinstance(v, Line):
                a = self.world_point_to_canvas(v.a)
                b = self.world_point_to_canvas(v.b)
                if a[2]>0 and b[2]>0:
                    vs = Line.pixels_3D(a,b)
                    self.display_screen_points_to_canvas(*vs)
            else:
                x,y,z = self.world_point_to_canvas(v)
                if z>0 and 0<x<self.width and 0<y<self.height:
                    self.canvas_lines[y][x] = char
                    
    def refresh_win(self):
        if self.fullscreen:
            self.refresh_screen_size()
            self.set_size()
            
    def update(self, callback = None):
        """Loop the display cycle and calls the given funcion before displaying the canvas"""
        
        self.run = True
        bt = time.time()
        while self.run:
            time.sleep(.02)
            t = time.time()
            self.delta = t-bt
            bt = t

            # update

            #self.refresh_win()
            self.update_controls()
            self.new()

            for elem in self.scene:
                if isinstance(elem, Volumetric):
                    pts = elem.get_points()
                else:
                    pts = elem.vertices
                scene.display_world_points_to_canvas(*pts)

            if callback:
                callback(self.delta)
            
            self.print()

    def add(self, *elems):
        for elem in elems:
            self.scene.append(elem)
            
        return self

    def __add__(self, b):
        self.add(b)
        return b

class Model:
    def __init__(self, *args):
        self.vertices = args
        self.default()

    def default(self):
        """Update the default vertices to the current ones"""

        r = []
        for elem in self.vertices:
            if isinstance(elem, Line):
                r.append(elem.default())
            else:
                # copy vector
                r.append(elem.copy())
        
        self.base = r
        return self

    def reset(self):
        """Reset the vertices to the default ones to avoid mathematical approximation errors"""

        r = []
        for elem in self.base:
            if isinstance(elem, Line):
                r.append(elem.reset())
            else:
                # copy vector
                r.append(elem.copy())
        
        self.vertices = r
        return self
        
    def __call__(self):
        """Reset the vertices to the default ones to avoid mathematical approximation errors"""
        return self.reset()

    def get_bounds(self):
        f = self.vertices[0]
        if isinstance(f, Line):
            f = f.a
        a = f.copy()
        b = f.copy()

        def check(v):
            for i in range(3):
                if v[i] < a[i]:
                    a[i] = v[i]
                if v[i] > b[i]:
                    b[i] = v[i]

        for v in self.vertices:
            if isinstance(v, Line):
                check(v.a)
                check(v.b)
            else:
                check(v)
        
        return a,b

    def center(self):
        a,b = self.get_bounds()
        c = (a+b)/2
        return c

    def scale(self, factor):
        cen = self.center()
        
        new = []
        for v in self.vertices:
            delta = v-cen
            new.append(cen + delta*factor)
        self.vertices = new
        
        return self

    def move(self, add):
        new = []
        for v in self.vertices:
            new.append(v+add)
        self.vertices = new
        
        return self

    def __mul__(self, b):
        new = []
        for v in self.vertices:
            if isinstance(b,Matrix):
                new.append(b*v)
            else:
                new.append(v*b)
        self.vertices = new

        return self

    def apply_matrix(self, ma, cen = 0):
        vecs = [ma*(v-cen) for v in self.vertices]
        self.vertices = [v+cen for v in vecs]

        return self

    def rotate_around_point(self, v, cen):
        """Rotate the model with the angles(x,y,z) with a given center(x,y,z)"""

        rot = Matrix.euler(v)
        return self.apply_matrix(rot, cen)

    def rotate(self, v):
        """Rotate the model with the angles(x,y,z) around its center"""
        
        cen = self.center()
        return self.rotate_around_point(v, cen)

    def rotate_around_axis(self, v, deg):
        """Rotate the model along an axis(x,y,z) with a angle in DEGREES"""

        rot = Matrix.axis_angle(v, deg)
        cen = self.center()
        return self.apply_matrix(rot, cen)

class Line:
    def __init__(self, a,b):
        self.a = a
        self.b = b
        self.default()

    def default(self):
        """Update the default vertices to the current ones"""
        self.ba = self.a.copy()
        self.bb = self.b.copy()
        return self

    def reset(self):
        """Reset the vertices to the default ones to avoid mathematical approximation errors"""
        self.a = self.ba.copy()
        self.b = self.bb.copy()
        return self
        

    def __str__(self):
        return f'Line ({self.a} <-> {self.b})'

    def __repr__(self):
        return str(self)

    def pixels(a,b):
        dx = b[0]-a[0]
        dy = b[1]-a[1]
        ma = max(abs(dx), abs(dy))

        res = []
        for i in range(ma):
            alpha = i/ma
            res.append(Vector(
                int(a[0]+(b[0]-a[1])*alpha),
                int(a[1]+(b[1]-a[1])*alpha),
            ))
        return res
    
    def pixels_3D(a,b):
        dx = b[0]-a[0]
        dy = b[1]-a[1]
        ma = max(abs(dx), abs(dy))

        res = []
        for i in range(ma):
            alpha = i/ma
            if int(a[2]+(b[2]-a[2])*alpha)>0:
                res.append(Vector(
                    int(a[0]+(b[0]-a[0])*alpha),
                    int(a[1]+(b[1]-a[1])*alpha),
                ))
        return res

    def __mul__(self, b):
        self.a = self.a*b
        self.b = self.b*b
        return self

    def __add__(self, b):
        self.a = self.a+b
        self.b = self.b+b
        return self

    def __sub__(self, b):
        self.a = self.a-b
        self.b = self.b-b
        return self

class Volumetric:
    def __init__(self, equation, pos, size, res = 1, world = False):
        self.eval = equation
        self.world = world
        self.size = size
        self.pos = pos
        self.res = res

    def get_points(self):
        r = []
        
        res = self.res
        s = self.size

        # Anchor
        sx = -s[0]/2
        sy = -s[1]/2
        sz = -s[2]/2
        ax = self.pos[0]
        ay = self.pos[1]
        az = self.pos[2]
        
        for x in range(s[0]*res):
            x/=res
            for y in range(s[1]*res):
                y/=res
                for z in range(s[2]*res):
                    z/=res
                    
                    lo = Vector(
                        x-sx,
                        y-sy,
                        z-sy,
                    )
                    glo = Vector(
                        x+ax-sx,
                        y+ay-sy,
                        z+az-sy,
                    )
                    if self.world:
                        v = self.eval(*glo)
                    else:
                        v = self.eval(*lo)
                    
                    if v==True or v>0:
                        r.append(glo)
        return r

### SCENE

scene = Ascii_Canvas(90, 30)

"""
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
"""

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
    pass
    #cube.rotate(Vector(delta, 0, delta))
    #cube2.rotate(Vector(0, delta, 0))

    #cube3().rotate_around_axis(Vector(0,1,0), time.time()*100)
    
    #canvas.display_world_points_to_canvas(* cube.vertices)
    #canvas.display_world_points_to_canvas(* cube2.vertices)
    #scene.display_world_points_to_canvas(* cube3.vertices)
    

scene.update(update)
