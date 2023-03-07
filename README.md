# Python-Symbolic-Calculation
Add to python many symbolic calculation types

## The Basics:
Create an unknown and make some changes:

Import a pre-defined unknown 
``` python
>>> from Core.simples import x
```
or create your own unknown
``` python
>>> from Core import Unknow
>>> unknown = Unknow('k')
```
Great!

Now let's do some additions and subtractions:
``` python
>>> addition = 3*x + 4*x - 5*x
>>> addition
2x
>>> subtraction = addition -3*x
>>> subtraction
-x
>>> with_number = 3*x -4 +7*x +6
>>> with_number
+10x +2
```
Now we are ready to solve a basic equation!
``` python
>>> from Core import Equation
>>> from Core.simples import x
>>>
>>> equation = Equation(2*x, 8) # means "2x = 8"
>>> equation.solve()
+4
```

### Polinomials:
When monomials are too easy, here we have Polinomials!

Polinomials are very useful in symbolic math computation!
``` python
>>> from Core import Polinomial
```
Now let's see some basic math with them:
``` python
>>> poli = Polinomial.from_string('3x + 7y -4')
>>> poli * 2
+14y +6x -8
>>> from Core.simples import x, y
>>> eq = poli - 7*y
>>> eq
+3x -4
>>> from Core import Equation
>>> Equation(eq, 0).solve()
4/3
```

### Radicals:
When we have to manage numbers under root, we need the Radical object:
``` python
>>> from Core import Radical
>>> radical = Radical(3)
>>> radical
²√3
>>> radical.to_number()
1.7320508075688772
>>> radical = Radical(6) * Radical(2)
>>> radical
2²√3
```


### Factorizzation of numbers:
The Integer class allows us to see numbers as multiplication of prime numbers:
``` python
>>> from Core import Integer
>>> Integer.factorize(12)
[2, 2, 3]
>>> Integer(65).factorize()
[5, 13]
```

### Factorizzation of polinomials:
As all us know, polinomials can be also be factorized:
``` python
>>> first_factor, second_factor = (x**2 + 4*x + 4).scompone()
>>> first_factor
+x +2
>>> second_factor 
+x +2
>>> first_factor * second_factor
+x² +4x +4
```
We can also scompone more complex polinomials such as "x² -3x -3":
``` python
>>> first_factor, second_factor = (x**2 - 3*x -3).scompone()
>>> first_factor
+2x -3 -1²√21
>>> second_factor
+2x -3 +²√21
>>> first_factor * second_factor
+4x² -12x -12
```
As we can see this polinomial isn't reduced, we can search if there is a common divisor between it's terms:
``` python
>>> mult = first_factor * second_factor
>>> mult.mcd()
4
>>> mult / mult.mcd()
+x² -3x -3
```

### Find common factors:
There is a function called 'factors' that finds common factors between items:
``` python
>>> from Core import factors
>>> from Core.simples import x, y
>>>
>>> factors(33, 27)
[1, 3]
>>> factors(15*x, 3*x)
[<Unknow: x>, <Unknow: 3x>, 1, 3]
 
>>> for i in factors(12*x*y**2, 3*x*y):
...   print(i, end=', ')
1, 3, x, 1xy, y, 3x, 3xy, 3y,
```

### Second Degree Equations
This library can also compute second degree equaitons
``` python
>>> from Core.simples import x
>>> from Core import Equation
>>> 
>>> x1, x2 = Equation(x**2 + 4*x +4, 0).solve()
>>> x1
2
>>> x2
2
```
