
import math

class Matrix:
    def __init__(self, *args):
        """Syntax: Matrix(values)[lines, columns]"""
        if len(args)==1:
            args = args[0]
        self.coords = list(args)
        
        self.size = None

        self.id = self.identity

    def get_pos(self, i: int) -> tuple:
        """Index to (Y,X) position"""
        return (i//self.size[1], i % self.size[1])

    def get_index(self, y: int, x: int) -> int:
        """(Y,X) Position to index"""
        return self.size[1]*y + x

    def __getitem__(self, size):
        if self.size == None:
            # Size to array
            if isinstance(size, int):
                if len(str(size))==2:
                    size = str(size)
                    size = (int(size[0]), int(size[1]))
                else:
                    size = (size, size)
            
            # Define size
            self.size = size
            return self
        else:
            # Get value
            if not isinstance(size, int):
                size = self.get_index(*size)
            return self.coords[size]

    def __setitem__(self, i, v):
        if not isinstance(i, int):
            i = self.get_index(*i)
        self.coords[i] = v

    def __str__(self):
        # Get minimum spaces for columns
        spaces_col = []
        i = 0
        for x in range(self.size[1]):
            v = 0
            for y in range(self.size[0]):
                le = len(str(self[y,x]))
                if le>v:
                    v = le
                i += 1
            spaces_col.append(v)

        # Put values in string
        lines = []
        i = 0
        for y in range(self.size[0]):
            line = []
            s = ''
            if y==0:
                s = '/ '
            elif y==self.size[0]-1:
                s = '\\ '
            else:
                s = '| '
                
            for x in range(self.size[1]):
                v = str(self.coords[i])
                spaces = spaces_col[x]
                while len(v)<spaces:
                    v += ' '
                line.append(v)
                i += 1
            s += ', '.join(line)
            
            if y==0:
                s += ' \\'
            elif y==self.size[0]-1:
                s += ' /'
            else:
                s += ' |'
            lines.append(s)

        # center prefix between lines

        prefix = 'Matrix'
        suffix = f'[{self.size[0]},{self.size[1]}]'
        cen = len(lines)//2
        
        s = ''
        for i in range(len(lines)):
            line = lines[i]
            s += '\n'
            if i==cen:
                s += prefix+line+suffix
            else:
                for _ in range(len(prefix)):
                    s += ' '
                s += line
        return s

    def __repr__(self):
        return str(self)

    def __mul__(a,b):
        ty =b.__class__.__name__
        if ty=='int' or ty=='float':
            r = Matrix([v*b for v in a.coords])[a.size]

        else:
            if ty=='Line':
                b.a = a*b.a
                b.b = a*b.b
                return b
            else:
                if a.size[1] != b.size[0]:
                    raise Exception("Multiplying matrices: Matrix A column and B row amount need to be the same.")
                
                r = Matrix([0 for i in range(b.size[0]*b.size[1])])[b.size]
                for y in range(b.size[0]):
                    col_b = y*b.size[1]
                    col_a = y*a.size[1]
                    for x in range(b.size[1]):
                        for i in range(b.size[0]):
                            r.coords[col_b+x] += a.coords[col_a+i] * b.coords[i*b.size[1]+x]
        return r

    def copy(self) -> 'Matrix':
        """Clones the matrix"""
        return Matrix(*self.coords)[self.size]

    def __add__(a,b):
        coords = []

        sx = max(b.size[0],a.size[0])
        sy = max(b.size[1],a.size[1])
        
        for y in range(sx):
            col_a = y*a.size[1]
            col_b = y*b.size[1]
            for x in range(sy):
                v = 0
                if y<a.size[0] and x<a.size[1]:
                    v += a.coords[y*a.size[1]+x]
                if y<b.size[0] and x<b.size[1]:
                    v += b.coords[y*b.size[1]+x]
                    
                coords.append(v)
                
        return Matrix(coords)[sx,sy]
    
    def __sub__(a,b):
        coords = []

        sx = max(b.size[0],a.size[0])
        sy = max(b.size[1],a.size[1])
        
        for y in range(sx):
            col_a = y*a.size[1]
            col_b = y*b.size[1]
            for x in range(sy):
                v = 0
                if y<a.size[0] and x<a.size[1]:
                    v += a.coords[y*a.size[1]+x]
                if y<b.size[0] and x<b.size[1]:
                    v -= b.coords[y*b.size[1]+x]
                    
                coords.append(v)
                
        return Matrix(coords)[sx,sy]

    def __truediv__(self, v):
        if isinstance(v, int) or isinstance(v, float):
            coords = [x/v for x in self.coords]   
            return Matrix(coords)[self.size]

    def identity(i: int) -> 'Matrix':
        """Returns the identity matrix of dimension i"""
        if isinstance(i, Matrix):
            i = max(i.size[0], i.size[1])
        
        coords = []
        for y in range(i):
            for x in range(i):
                if x==y:
                    coords.append(1)
                else:
                    coords.append(0)

        return Matrix(coords)[i,i]

    def euler_x(v):
        cos = math.cos(v)
        sin = math.sin(v)
        
        r = Matrix(
            1,   0,   0,
            0, cos,-sin,
            0, sin, cos,
        )[3,3]
        return r
    
    def euler_y(v):
        cos = math.cos(v)
        sin = math.sin(v)
        
        r = Matrix(
            cos, 0, sin,
            0,   1,   0,
            -sin,0, cos,
        )[3,3]
        return r
    
    def euler_z(v):
        cos = math.cos(v)
        sin = math.sin(v)
        
        r = Matrix(
            cos,-sin, 0,
            sin, cos, 0,
            0,     0, 1,
        )[3,3]
        return r
    

    def euler(vec):
        """3D rotation matrix with given vectors for angles"""

        #https://en.wikipedia.org/wiki/Rotation_matrix
        
        rx = self.euler_x(vec[0])
        ry = self.euler_y(vec[1])
        rz = self.euler_z(vec[2])

        """
        vx = vec[0]
        vy = vec[1]
        vz = vec[2]
        
        cosx = math.cos(vx)
        sinx = math.sin(vx)

        cosy = math.cos(vy)
        siny = math.sin(vy)

        cosz = math.cos(vz)
        sinz = math.sin(vz)
        
        rx = Matrix(
            1,    0,    0,
            0, cosx,-sinx,
            0, sinx, cosx,
        )[3,3]
        ry = Matrix(
            cosy, 0, siny,
            0,    1,    0,
            -siny,0, cosy,
        )[3,3]
        rz = Matrix(
            cosz,-sinz, 0,
            sinz, cosz, 0,
            0,       0, 1,
        )[3,3]
        """

        rotator = rz*ry*rx
        return rotator

    def inverse(self):
        """Returns the inverse matrix"""

        # Source:
        # https://www.researchgate.net/publication/220337322

        if self.size[0] != self.size[1]:
            raise Exception('Can only get the inverse of a square matrix!')

        coords = [*self.coords]
        size = self.size[0]
        
        det = 1
        
        for p in range(size):
            pivot = coords[size*p+p]
            det *= pivot
            
            if abs(pivot) < 1e-5:
                return 0
            
            for i in range(size):
                coords[i*size+p] /= -pivot
                
            for i in range(size):
                if i != p:
                    for j in range(size):
                        if j != p:
                            coords[i*size+j] += coords[p*size+j] * coords[i*size+p]
            
            for j in range(size):
                coords[p*size+j] /= pivot
            coords[p*size+p] = 1/pivot

        inversed = Matrix(coords)[size,size]
        #return det, inversed
        return inversed

    def axis_rad(axis, rad):
        """Rotation matrix around an axis(x,y,z) of angle in RADIANS"""
        # https://en.wikipedia.org/wiki/Rotation_matrix
        
        x = axis[0]
        y = axis[1]
        z = axis[2]
        
        mag = math.sqrt(x**2 + y**2 + z**2)
        ux = axis[0]/mag
        uy = axis[1]/mag
        uz = axis[2]/mag
        
        cos = math.cos(rad)
        sin = math.sin(rad)
        mcos = 1-cos
        
        return Matrix(
            cos+ux*mcos   , x*y*mcos-z*sin, x*z*mcos+y*sin,
            y*x*mcos+z*sin, cos+uy*mcos   , y*z*mcos-x*sin,
            z*x*mcos-y*sin, z*y*mcos+x*sin, cos+uz*mcos   ,
        )[3,3]

    def axis_angle(axis, deg):
        """Rotation matrix around an axis(x,y,z) of angle in DEGREES"""
        return Matrix.axis_rad(axis, math.radians(deg))

"""
a = Matrix(
    0,1,2,
    3,4,5,
    6,7,8,
)[3,3]

b = Matrix(
    1,2,
    3,4,
    5,6,
)[3,2]

i = Matrix.identity(3)

print(i * a)
print(a.__class__.__name__)
"""

"""
A = Matrix(
     2, 1, 3,
     1, 3,-3,
    -2, 4, 4,
)[3,3]

print(A.inverse())
"""


