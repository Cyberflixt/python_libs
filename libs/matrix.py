
class Matrix:
    def __init__(self, *args):
        if len(args)==1:
            self.vals = args[0]
        else:
            self.vals = args
        
        self.size = None

    def get_index(self, x,y):
        return x + self.size[0]*y

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
                line.append(str(self.vals[i]))
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
            col = y*b.size[1]
            for x in range(b.size[1]):
                for i in range(b.size[0]):
                    r.vals[col+x] += a.vals[col+i] * b.vals[x+i*b.size[1]]
        return r
            


a = Matrix(
    0,1,2,
    3,4,5,
    6,7,8,
)[3,4]

b = Matrix(
    1,2,
    3,4,
    5,6,
)[3,2]

print(a*b)
#print(a)
