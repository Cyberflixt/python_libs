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
```py
a = Vector(1,2,3)
b = Vector(3,3,3)
c = Vector(2,1,0)
print(a == b-c)
```
```py
>>> True
```

But some aren't really black and white:

- **Ambigous operators:**

```bool(foo)``` will always return ```True```  
> if (Vector(0)): True

This allows simpler boolean operations:
```py
vec and "Correct" or "Incorrect"
```

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

## Methods:

### bounds(*vectors):  
Returns the minimum and maximum vectors of all given vectors:  
-> (min: Vector, max: Vector)
```py
a = Vector(1,2,3)
b = Vector(3,3,2)
c = Vector(2,1,0)
print(a.bounds(b,c)) # using self
print(Vector.bounds(a,b,c))
```
```py
>>> (Vector3(1, 1, 0), Vector3(3, 3, 3))
>>> (Vector3(1, 1, 0), Vector3(3, 3, 3))
```

### dot(*vectors):  
(<=> length of a vector)  
Dot vectors of one or multiple vectors:  
-> scalar: int
```py
a = Vector(1,2,3)
b = Vector(3,3,2)
print(a.dot(b))
```
```py
>>> 15
```

### cross(vecA, vecB):  
> ⚠️ Only for **Vector3**

Cross product of 2 Vectors:
-> crossed: Vector  

<img src="http://mechanicsmap.psu.edu/websites/A1_vector_math/A1-4_crossproduct/images/crossproduct.png" height="150"/>  
```py
a = Vector(1,2,3)
b = Vector(3,3,2)
print(a.cross(b))
```
```py
>>> Vector3(-5, 7, -3)
```

### angle(vecA, vecB):  
> ⚠️ Only for **Vector2**

Returns the angle between 2 vectors:  
-> radians: float  

<img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQoq798oPzBN9PSLUTh2UDNUC7DAutz24nVoL--BFgaem3hnzsFx2E9lzpR5khRtN2jWRw&usqp=CAU" height="150"/>

```py
a = Vector(1,0)
b = Vector(0,1)
print(a.angle(b))
```
```py
>>> 1.571 # radians
```

### orthogonal(vecA, vecB, approx=0):
> ⚠️ Only for **Vector2**

Returns True if both vectors are orthogonal:  
(<=> vecA.dot(vecB) <= approx)  
-> orthogonal: bool  

<img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQIyKMPuZxr6zesRykMGH8k2uSERk2gfiStXw&usqp=CAU" height="150"/>

```py
a = Vector(1,0)
b = Vector(0,1)
print(a.orthogonal(b))
```
```py
>>> True
```


### lerp(vecA, vecB, time):

Returns the linearly interpolated vector:  

<img src="https://global.discourse-cdn.com/standard17/uploads/threejs/original/3X/2/8/283f0a36481db3e75d00c9fce14a8b169021f37b.png" height="150"/>

```py
a = Vector(6,3)
b = Vector(10,1)
print(a.lerp(b, 0.5))
```
```py
>>> Vector2(8, 2)
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


