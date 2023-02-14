from .types import *

def divide(poly1: Polinomial, poly2: Polinomial):
    
    if len(poly2.terms) == 2:
        letter = poly2.terms[0]

        dpoly = Polinomial(terms=poly1.terms.copy())

        quotient = Polinomial([])

        for i in poly1:
            try:
                if isinstance(i, (Unknow, Literal)) and i.esponent >= letter.esponent:
                    term = dpoly.get_term_from_grade(i.esponent, ensure_success=True)
                    division = term/letter
                    mult = poly2 * division
                    quotient = quotient + division

                    dpoly: Polinomial = dpoly - mult

                    dpoly.semplify_and_format()

            except AttributeError as e:
                import traceback
                print(traceback.format_exc())
                return None
        
    return (quotient, dpoly)

def scompone(poly: Polinomial):

    if isinstance(poly, str): poly = Polinomial.from_string(poly)

    if not poly: return None
    
    if poly == Trinomial:
        pa = poly[0]
        pb = poly[1]
        pc = poly[2]

        # 2 grade trinomial
        if pa.esponent == 2 and \
            pb.symbol == pa.symbol and \
            pb.esponent == 1 and not isinstance(pc, (Unknow, Literal, LiteralFraction)):

            a = Number(pa.coefficient)
            b = Number(pb.coefficient)
            
            delta = b ** 2 - 4*a*pc
            if delta > 0:
                _rad = Radical(delta)
                solutions = [LiteralFraction((-b -_rad),(2*a)),
                            LiteralFraction((_rad -b),(2*a))]
                f = (Unknow('x')*solutions[0].denominator - solutions[0].numerator)
                s = (Unknow('x')*solutions[1].denominator - solutions[1].numerator)

                return (f, s)
            elif delta == 0:
                rv = Radical(pa)+ Radical(pc)
                return (rv,rv)
            else:
                raise NotImplementedError('Cannot get the square root of a negative number')
        
    elif poly == Quadrinomial: # cube of binomial
        other = poly.terms.copy()
        tgrade = []

        for i in poly:
            if not isinstance(i, UnknownMultiplication) and i.esponent == 3:
                other.remove(i)
                tgrade.append(i)
            
        # square of binomial
        if len(tgrade) == 2:
            if 3*(Radical(tgrade[0], 3)**2)*Radical(tgrade[1], 3) in other and \
               3*(Radical(tgrade[1], 3)**2)*Radical(tgrade[0], 3) in other:
                if isinstance(other[0], (Unknow, Literal, UnknownMultiplication)): fv = other[0].coefficient
                else: fv = int(other[0])
                if isinstance(other[1], (Unknow, Literal, UnknownMultiplication)): sv = other[1].coefficient
                else: sv = int(other[1])

                if (fv > 0) and (sv > 0):
                    rv = Radical(tgrade[0], 3) + Radical(tgrade[1], 3)
                elif (fv > 0) and (sv < 0):
                    rv = Radical(tgrade[0], 3) - Radical(tgrade[1], 3)
                elif (fv < 0) and (sv > 0):
                    rv = Radical(tgrade[1], 3) - Radical(tgrade[0], 3)
                elif (fv < 0) and (sv < 0):
                    rv = - Radical(tgrade[0], 3) - Radical(tgrade[1], 3)
                return (rv, rv)
            
    elif poly == Binomial:
        f = poly[0]
        s = poly[1]

        a = Radical(f)

        # subtraction of squares
        if not isinstance(a, Radical) and (s.coefficient if isinstance(s, (Unknow, Literal)) else s.number) < 0:
            b = Radical(abs(s))
            if not isinstance(b, Radical):
                return ((a +b), (a -b))
        
        # subtraction of cubes
        a = Radical(f, 3)
        if not isinstance(a, Radical):
            b = Radical(abs(s), 3)
            if not isinstance(b, Radical):
                if (s.coefficient if isinstance(s, (Unknow, Literal)) else s.number) < 0: # positive
                    return ((a - b),((a**2) + a*b +(b**2))) 
                else: # negative
                    return ((a + b),((a**2) - a*b +(b**2)))
            
    return (poly, 1)
