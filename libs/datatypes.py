
import time

class LinkedIter():
    def __init__(self, start):
        self.loop = start

    def __next__(self):
        if self.loop:
            v = self.loop.val
            self.loop = self.loop.next
            return v
        raise StopIteration

class LinkedCell():
    def __init__(self, val):
        self.val = val
        self.next = None

    def last(self):
        while self.next:
            self = self.next
        return self
    
    def append(self, val):
        new = LinkedCell(val)
        
        last = self.last()
        last.next = new
        
    def concat(self, new):
        last = self.last()
        last.next = new

    def prepend(self, val):
        new = LinkedCell(self.val)
        
        new.next = self.next
        self.val = val
        self.next = new

    def insert(self, i, val):
        new = LinkedCell(val)
        for _ in range(i-1):
            self = self.next
        
        self.next, new.next = new, self.next
        

    def delend(self):
        while self.next.next:
            self = self.next
        self.next = None

    def delstart(self):
        self.val = self.next.val
        self.next = self.next.next

    def __str__(self):
        s = 'LinkedList['
        cell = self
        while cell:
            s += str(cell.val)
            if cell.next:
                s += ', '
            cell = cell.next
        return s+f']'
    
    def __repr__(self):
        return str(self)

    def __getitem__(self, i):
        for _ in range(i):
            self = self.next
        return self.val

    def __setitem__(self, i, val):
        for _ in range(i):
            self = self.next
        self.val = val

    def __len__(self):
        n = 1
        while self := self.next:
            n += 1
        return n

    def __iter__(self):
        return LinkedIter(self)

    def __add__(self, b):
        self.append(b)

    def list(self):
        li = []
        while self:
            self = self.next
            li.append(self.val)
        return li
        
    def nodeList(self):
        li = []
        while self:
            li.append(self)
            self = self.next
        return li

    def reverse(self):
        li = self.list()
        l = len(li)
        
        for i in range(l-1,0,-1):
            print(i)
            li[i].val = li[i-1]
        li[1].next = None
        print('done')
        

class LinkedList(LinkedCell):
    def __init__(self, *vals):
        if len(vals)>0:
            LinkedCell.__init__(self, vals[0])
            
            cell = self
            for val in vals[1:]:
                new = LinkedCell(val)
                cell.next = new
                cell = new

            self.len = len(vals)

class BucketCell():
    def __init__(self, *args):
        """Faster list for appends and prepends,
        slower for insert, getting and setting,
        same for cycling"""
        
        self.val = args[0]
        if len(args)>1:
            self.next = BucketCell(*args[1:])
            self.last = self.next.last
        else:
            self.next = None
            self.last = self

    def __str__(self):
        return f'bcell({self.val}) --> {self.next}'

    def __repr__(self):
        return str(self)

    def reverse(self, old = None):
        if self.next:
            self.next.reverse(self)
        self.next = old

    def copy(self):
        new = BucketCell(self.val)
        if self.next:
            new.next = self.next.copy()
        return new

