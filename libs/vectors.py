
from __future__ import annotations
import math

def vectorCoordProperty(i):
    def getx(self):
        #print('getting',i)
        return self.coords[i]
    
    def setx(self, value):
        #print('setting',i,'to',value)
        self.coords[i] = value

    return property(getx, setx)

class Vector():

    def __init__(self, *coords):
        """Create a Vector(x, y, z, ...) or use a list or A dictionary, really anything"""
        #self.letters = 'xyzwabcdefghijklmnopqrstuv'
        
        if len(coords)==1:
            coords = coords[0]
            if isinstance(coords, dict):
                coords = self.dictToArr(coords)
                #coords = coords.values()
            else:
                coords = coords.copy()
        
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
        """
        v = self.varToVec(v)
        b = True
        for i in range(max(len(self.coords), len(v.coords))):
            va = self.coords[i] if i<len(self.coords) else 0
            vb = v.coords[i] if i<len(v.coords) else 0
            b = b and (va==vb)
        return b
        """
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
        v = self.varToVec(v)
        vals = []
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

    def __rlt__(self, v):
        a = var
        print(0)
        return 345678

    def append(self, *values) -> Vector:
        """Appends one or multiple new coordinate(s) to the vector:
        -> self"""
        self.coords += values
        return self

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

        if len(a)==3:
            return Vector(
                a.y*b.z - a.z*b.y,
                a.z*b.x - a.x*b.z,
                a.x*b.y - a.y*b.x
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
        for vec in vectors[1:]:
            for i in range(len(vec)):
                if vec[i]>maxVector[i]:
                    maxVector[i] = vec[i]
        return maxVector
    
    def min(*vectors):
        """Returns a Vector with each highest components amongst given vectors:
        -> max: Vector"""
        minVector = vectors[0].copy()
        for vec in vectors[1:]:
            for i in range(len(vec)):
                if vec[i]<minVector[i]:
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

    forward = [0,1]

class Pointer():
    def __init__(self, *args, **kwargs):
        '''Create a Pointer with given Position and Rotation (radians)'''
        if len(args)==1:
            args = args[0]
        
        self.pos = Vector(args[0])
        self.rot = args[1]
        
        for k in kwargs:
            v = kwargs[k]
            k = k.lower()
            if isinstance(v,str):
                v = v.lower()
            
            if k=='unit' and v=='deg':
                self.deg = True
    
    # magic methods
    
    def __getitem__(self, k):
        if k==0:
            return self.pos
        return self.rot

    def __setitem__(self, k, val):
        if k==0:
            self.pos = val
        else:
            self.rot = val
            
    def __str__(self):
        return f'Pointer(pos: {self.pos}, rot: {self.rot}))'
    def __repr__(self):
        return str(self)

    # methods

    def getRot(self):
        if self.deg:
            return math.radians(self.rot)
        return self.rot

    def move(self, vec):
        self.pos += Vector(vec).rotate(self.getRot())
        return self

    def forward(self, v):
        #self.move(Vector.forward)
        self.pos += Vector.fromAngle(self.getRot(), v)
        #self.pos += Vector.fromDeg(self.rot, v)
        return self

    def rotate(self, v):
        self.rot += v
        return self

class PointerDeg():
    def __init__(self, *args, **kwargs):
        self = Pointer(*args, **kwargs, unit='deg')

a = Vector(2,4)
#b = Vector(3,8)











