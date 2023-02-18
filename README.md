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
>>> from Core.simples import y
>>> eq = poli - 7*y
>>> eq
+3x -4
>>> from Core import Equation
>>> Equation(eq, 0).solve()
4/3
```
### Factorizzation of a polinomial:
As all us know, polinomials can be also be factorized:
``` python
```
