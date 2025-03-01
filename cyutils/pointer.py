
import cyutils.Vector

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
