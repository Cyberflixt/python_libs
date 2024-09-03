
class Tree:
    def __init__(self, v = None, a = None, b = None):
        self.v = v
        self.a = a
        self.b = b

    def text(self, height):
        tabs = 3
        s = ''
        if height>0:
            for i in range((height-1)*tabs):
                s += ' '
            s += '|'
            for i in range(tabs-1):
                s += '-'
        s += str(self.v)
        
        if self.a:
            s += '\n' + self.a.text(height+1)
        if self.b:
            s += '\n' + self.b.text(height+1)
        
        return s

    def __str__(self):
        return self.text(0)

    def __repr__(self):
        return str(self)


a = Tree(
    'root',
    Tree(
        1,
        Tree(
            2
        ),
        Tree(
            3
        )
    ),
    Tree(
        4,
        Tree(
            5
        )
    )
)

print(a)
