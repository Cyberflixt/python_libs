
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
                size = (len(self.coords)//size, size)
            
            # Define size
            self.size = size
            return self
        else:
            # Get value
            if isinstance(size, int):
                return self.coords[size]
            
            return self.coords[self.get_index(*size)]

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
        if isinstance(b, int) or isinstance(b, float):
            r = Matrix([v*b for v in a.coords])[a.size]

        elif isinstance(b, Matrix):
            if a.size[1] != b.size[0]:
                raise ValueError("Multiplying matrices: Matrix A column and B row lengths need to be the same.")
                
            r = Matrix([0 for i in range(b.size[0]*b.size[1])])[b.size]
            for y in range(b.size[0]):
                col_b = y*b.size[1]
                col_a = y*a.size[1]
                for x in range(b.size[1]):
                    for i in range(b.size[0]):
                        r.coords[col_b+x] += a.coords[col_a+i] * b.coords[i*b.size[1]+x]
        else:
            ty = b.__class__.__name__
            if ty=='Line':
                b.a = a*b.a
                b.b = a*b.b
                return b
            else:
                # Handle as list or vector
                if a.size[1] != len(b):
                    raise ValueError("Multiplying matrices: Matrix A column and B length need to be the same.")

                r = Matrix([0 for i in range(len(b))])[len(b), 1]
                for y in range(len(b)):
                    iy = y*a.size[1]
                    for x in range(a.size[0]):
                        r.coords[y] += a.coords[iy + x] * b[x]
                return r
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
                # add A value if in matrix
                if y<a.size[0] and x<a.size[1]:
                    v += a.coords[y*a.size[1]+x]
                # add B value if in matrix
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
                # add A value if in matrix
                if y<a.size[0] and x<a.size[1]:
                    v += a.coords[y*a.size[1]+x]
                # subtract B value if in matrix
                if y<b.size[0] and x<b.size[1]:
                    v -= b.coords[y*b.size[1]+x]
                    
                coords.append(v)
                
        return Matrix(coords)[sx,sy]

    def __truediv__(self, v):
        if isinstance(v, int) or isinstance(v, float):
            coords = [x/v for x in self.coords]   
            return Matrix(coords)[self.size]

    def __pow__(self, v):
        r = self
        for i in range(v-1):
            r *= r
        return r

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
        # src: https://en.wikipedia.org/wiki/Rotation_matrix
        
        rx = Matrix.euler_x(vec[0])
        ry = Matrix.euler_y(vec[1])
        rz = Matrix.euler_z(vec[2])

        rotator = rz*ry*rx
        return rotator

    def inverse(self):
        """Returns the inverse matrix"""
        # src: ttps://www.researchgate.net/publication/220337322

        if self.size[0] != self.size[1]:
            raise Exception('Can only get the inverse of a square matrix!')

        coords = [*self.coords]
        size = self.size[0]
        
        #det = 1
        
        for p in range(size):
            pivot = coords[size*p+p]
            #det *= pivot
            
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

    def axis_deg(axis, deg):
        """Rotation matrix around an axis(x,y,z) of angle in DEGREES"""
        return Matrix.axis_rad(axis, math.radians(deg))

    def remove_column(self, x: int):
        """Removes a column from the matrix at a given abscissa"""
        h,w = self.size
        coords = []
        
        for i in range(len(self.coords)):
            if i%w != x:
                coords.append(self.coords[i])
        return Matrix(coords)[h,w-1]

    def remove_row(self, y: int):
        """Removes a row from the matrix at a given ordinate"""
        h,w = self.size
        coords = []
        
        for i in range(len(self.coords)):
            if i//w != y:
                coords.append(self.coords[i])
        return Matrix(coords)[h-1,w]

    def __neg__(self):
        coords = [-v for v in self.coords]
        return Matrix(coords)[self.size]

    def __floor__(self):
        coords = [math.floor(v) for v in self.coords]
        return Matrix(coords)[self.size]

    def __ceil__(self):
        coords = [math.ceil(v) for v in self.coords]
        return Matrix(coords)[self.size]

    def __trunc__(self):
        coords = [math.trunc(v) for v in self.coords]
        return Matrix(coords)[self.size]

    def __round__(self):
        coords = [round(v) for v in self.coords]
        return Matrix(coords)[self.size]

    def __abs__(self):
        coords = [abs(v) for v in self.coords]
        return Matrix(coords)[self.size]

    def __invert__(self):
        coords = [~v for v in self.coords]
        return Matrix(coords)[self.size]

    def index(self, v):
        return self.coords.index(v)



if __name__ == '__main__':
    a = Matrix(
        0,1,2,
        3,4,5,
        6,7,8,
    )[3,3]

    b = Matrix(
        1,2,
        3,4,
        5,6,
        7,8,
        9,10,
    )[2]

    
    c = Matrix(1,2,3)[3,1]
    print(c)
    print(a * [1,2,3])

    print(-a)

    i = Matrix.identity(3)

    print('a',a)
    print('I(3)*a',i * a)

    A = Matrix(
         2, 1, 3,
         1, 3,-3,
        -2, 4, 4,
    )[3,3]

    print('a^-1',A.inverse())

    print('a*a',a*a)
    print('a**2',a**2)
    print('a**4',a**4)

    print(a.remove_column(1))
    print(a.remove_row(1))


