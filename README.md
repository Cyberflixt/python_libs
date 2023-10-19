# PythonLibs

Somewhat useful python custom libraries

# Vector

- Create Vectors and use operations in any way you want.
- Convenient, no dimensions limits, easily manipulated.

Use it as an object, list, dictionary, tuple, whatever, ***anything works***.


## Vector basics
### Declaration
```py
from vectors import *
foo = Vector(5,7)
print(foo)
```
```py
>>> Vector2(5, 7)
```
Or choose your own way to create a Vector
```py
a = Vector([3,4,6])
b = Vector({'y':8, 'x':3})
c = Vector(1)
d = Vector()
```
```py
>>> Vector3(3, 4, 6)
>>> Vector2(3, 8)
>>> Vector1(1)
>>> Vector0()
```

## Basic operations
- Working operators:

```bool``` ```abs``` ```sum``` ```ceil``` ```floor``` ```round``` ```invert``` ```str``` ```==``` ```-x``` ```and``` ```or``` ```%``` ```*``` ```+``` ```-``` ```/``` ```//``` ```**``` ```[x]``` ```[x]=x``` ```len``` ```hash``` ```repr``` ```<``` ```>``` ```<=``` ```>=``` ```~```

Just think of them as normal numbers:
```py
a = Vector(1,2)
b = Vector(3,4)

print(a+b)
```
```py
>>> Vector2(4, 6)
```

Not the same dimension? **Doesn't matter**.  
- 0 will be the default value for missing values
```py
a = Vector(1,2,3)
b = Vector(5)

print(a-b)
```
```py
>>> Vector3(-4, 2, 3)
```
- empty values will be ignored for divisions (no divisions by 0)  
operators: ```/``` ```//``` ```%```
```py
a = Vector(6,2,1,0)
b = Vector(2)

print(a/b) # a//b also works btw
```
```py
>>> Vector4(3.0, 2, 1, 0)
```

## Coordinates
Coordinates are saved in Vector.coords
```py
foo = Vector(7,8,9)
print(foo.coords)
```
```py
>>> [7, 8, 9]
```
However, that was the polically correct way, which is boring. 
Again, do it however you want:

```py
foo = Vector(7,8,9)
for v in foo:
    print(v)
```
```py
7 8 9
```
Or unpacking the values
```py
def bar(x,y,z):
    print(x+y+z)

foo = Vector(7,8,9)
bar(*foo)
```
```py
24
```
## Individual coordinates
You get it at this point...
```py
foo = Vector(7,8,9)

foo.coords[0] = 1
foo[1] = 2
foo.z = 3

print(foo)

print(foo.coords[0], foo[1], foo.z)
```
```py
Vector3(1, 2, 3)
1 2 3
```

## Comparison
Operators such as ```==``` ```!=``` are self-explanatory,  
But some aren't really black and white:

- **Ambigous operators:**

```bool(foo)``` will always return ```True```  
> if (Vector(0)): True

```a>b``` will return ```sum(a)>sum(b)``` (sum of all coordinates)  
> Vector(-8,8) > Vector(1) = False

## Math aliases
Vectors are compatible with the math lib
```py
import math

foo = Vector(1.3, 2.8)
print(math.floor(foo))
print(math.ceil(foo))
```
```py
Vector2(1, 2)
Vector2(2, 3)
```
It is also possible to use these methods without the library
```py
print(foo.floor())
print(foo.ceil())
```

## Copying
Use either ```copy``` ```clone``` ```new```  
Or you can even use Vector(vec):
```py
foo = Vector(1,2)

a = foo.copy()
b = foo.clone()
c = foo.new()
d = Vector(foo)

foo.x = 0

print(a,b,c,d)
print(foo)
```
```py
Vector2(1, 2) Vector2(1, 2) Vector2(1, 2) Vector2(1, 2)
Vector2(0, 2)
```


## Pointer [WIP]
***[Only supported in 2D for now]***  
An object with a Vector position and a rotation number

```py
arrow = Pointer(Vector(0,0), 0, unit='deg') # radians by default
arrow.move(Vector(5,0))
arrow.rotate(45)
arrow.forward(5)
```


