
class Matrix:
    def __init__(self, *args):
        if len(args)==1:
            self.vals = args[0]
        else:
            self.vals = args
        
        self.size = None

        self.id = self.identity

    def get_pos(self, i):
        return (i//self.size[1], i % self.size[1])

    def get_index(self, y,x):
        return self.size[1]*y + x

    def __getitem__(self, size):
        # Size to array
        if isinstance(size, int):
            if len(str(size))==2:
                size = str(size)
                size = (int(size[0]), int(size[1]))
            else:
                size = (size, size)

        
        if self.size == None:
            # Define size
            self.size = size
            return self
        else:
            # Get value
            i = self.get_index(*size)
            return self.vals[i]

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
        s = ''
        i = 0
        for y in range(self.size[0]):
            line = []
            if y==0:
                s += '/ '
            elif y==self.size[0]-1:
                s += '\\ '
            else:
                s += '| '
                
            for x in range(self.size[1]):
                v = str(self.vals[i])
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
            s += '\n'
        return s

    def __repr__(self):
        return str(self)

    def __mul__(a,b):
        if a.size[1] != b.size[0]:
            raise Exception("Multiplying matrices: Matrix A column and B row amount need to be the same.")
        
        r = Matrix([0 for i in range(b.size[0]*b.size[1])])[b.size]
        for y in range(b.size[0]):
            col_b = y*b.size[1]
            col_a = y*a.size[1]
            for x in range(b.size[1]):
                for i in range(b.size[0]):
                    r.vals[col_b+x] += a.vals[col_a+i] * b.vals[i*b.size[1]+x]
        return r

    def copy(self):
        return Matrix(*self.vals)[self.size]

    def __add__(a,b):
        vals = []

        sx = max(b.size[0],a.size[0])
        sy = max(b.size[1],a.size[1])
        
        for y in range(sx):
            col_a = y*a.size[1]
            col_b = y*b.size[1]
            for x in range(sy):
                v = 0
                if y<a.size[0] and x<a.size[1]:
                    v += a.vals[y*a.size[1]+x]
                if y<b.size[0] and x<b.size[1]:
                    v += b.vals[y*b.size[1]+x]
                    
                vals.append(v)
                
        return Matrix(vals)[sx,sy]
    
    def __sub__(a,b):
        vals = []

        sx = max(b.size[0],a.size[0])
        sy = max(b.size[1],a.size[1])
        
        for y in range(sx):
            col_a = y*a.size[1]
            col_b = y*b.size[1]
            for x in range(sy):
                v = 0
                if y<a.size[0] and x<a.size[1]:
                    v += a.vals[y*a.size[1]+x]
                if y<b.size[0] and x<b.size[1]:
                    v -= b.vals[y*b.size[1]+x]
                    
                vals.append(v)
                
        return Matrix(vals)[sx,sy]

    def identity(i):
        if isinstance(i, Matrix):
            i = max(i.size[0], i.size[1])
        
        vals = []
        for y in range(i):
            for x in range(i):
                if x==y:
                    vals.append(1)
                else:
                    vals.append(0)

        return Matrix(vals)[i,i]
        
            


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

print(a.id() * a)
