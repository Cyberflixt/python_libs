
from __future__ import annotations
import math

def vectorCoordProperty(i):
    def getx(self):
        return self.coords[i]
    
    def setx(self, value):
        self.coords[i] = value

    return property(getx, setx)

def propertySize():
    def gets(self):
        return (len(self.coords), 1)

    def sets(self):
        raise Exception('You cannot set the size of a vector')

    return property(gets, sets)

class Vector():

    def __init__(self, *coords):
        """Create a Vector(x, y, z, ...) or use a list or A dictionary, really anything"""
        
        if len(coords)==1:
            elem = coords[0]
            if isinstance(elem, dict):
                coords = self.dictToArr(elem)
            elif not (isinstance(elem, int) or isinstance(elem, float)):
                coords = elem.copy()
        
        self.coords = list(coords)

        # aliases
        self.ceil = self.__ceil__
        self.floor = self.__floor__
        self.mag = self.magnitude
        self.length = self.magnitude
        self.normalize = self.unit
        
        self.copy = self.clone
        self.new = self.clone

    def dictToArr(self, di):
        arr = []
        letters = 'xyzwabcdefghijklmnopqrstuv'
        for k in letters:
            if k in di:
                arr.append(di[k])
        return arr

    def __bool__(self):
        return True

    def __abs__(self):
        return Vector(*[abs(v) for v in self.coords])

    def __ceil__(self):
        return Vector(*[math.ceil(v) for v in self.coords])

    def __trunc__(self):
        return Vector(*[math.trunc(v) for v in self.coords])

    def __floor__(self):
        return Vector(*[math.floor(v) for v in self.coords])

    def __round__(self):
        return Vector(*[round(v) for v in self.coords])
    
    def __invert__(self):
        return Vector(*[~v for v in self.coords])

    def __str__(self):
        s = ''
        for v in self.coords:
            s = s+str(v)+', '
        return f'Vector{len(self.coords)}({s[:-2]})'

    ### math

    def varToVec(self, v):
        """Transforms a variable to a vector usable to the first given vector"""
        if isinstance(v,int) or isinstance(v,float):
            return Vector(*[v for i in range(len(self.coords))])
        elif isinstance(v,list):
            return Vector(*[v[i] for i in range(len(v))] )
        return v
    
    def __eq__(self, v):
        return hash(self)==v

    def __neg__(self):
        return Vector([-v for v in self.coords])

    def __and__(self, v):
        return bool(self) and bool(v)

    def __or__(self,v):
        return bool(self) or bool(v)

    def __mod__(self, v):
        v = self.varToVec(v)
        vals = []
        for i in range(max(len(self.coords), len(v.coords))):
            va = self.coords[i] if i<len(self.coords) else 0
            vb = v.coords[i] if i<len(v.coords) else 0
            if vb==0:
                vals.append(va)
            else:
                vals.append(va%vb)
        return Vector(*vals)

    def __mul__(self, v):
        vals = []
        # Multiply by whatever
        v = self.varToVec(v)
        for i in range(max(len(self.coords), len(v.coords))):
            va = self.coords[i] if i<len(self.coords) else 0
            vb = v.coords[i] if i<len(v.coords) else 0
            vals.append(va*vb)
        
        return Vector(*vals)

    def __rmul__(self, v):
        return self.varToVec(v) * self

    def __add__(self, v):
        v = self.varToVec(v)
        vals = []
        for i in range(max(len(self.coords), len(v.coords))):
            va = self.coords[i] if i<len(self.coords) else 0
            vb = v.coords[i] if i<len(v.coords) else 0
            vals.append(va+vb)
            
        return Vector(*vals)

    def __radd__(self, v):
        return self + v

    def __sub__(self, v):
        v = self.varToVec(v)
        vals = []
        for i in range(max(len(self.coords), len(v.coords))):
            va = self.coords[i] if i<len(self.coords) else 0
            vb = v.coords[i] if i<len(v.coords) else 0
            vals.append(va-vb)
            
        return Vector(*vals)

    def __rsub__(self, v):
        return self.varToVec(v) - self

    def __truediv__(self, v):
        v = self.varToVec(v)
        vals = []
        for i in range(max(len(self.coords), len(v.coords))):
            va = self.coords[i] if i<len(self.coords) else 0
            vb = v.coords[i] if i<len(v.coords) else 0
            vals.append(va/vb if vb!=0 else va)
            
        return Vector(*vals)

    def __rtruediv__(self, v):
        return self.varToVec(v)/self

    def __floordiv__(self, v):
        v = self.varToVec(v)
        vals = []
        for i in range(max(len(self.coords), len(v.coords))):
            va = self.coords[i] if i<len(self.coords) else 0
            vb = v.coords[i] if i<len(v.coords) else 0
            vals.append(va//vb if vb!=0 else va)
        
        return Vector(*vals)

    def __rfloordiv__(self, v):
        return self.varToVec(v)//self

    def __pow__(self, v):
        v = self.varToVec(v)
        vals = []
        for i in range(max(len(self.coords), len(v.coords))):
            va = self.coords[i] if i<len(self.coords) else 0
            vb = v.coords[i] if i<len(v.coords) else 0
            vals.append(va**vb)
        
        return Vector(*vals)

    def __rpow__(self, v):
        return self.varToVec(v)**self

    

    def __getitem__(self, k):
        if type(k)=='string':
            k = self.letters.index(k)
        return self.coords[k]

    def __setitem__(self, k, val):
        if type(k)=='string':
            k = self.letters.index(k)
        self.coords[k] = val

    def __len__(self): return len(self.coords)

    def __hash__(self):
        s = ','.join([str(float(v)) for v in self.coords])
        return hash(s)

    def __repr__(self):
        return str(self)

    def __lt__(self, v):
        v = self.varToVec(v)
        a = sum(self.coords)
        b = sum(v.coords)
        return a<b
    def __gt__(self, v):
        v = self.varToVec(v)
        a = sum(self.coords)
        b = sum(v.coords)
        return a>b
    def __le__(self, v):
        return self<v or self==v
    def __ge__(self, v):
        return self>v or self==v

    def append(self, *values) -> Vector:
        """Appends one or multiple new coordinate(s) to the vector:
        -> self"""
        a = self.copy()
        a.coords += values
        return a

    def magnitude(self, vector = None) -> float:
        """Length of a vector. *Optional: Give another vector to get the distance:
        -> magnitude: float"""
        vec = self
        if vector:
            vec -= vector
        return math.sqrt(sum(v*v for v in vec.coords))
    
    def unit(self) -> Vector:
        """Returns the unit vector (=normalized)
        -> unit: Vector"""
        return self/self.magnitude()

    def clone(self) -> Vector:
        """Creates an identical vector:
        -> new: Vector"""
        return Vector(self.coords)

    def bounds(*vectors):
        """Gets the minimum and maximum vectors of all given vectors:
        -> (min: Vector, max: Vector)"""
        if len(vectors)==1:
            vectors = vectors[0]
        
        maxVec = vectors[0].copy()
        minVec = vectors[0].copy()
        for vec in vectors:
            for i in range(len(minVec)):
                maxVec[i] = max(maxVec[i],vec[i])
                minVec[i] = min(minVec[i],vec[i])
        return minVec, maxVec

    def dot(*vectors) -> int:
        """Dot vectors of multiple vectors:
        -> scalar: int"""
        if len(vectors)==1:
            vecs = vectors[0]

        products = []
        for vec in vectors:
            for i in range(len(vec)):
                if i < len(products):
                    products[i] *= vec[i]
                else:
                    products += [vec[i]]
        
        return sum(products)

    def cross(a,b) -> Vector:
        """Cross product of 2 vectors:
        -> crossed: Vector"""

        av = a.coords
        bv = b.coords
        
        if len(a)==2:
            return av[0]*bv[1] - av[1]*bv[0]
        if len(a)==3:
            return Vector(
                av[1]*bv[2] - av[2]*bv[1],
                av[2]*bv[0] - av[0]*bv[2],
                av[0]*bv[1] - av[1]*bv[0]
                )
        raise Exception(f'Tried computing the cross product of a vector of {len(a)} and {len(b)} dimensions!')

    def angle(a,b) -> float:
        """Gets the angle between 2 vectors:
        -> radians: float"""

        dot = a.dot(b)
        maga = a.magnitude()
        magb = b.magnitude()
        radians = math.acos(dot/(maga*magb))
        return radians

    def project(a,b) -> Vector:
        """Gets the vector A projected ONTO B (same direction as b):
        -> projected: Vector"""

        # P = A * (A ° B) / |A|^2
        projected = a*( a.dot(b) / a.magnitude()**2 )
        return projected

    def orthogonal(a,b, approx=0) -> bool:
        """Are vectors A & B orthogonal ("perpendicular"):
        -> orthogonal: boolean"""
        return a.dot(b) <= approx

    def lerp(a,b,t) -> Vector:
        """Lerp 2 vectors A,B by a float T:
        -> lerped: Vector"""
        # a+(b-a)*t
        coords = [a.coords[i] + (b.coords[i]-a.coords[i])*t for i in range(len(a.coords))]
        return Vector(coords)

    def max(*vectors):
        """Returns a Vector with each highest components amongst given vectors:
        -> max: Vector"""
        maxVector = vectors[0].copy()
        for j in range(len(vectors)-1):
            vec = vectors[j+1]
            for i in range(len(vec)):
                if vec[i] > maxVector[i]:
                    maxVector[i] = vec[i]
        return maxVector
    
    def min(*vectors):
        """Returns a Vector with each highest components amongst given vectors:
        -> max: Vector"""
        minVector = vectors[0].copy()
        for j in range(len(vectors)-1):
            vec = vectors[j+1]
            for i in range(len(vec)):
                if vec[i] < minVector[i]:
                    minVector[i] = vec[i]
        return minVector

    def rotate(self, radians):
        '''Rotate vector counterclockwise
        -> rotated: Vector'''
        return Vector(
            self.x * math.cos(radians) - self.y * math.sin(radians),
            self.x * math.sin(radians) + self.y * math.cos(radians),
        )
    def rotateDeg(self, deg):
        '''Rotate vector counterclockwise
        -> rotated: Vector'''
        return self.rotate(math.radians(deg))

    def fromAngle(radians, length=1):
        '''Create a Vector from the given angle in radians'''
        return Vector(0, length).rotate(radians)
    def fromDeg(degrees, length=1):
        '''Create a Vector from the given angle in degrees'''
        return Vector.fromAngle(math.radians(degrees), length)

    ###################################

    x = vectorCoordProperty(0)
    y = vectorCoordProperty(1)
    z = vectorCoordProperty(2)
    w = vectorCoordProperty(3)

    size = propertySize()

    forward = [0,1]

if __name__ == '__main__':
    a = Vector(1,2)
    b = Vector(-2,0)
    c = Vector(3,-1)
    print('a =',a)
    print('b =',b)
    print('c =',c)
    print('\n_________________')
    print(a,'+',b,'=',a+b)
    print(a,'-',b,'=',a-b)
    print(a,'*',b,'=',a*b)
    print(a,'/',b,'=',a/b)
    print(a,'//',b,'=',a//b)
    print(a,'%',2,'=',a%2)
    print(a,'%',b,'=',a%b)
    print(a,'**',2,'=',a**2)
    print(a,'**',b,'=',a**b)
    print('abs(a) =', abs(a))
    print('cast bool(a) =', bool(a))
    print('math.floor(a) =', math.floor(a))
    print('math.trunc(a) =', math.trunc(a))
    print('math.ceil(a) =', math.ceil(a))
    print('round(a) =', round(a))
    print('~a =', ~a)
    print('str(a) =', str(a))
    print('a.dot(b) =', a.dot(b))
    print('a.cross(b) =', a.cross(b))
    print('Vector(2,0,3).cross(Vector(5,2,0)) =', Vector(2,0,3).cross(Vector(5,2,0)))
    print('a.angle(b) =', a.angle(b))
    print('a.project(b) =', a.project(b))
    print('a.orthogonal(b) =', a.orthogonal(b))
    print('a.magnitude() =', a.magnitude())
    print('a.magnitude(b) =', a.magnitude(b))
    print('a.unit() =', a.unit())
    print('a.append(5) =', a.append(5))
    print('a.lerp(b, 0.5) =', a.lerp(b, 0.5))
    print('a.bounds(c) =', a.bounds(c))
    print('a.max(b,c) =', a.max(b,c))
    print('a.min(b,c) =', a.min(b,c))
    print('a.rotate(math.pi/2) =', a.rotate(math.pi/2))
    print('a.rotateDeg(90) =', a.rotateDeg(90))
    print('cast varToVec(a, 5) =', a.varToVec(5))
    print('Vector.fromAngle(math.pi/2, 3) =', Vector.fromAngle(math.pi/2, 3))
    print('Vector.fromDeg(90, 2) =', Vector.fromDeg(90, 2))

    print('\n_________________')
    print('Dynamic attribution')
    print('a.x = -5\na[1] = 3')
    a.x = -5
    a[1] = 3
    print('a =',a)
    print('b.coords[0] = 1')
    b.coords[0] = 1
    print('b.coords =', b.coords)
    
    print('\n_________________')
    print('Comparison')
    print(a>b)
    print(a<b)
    print(a>=b)
    print(a<=b)
    print(a and b)
    print(a or b)

    print('\n_________________')
    print('Instancing')
    print(Vector())
    print(Vector(1))
    print(Vector([1,2]))
    print(Vector(Vector(1,2,3)))
    print(Vector({'x': 1, 'y': 2, 'z': 3, 'w': 4}))
    
    input()











