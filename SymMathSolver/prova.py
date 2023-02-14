from Core import Polinomial, LiteralFraction, Unknow, Radical, Number

from Core.polynomialdivision import divide, scompone

expr = '''
(3x +4(
    (2x +4)(2x - 4) +
    7(3
    (22 + 
        (34-2)
    )
    )
    )
) = 
(13 +4x)'''

'''
expr = expr.replace('\n', '') \
    .replace(' ', '').replace('=', ' = ')\
    .replace('+', ' +').replace('-',' -')

dept = 0
refs = {}

class hierarchy(object):

    def __init__(self) -> None:
        pass

ccount = 0

for c in expr:
    if '(' == c:
        dept += 1
        if not isinstance(refs.get(dept), list):
            refs[dept] = [[ccount]]
        else: refs[dept].append([ccount])
    
    if ')' == c:
        refs[dept][-1].append(ccount)
        dept -= 1
    
    ccount += 1

sref = refs.copy()
obref = refs.copy()

for n in list(refs.keys())[::-1]:
    for i in refs[n]:
        if n > 1:
            for si in refs[n-1]:
                if si[0] < i[0] and i[1] < si[1]:
                    sref[n-1][sref[n-1].index(si)].append(i)
                    #print(Monomial.from_string(expr[i[0]+1:i[1]]))

                    obref[n-1][obref[n-1].index(si)].append(Monomial.from_string(expr[i[0]+1:i[1]]))
        else:
            pass #for i in refs[n]:
                #print(Monomial.from_string(expr[i[0]+1:i[1]]))

del refs

print(sref[1], '\n', obref[1])
print(expr)'''

'''division, rest = divmod(Polinomial.from_string('2x^5 -x^4 -x^3 +4x^2 -2x'), Polinomial.from_string('x^2 -x +1'))

print(division, rest)'''

scomp = scompone(Unknow('a^3') + (Unknow('3a^2') * 'b') + (Unknow('3b^2') * 'a') + Unknow('b^3'))

print(scomp[0], scomp[1])

'''print(Radical(Radical(3**7, 3)).semplify())'''