class BucketList():
    def __init__(self, *vals):
        if vals:
            self.head = BucketCell(*vals)
            self.last = self.head.last
        else:
            self.head = None
            self.last = None

    def __iter__(self):
        return LinkedIter(self.head)

    def __str__(self):
        s = 'BucketList['
        cell = self.head
        while cell:
            s += str(cell.val)
            if cell.next:
                s += ', '
            cell = cell.next
        return s+']'
    
    def __repr__(self):
        return str(self)
    
    def append(self, v):
        """Fast"""
        new = BucketCell(v)
        self.concat(new)
    
    def concat(self, new):
        """Fast"""
        if self.head:
            self.last.next = new
        else:
            self.head = new
        self.last = new.last

    def precat(self, new):
        newend = new
        while newend.next:
            newend = newend.next
        newend.next = self.head
            
        self.head = new
        
    def prepend(self, v):
        """Fast"""
        new = BucketCell(v)
        new.next = self.head
        self.head = new

    def delstart(self):
        """Fast"""
        self.head = self.head.next

    def delend(self):
        """Slow"""
        cell = self.head
        if cell:
            if cell.next:
                while cell.next and cell.next.next:
                    cell = cell.next
                cell.next = None
                self.last = cell
            else:
                self.head = None

    def __getitem__(self, i):
        """slow"""
        cell = self.head
        for _ in range(i):
            cell = cell.next
        return cell.val
    
    def __setitem__(self, i, val):
        """slow"""
        cell = self.head
        for _ in range(i):
            cell = cell.next
        cell.val = val

    def __len__(self):
        i = 0
        self = self.head
        while self:
            self = self.next
            i+=1
        return i
    
    def insert(self, i, val):
        if i==0:
            self.append(val)
        else:
            cell = self.head
            for _ in range(i-1):
                cell = cell.next

            if cell.next:
                new = BucketCell(val)
                new.next = cell.next
                cell.next = new
            else:
                self.append(val)
        return self

    def pop(self, i=None):
        if i==None:
            self.delend()
        else:
            if i==0:
                self.head = self.head.next
            else:
                cell = self.head
                for _ in range(i-1):
                    cell = cell.next
                if cell.next:
                    cell.next = cell.next.next
                else:
                    cell.next = None
                return cell

    def index(self, val):
        cell = self.head
        i = 0
        while cell:
            if cell.val == val:
                return i
            cell = cell.next
            i += 1
    
    def remove(self, val):
        cell = self.head
        old = False
        while cell:
            if cell.val == val:
                if old:
                    old.next = cell.next
                else:
                    self.head = cell.next
            old = cell
            cell = cell.next

    def reverse(self):
        self.head.reverse()
        self.head, self.last = self.last, self.head

    def copy(self):
        new = BucketList()
        new.head = self.head.copy()
        return new

    def list(self):
        li = []
        cell = self.head
        while cell:
            li.append(cell.val)
            cell = cell.next
        return li

    def extend(self, it):
        cell = self.last
        for v in it:
            new = BucketCell(v)
            cell.next = new
            cell = new

    def clear(self):
        self.head = None

    def count(self, val):
        i = 0
        cell = self.head
        while cell:
            if cell.val == val:
                i+=1
            cell = cell.next
        return i

    def sort(self, **kwargs):
        li = self.list()
        li.sort(**kwargs)
        self.head = BucketList(*li).head
        return self

"""
a = LinkedList(3,4,5)
b = LinkedList(11,12,13)
print(a)
a.append(6)
print('appended 6:',a)
a.prepend(2)
print('prepended 2:',a)
a.delend()
print('delend',a)
a.delstart()
print('delstart',a)
a.insert(2,9)
print('insert',a)
print('elem[0]:',a[0])
a[1] = 8
print('elem[1] = 8:',a)
print('len:',len(a))

for v in a:
    print(v)

a.concat(b)
print(a)
a.append(6)
print(a)
a.reverse()
print(a)
"""

"""
a = BucketList()
print(a)
a.append(6)
print(a)
a.append(7)
print(a)
a.prepend(2)
print(a)
a.prepend(1)
print(a)

a.delstart()
print(a)
a.delend()
print(a)
a.append(7)
print(a)
print(a[1])
a[0] = 5
print(a)

for v in a:
    print(v)

a.insert(0,4)
print(a)
a.insert(3,6.5)
print(a)
a.insert(5,8)
print(a)
a.append(9)
print(a)

b = a.copy()
a.reverse()
print(a)
print(b)

print(a.list())
print(a)
a.pop(0)
print(a)
a.pop(2)
print(a)
a.pop()
print(a)
print(a.index(7))
a.remove(4)
print(a)
a.extend(range(9))
print(a)
print(a.count(8))
print(a.sort())
print(a.sort(key = lambda key: -key))
"""

v = 10000
vb = 100

def foo(v):
    a = BucketList()
    for i in range(v):
        a.prepend(i)
    return a

def bar(v):
    a = []
    for i in range(v):
        a.append(i)
    return a

t = time.time()
for i in range(vb):
    foo(v)
print(time.time()-t)
print(f'x{v*vb}')



