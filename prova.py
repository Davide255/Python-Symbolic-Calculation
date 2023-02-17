from Core import *
from Core.simples import x, y

s = System(
    Equation(3*(y -12), x -12), 
    Equation(2*(y +3), x +3)).solve()

print(s)
