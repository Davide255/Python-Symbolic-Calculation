from typing import List, Union, Tuple
from fractions import Fraction

SQRT_SYMBOL = '√'

class Binomial: pass
class Trinomial: pass
class Quadrinomial: pass

class Polinomial(object): ...
class Literal(object): ... 
class Unknow(object): ...
class Number(object): ...
class LiteralFraction(object): ...

def apex(number: Union[int, Number]):
    _apexs = {
        0:u'\u2070',
        1:u'\xb9',
        2:u'\xb2',
        3:u'\xb3',
        4:u'\u2074',
        5:u'\u2075',
        6:u'\u2076',
        7:u'\u2077',
        8:u'\u2078',
        9:u'\u2079'
    }
    string = ''
    for n in str(number): string += _apexs[int(n)]
    return string

class Number(object):
    
    def __init__(self, number: int, esponent: int = 1) -> None:
        self.number = number
        self.esponent = esponent

    def __int__(self) -> int:
        return self.number
    
    def __str__(self) -> str:
        if self.esponent == 1:
            return self.number.__str__()
        else: return '{}^{}'.format(self.number, self.esponent)
    
    @classmethod
    def factorize(self, number = None):
        if not number: n = self.number
        else: n = number
        factors = []
        while n > 1:
            for i in range(2, n+1):
                if n % i == 0:
                    n //= i
                    factors.append(i)
                    break
        factors.sort()
        return factors
    
    def __eq__(self, __x: object) -> bool:
        return self.number.__eq__(__x)
    
    def __neg__(self):
        self.number = -self.number
        return self
    
    def __abs__(self):
        return abs(self.number ** self.esponent)
    
    def __radd__(self, value):
        return value.__add__(self.number)
    
    def __rsub__(self, value):
        return value.__sub__(self.number)
    
    def __rmul__(self, value):
        return value.__mul__(self.number)
    
    def __rdiv__(self, value):
        return value.__div__(self.number)
    
    def __rtruediv__(self, value):
        return value.__truediv__(self.number)

    def __add__(self, value):
        if isinstance(value, (Unknow, Literal)):
            return value.__add__(self.number)
        elif isinstance(value, Radical):
            return Polinomial(terms=[value, self])
        elif isinstance(value, Number):
            return Number((self.number**self.esponent) + (value.number**value.esponent))
        else: 
            self = Number(self.number)
            return self.number.__add__(value)

    def __sub__(self, value):
        if isinstance(value, (Unknow, Literal)):
            return value.__sub__(self.number)
        elif isinstance(value, Radical):
            return Polinomial(terms=[-value, self])
        elif isinstance(value, Number):
            return Number((self.number**self.esponent) - (value.number**value.esponent))
        else: 
            self = Number(self.number)
            return self.number.__sub__(value)

    def __mul__(self, value):
        if isinstance(value, (Unknow, Literal)):
            return value * self.number
        elif isinstance(value, Radical):
            return value * self
        elif isinstance(value, Number):
            return Number((self.number**self.esponent) * (value.number**value.esponent))
        else:
            self = Number(self.number)
            return self.number.__mul__(value)

    def __truediv__(self, value):
        if isinstance(value, (Unknow, Literal)):
            return value / self.number
        elif isinstance(value, Radical):
            return value / self
        elif isinstance(value, Number):
            div = (self.number**self.esponent) /(value.number**value.esponent)
            if div.is_integer():
                return Number(div)
            else: return LiteralFraction((self.number**self.esponent), (value.number**value.esponent))
        else: 
            self = Number(self.number)
            return self.number.__truediv__(value)

    def __pow__(self, value):
        if isinstance(value, (Unknow, Literal)):
            return value ^ self.number
        elif isinstance(value, Radical):
            raise ValueError('Cannot elevate number by radical!')
        elif isinstance(value, Number):
            return Number(self.number**(self.esponent + (value.number**value.esponent)))
        elif isinstance(value, float):
            return self.number ** value
        else: 
            self = Number(self.number)
            return self.number.__pow__(value)

class Radical(object):
    
    coefficient = 1
    base = None
    index = 2

    def __new__(cls, 
        value: Union[Unknow, Literal, LiteralFraction, int, float, Number, Polinomial, 
                     List[Union[Unknow, Literal, LiteralFraction, int, float, Number, Polinomial]]], 
        index: int = 2,
        coefficient: int = 1) -> None:

        self = super(Radical, cls).__new__(cls)

        if not isinstance(value, list):
            if isinstance(value, str):
                self.base = Polinomial.from_string(value)
            else: self.base = value
            self.index = index
            self.coefficient = coefficient
        else:
            if len(value) == 0:
                return Number(0)
            elif len(value) == 1:
                self.base = value[0]
                self.index = index
                self.coefficient = coefficient
            elif len(value) == 2:
                self.base = value[0]
                self.index = value[1]
                self.coefficient = coefficient
            else:
                self.base = value[1]
                self.coefficient = value[0]
                self.index = value[2]
        
        if isinstance(self.base, (Number, int, float, Fraction)) and (self.base ** (1/self.index)).is_integer():
            return Number(int(self.base ** (1/self.index)))
        else: return self.semplify()

    def semplify(self):
        esp = 1
        num = -1
        nin = -1

        if isinstance(self.base, (Number, int, float, Fraction)):
            if (self.base ** 1/self.index).is_integer():
                return Number(self.base ** 1/self.index)
            else:
                factors = []
                processed = []
                nfactors = Number.factorize(self.base)
                for i in nfactors:
                    if not i in processed:
                        factors.append(Number(int(i), nfactors.count(i)))
                        processed.append(i)
                
                out = []
                rin = []
                for i in factors:
                    if i.esponent >= self.index:
                        esp = i.esponent
                        newesp = 0
                        while esp >= self.index:
                            esp = esp - self.index
                            newesp += 1
                        out.append(Number(i.number, newesp))
                        if esp != 0:
                            rin.append(Number(i.number, esp))
                    else: rin.append(i)

                if len(out) > 0:                
                    num = 1
                    for i in out:
                        num *= i.number

                if len(rin) > 0:
                    nin = 1
                    for i in rin:
                        nin *= i.number
                else: nin = self.base.coefficient

                if num != -1:
                    return Radical([num, nin, self.index])
                else: return self

        elif isinstance(self.base, (Unknow, Literal)):
            if (self.base.coefficient ** (1/self.index)).is_integer():
                num = int(self.base.coefficient ** (1/self.index))
            else:
                factors = []
                processed = []
                nfactors = Number.factorize(self.base.coefficient)
                for i in nfactors:
                    if not i in processed:
                        factors.append(Number(int(i), nfactors.count(i)))
                        processed.append(i)
                
                out = []
                rin = []
                for i in factors:
                    if i.esponent >= self.index:
                        esp = i.esponent
                        newesp = 0
                        while esp >= self.index:
                            esp = esp - self.index
                            newesp += 1
                        out.append(Number(i.number, newesp))
                        if esp != 0:
                            rin.append(Number(i.number, esp))
                    else: rin.append(i)
                
                num = 1
                for i in out:
                    num *= i.number

                if len(rin) > 0:
                    nin = 1
                    for i in rin:
                        nin *= i.number
                else: nin = self.base.coefficient
                

            if self.base.esponent % self.index == 0:
                if (num != -1 and abs(nin) == 1) or self.base.coefficient == 1:
                    return Unknow([abs(num), self.base.symbol, int(self.base.esponent / self.index)])
                else: 
                    return Radical([Unknow([abs(num), self.base.symbol, int(self.base.esponent / self.index)]), nin, self.index])
            elif self.base.esponent > self.index:
                esp = self.base.esponent
                newesp = 0
                while esp >= self.index:
                    esp -= self.index
                    newesp += 1
                return Radical([Unknow([abs(num), self.base.symbol, newesp]), Unknow([nin, self.base.symbol, esp]), self.index])
            else: 
                return Radical([Number(abs(num)), Unknow([nin, self.base.symbol, self.base.esponent]), self.index])
            
        elif isinstance(self.base, Radical):
            rad = Radical([self.base.coefficient, self.base.base, self.index * self.base.index])
            return rad.semplify()

    def __str__(self) -> str:
        return '{}{}{}{}'.format(self.coefficient if self.coefficient != 1 else '', apex(self.index), SQRT_SYMBOL, self.base)

    def __neg__(self):
        self.coefficient = -self.coefficient
        return self
    
    def __eq__(self, value):
        if isinstance(value, Radical):
            return True \
                if self.coefficient == value.coefficient and \
                self.base == value.base and \
                self.index == value.index else False
        else: return False

    def __add__(self, value):
        if isinstance(value, Radical) and self.base == value.base and self.index == value.index:
            return Radical([self.coefficient + value.coefficient, self.base, self.index])
        return Polinomial(terms=[self, value])
    
    def __sub__(self, value):
        if isinstance(value, Radical) and self.base == value.base and self.index == value.index:
            return Radical([self.coefficient - value.coefficient, self.base, self.index])
        return Polinomial(terms=[self, -value])
    
    def __mul__(self, value):
        if isinstance(value, (Number, int, float, Fraction, LiteralFraction)):
            return Radical([self.coefficient * value, self.base, self.index])
        elif isinstance(value, (Unknow, Literal)):
            return Unknow([Radical(self.coefficient * value.coefficient, self.base, self.index), value.symbol, value.esponent])
        elif isinstance(value, Radical):
            if self.base == value.base and self.index == value.index:
                return self.base * self.coefficient * value.coefficient
            elif self.index == value.index:
                return Radical([self.coefficient * value.coefficient, self.base * value.base, self.index])
            elif self.base == value.base:
                return Radical([self.coefficient * value.coefficient, self.base, self.index + value.index])
            else: return UnknownMultiplication(self, value)
        elif isinstance(value, Polinomial):
            return value * self

    def __truediv__(self, value):
        if isinstance(value, (Number, int, float, Fraction, LiteralFraction)):
            return Radical([self.coefficient / value, self.base, self.index])
        elif isinstance(value, (Unknow, Literal)):
            return Unknow([Radical(self.coefficient / value.coefficient, self.base, self.index), value.symbol, value.esponent])
        elif isinstance(value, Radical):
            if self.base == value.base and self.index == value.index:
                return self.coefficient / value.coefficient
            elif self.index == value.index:
                return Radical([self.coefficient / value.coefficient, self.base / value.base, self.index])
            elif self.base == value.base:
                return Radical([self.coefficient / value.coefficient, self.base, self.index - value.index])
            else: return LiteralFraction(self, value)
        elif isinstance(value, Polinomial):
            return value / self

class Unknow(object):

    symbol = None
    coefficient = None
    esponent = 1

    def __new__(cls, _Unknow: Union[str, List[Union[int, str, int]]] = None, return_if_0 = False):

        self = super(Unknow, cls).__new__(cls)

        if isinstance(_Unknow, str):
            if isinstance(_Unknow, str) and _Unknow.replace('-', '').replace('+','').isdigit():
                return Number(int(_Unknow))

            if _Unknow.replace('-', '').replace('+','').replace('^','').isalpha():
                self.symbol = _Unknow.replace('-', '').replace('+','').replace('^',' ')[0]
                self.coefficient = 1 if not '-' in _Unknow else -1
                self.esponent = 1 if not len(_Unknow.replace('-', '').replace('+','').replace('^',' ')) == 2 else _Unknow.replace('-', '').replace('+','').replace('^',' ')[1]
            else:
                num = ''
                self.symbol = ''
                for i in _Unknow:
                    if i.isdigit() or i == '-': num += i
                    elif i == '+': pass
                    elif i == '^':
                        self.esponent = int(_Unknow[_Unknow.find('^')+1:])
                        break
                    else: self.symbol += i
                import re
                self.coefficient = int(num) if re.search(r'[0-9]+', num) else int(num+'1')

        elif isinstance(_Unknow, list) and isinstance(_Unknow[1], str):
            self.coefficient = _Unknow[0]
            self.symbol = _Unknow[1]
            self.esponent = _Unknow[2] if len(_Unknow) > 2 else 1

        if (self.coefficient == 0 or self.esponent == 0) and not return_if_0:
            return Number(0)
    
        return self
    
    def __neg__(self):
        self.coefficient = -self.coefficient
        return self
    
    def __eq__(self, value) -> bool:
        if isinstance(value, Unknow):
            if self.coefficient == value.coefficient and self.symbol == value.symbol and self.esponent == value.esponent:return True
            else: return False
        return False

    def __add__(self, value):
        return Polinomial.from_sum(self, value)
    
    def __radd__(self, value):
        return Polinomial.from_sum(self, value)

    def __sub__(self, value):
        return Polinomial.from_sub(self, value)

    def __rsub__(self, value):
        return Polinomial.from_sub(value, self)

    def __mul__(self, value):

        if isinstance(value, str): value = Polinomial.from_string(value)

        if isinstance(value, (Unknow, Literal)):
            return Polinomial.from_mul(self, value)
        else:
            try:
                return Unknow([self.coefficient * int(value), self.symbol, self.esponent])
            except Exception as e:
                import traceback
                print(traceback.format_exc())
                return self

    def __rmul__(self, value):
        return self.__mul__(value)

    def __truediv__(self, value):
        if isinstance(value, str): value = Polinomial.from_string(value)

        if isinstance(value, (Unknow, Literal)):
            return Polinomial.from_mul(self, value)
        else:
            try: 
                self = Unknow([self.coefficient, self.symbol, self.esponent])
                self.coefficient = self.coefficient / int(value)
                if self.coefficient.is_integer(): self.coefficient = int(self.coefficient)
                else: self.coefficient = Fraction.from_float(self.coefficient)
                return self
            except Exception as e:
                import traceback
                print(traceback.format_exc())
                return self         

    def __rtruediv__(self, value):
        return LiteralFraction(value, self)

    def __pow__(self, value):
        if isinstance(value, str): value = Polinomial.from_string(value)

        if isinstance(value, (Unknow, Literal)):
            # Power with letter not implemented
            return self
            #return Unknow(self.coefficient ** value.coefficient,)

        if isinstance(value, int):
            self = Unknow([self.coefficient, self.symbol, self.esponent])
            self.esponent += value
            return self

    def __str__(self) -> str:
        return '{}{}{}'.format(str(self.coefficient) if abs(self.coefficient) != 1 else ('-' if self.coefficient < 0 else ''), self.symbol, apex(self.esponent) if self.esponent != 1 else '')

class Literal(Unknow):

    def __init__(self, letter: str) -> None:
        if letter.isalnum():
            num = ''
            self.symbol = ''
            for i in letter:
                if i.isdigit(): num += i
                else: self.symbol += i
            self.coefficient = int(num)

        elif letter.isalpha():
            self.symbol = letter
            self.coefficient = 1

class UnknownMultiplication(object):

    literals = None
    coefficient = None

    def __init__(self, *literals) -> None:
        self.literals = literals

        for i in literals:
            if self.coefficient: self.coefficient = self.coefficient * i.coefficient
            else: self.coefficient = i.coefficient

    def literal_part(self) -> str:
        fstr = ''
        for i in self.literals:
            fstr += i.symbol
        return fstr
    
    def __eq__(self, value):
        if isinstance(value, UnknownMultiplication):
            if self.coefficient == value.coefficient:
                for n, i in enumerate(self.literals):
                    if i.symbol != value.literals[n].symbol and\
                       i.esponent != value.literals[n].esponent: return False
                return True
        return False

    def __str__(self) -> str:
        fstr = ''
        for i in self:
            fstr += i.symbol + (apex(i.esponent) if i.esponent !=1 else '')
        return str(self.coefficient) + fstr
    
    def to_list(self) -> List[Union[int, Unknow]]:
        return self.literals
    
    def __add__(self, value):
        return Polinomial(terms=[self, value])
    
    def __radd__(self, value):
        return Polinomial(terms=[self, value])

    def __sub__(self, value):
        return Polinomial(terms=[self, value])
    
    def __rsub__(self, value):
        return Polinomial(terms=[self, -value])

    def __mul__(self, value):
        
        if isinstance(value, str): value = Polinomial.from_string(value)

        if isinstance(value, (Unknow, Literal, Number, int, float, Fraction, LiteralFraction)):
            new = [i * value for i in self]
            return Polinomial(terms=new)

        if isinstance(value, UnknownMultiplication):
            new = [i * l for l in value.literals for i in self]
            return Polinomial(terms=new)
    
    def __truediv__(self, value):
        
        if isinstance(value, str): value = Polinomial.from_string(value)

        if isinstance(value, (Unknow, Literal, Number, int, float, Fraction, LiteralFraction)):

            for i in self:
                if value / i:
                    pass

            return LiteralFraction(self, value)

        if isinstance(value, UnknownMultiplication):
            return LiteralFraction(self, value)
    
    def __pow__(self, value):

        if isinstance(value, str): value = Polinomial.from_string(value)

        if isinstance(value, (Number, int, float, Fraction)):
            new = [i**value for i in self]
            return Polinomial(terms=new)

    def __iter__(self):
        return iter(self.literals)

class Polinomial(object):

    terms: List[Union[Polinomial, Tuple[Union[int, str]]]] = None
    
    def __init__(self, terms: list = None) -> None:
        self.terms = terms if terms else []

        self.semplify_and_format()

    def __str__(self) -> str:
        self.semplify_and_format()
        fstr = ''
        for i in self.terms:
            if isinstance(i, (list,tuple)):
                e = str(i[0]) + i[1].symbol + i[2].symbol
                e = '+'+e if not e.startswith('-') else e
                fstr += e
            else: fstr += '+'+str(i) if not str(i).startswith('-') else str(i)

            fstr += ' '
        return fstr.replace('++', '+').replace('  ', ' ')
    
    def __getitem__(self, key):
        return self.terms.__getitem__(key)
    def __contains__(self, obj):
        return self.terms.__contains__(obj)
    
    @classmethod
    def scompone(self, poly: Polinomial):

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

    def get_term_from_grade(self, grade, letter=None, ensure_success=False):
        for i in self:
            if isinstance(i, (Unknow, Literal)) and i.esponent == grade: 
                if not letter: return i
                elif i.symbol == letter: return i
        if not ensure_success: return None
        else: return Unknow([0, letter if letter else 'x', grade])

    def from_sum(ob1, ob2) -> Union[Number, Unknow, Polinomial]:
        # n+n, x+n, x+x

        if isinstance(ob1, str): ob1 = Polinomial.from_string(ob1)
        if isinstance(ob2, str): ob2  = Polinomial.from_string(ob2)

        if isinstance(ob1, Polinomial):
            return ob1 + ob2
        elif isinstance(ob2, Polinomial):
            return ob2 + ob1

        if isinstance(ob1, (Number, int, float, LiteralFraction, Fraction)):
            if isinstance(ob2, (Number, int, float, LiteralFraction, Fraction)):
                return Number(ob1 + ob2)
            if isinstance(ob2, (Unknow, Literal)):
                return Polinomial(terms=[ob1, ob2])
            
        if isinstance(ob1, (Unknow, Literal)):
            if isinstance(ob2, (Number, int, float, Fraction)):
                return Polinomial(terms=[ob1, ob2])
            if isinstance(ob2, (Unknow, Literal)):
                if ob1.symbol == ob2.symbol or ob1.symbol == ob2.symbol[::-1]:
                    return Unknow([ob1.coefficient + ob2.coefficient, ob1.symbol])
                else:
                    return Polinomial(terms=[ob1, ob2])

    def from_sub(ob1, ob2):
        # n-n, x-n, x-x

        if isinstance(ob1, str): ob1 = Polinomial.from_string(ob1)
        if isinstance(ob2, str): ob2  = Polinomial.from_string(ob2)

        if isinstance(ob1, (Number, int, float, Fraction, LiteralFraction)):
            if isinstance(ob2, (Number, int, float, Fraction, LiteralFraction)):
                return Number(ob1 - ob2)
            if isinstance(ob2, (Unknow, Literal)):
                return Polinomial(terms=[ob1, -ob2])
            
        if isinstance(ob1, (Unknow, Literal)):
            if isinstance(ob2, (Number, int, float, Fraction, LiteralFraction)):
                return Polinomial(terms=[ob1, -ob2])
            if isinstance(ob2, (Unknow, Literal)):
                if ob1.symbol == ob2.symbol or ob1.symbol == ob2.symbol[::-1]:
                    return Unknow([ob1.coefficient - ob2.coefficient, ob1.symbol, ob1.esponent])
                else:
                    return Polinomial(terms=[ob1, -ob2])

    def from_mul(ob1, ob2):
        # n*n, x*n, x*x

        if isinstance(ob1, str): ob1 = Polinomial.from_string(ob1)
        if isinstance(ob2, str): ob2  = Polinomial.from_string(ob2)

        if isinstance(ob1, (Number, int, float, Fraction, LiteralFraction)):
            if isinstance(ob2, (Number, int, float, Fraction, LiteralFraction)):
                return Number(ob1 * ob2)
            if isinstance(ob2, (Unknow, Literal)):
                return Unknow(ob2 * ob1)
            
        elif isinstance(ob1, (Unknow, Literal)):
            if isinstance(ob2, (Number, int, float, Fraction, LiteralFraction)):
                return Unknow([ob1.coefficient * int(ob2), ob1.symbol])
            if isinstance(ob2, (Unknow, Literal)):
                if ob1.symbol == ob2.symbol:
                    return Unknow([ob1.coefficient * ob2.coefficient, ob1.symbol, ob1.esponent + ob2.esponent])
                else:
                    return Polinomial(terms=[UnknownMultiplication(ob1, ob2)])
                
        elif isinstance(ob1, Polinomial):
            return ob1 * ob2

    def from_div(ob1, ob2):
        # n/n, x/n, x/x

        if isinstance(ob1, str): ob1 = Polinomial.from_string(ob1)
        if isinstance(ob2, str): ob2  = Polinomial.from_string(ob2)

        if isinstance(ob1, (Number, int, float, Fraction, LiteralFraction)):
            if isinstance(ob2, (Number, int, float, Fraction, LiteralFraction)):
                return Number(ob1 / ob2)
            if isinstance(ob2, (Unknow, Literal)):
                return Unknow(ob1 / ob2)
            
        if isinstance(ob1, (Unknow, Literal)):
            if isinstance(ob2, (Number, int, float, Fraction, LiteralFraction)):
                return ob1 / ob2
            if isinstance(ob2, (Unknow, Literal)):
                if ob1.symbol == ob2.symbol:
                    return Unknow([Fraction(ob1.coefficient, ob2.coefficient), ob1.symbol, ob1.esponent - ob2.esponent])
                else:
                    return LiteralFraction(ob1.symbol, ob2.symbol) * Fraction(ob1.coefficient, ob2.coefficient)

    def from_string(string: str):
        terms = []
        string = string.replace('+', ' +').replace('-',' -').replace('  ', ' ')

        if '(' in string:
            string = string.replace(string[string.find('('):string.__len__()-string[::-1].find(')')+1], '')

        for i in string.split(' '):
            if i.replace('-','').replace('+','').replace('^', '').replace(' ', '').isalnum():
                terms.append(Unknow(i))
            elif i.replace('-','').replace('+','').isdigit():
                terms.append(Number(i))

        if len(terms) == 0: return None
        else: return Polinomial(terms=terms) if len(terms) > 1 else terms[0]
    
    def semplify_and_format(self):

        numbers = []
        literals = []
        fractions = []
        
        mons = [self]

        while len(mons) != 0:
            for i in mons.pop().terms:
                if isinstance(i, (Number, int, float, Fraction)):
                    numbers.append(int(i))
                elif isinstance(i, (Unknow, Literal, UnknownMultiplication)):
                    literals.append(i)
                elif isinstance(i, Polinomial):
                    mons.append(i)
                elif isinstance(i, LiteralFraction):
                    fractions.append(i)

        self.terms.clear()
        
        umap = {}
        
        for i in literals:
            if not isinstance(i, UnknownMultiplication): 
                if i.esponent == 0: 
                    numbers.append(Number(i.coefficient))
                    break
                key = i.symbol+'^'+str(i.esponent)   
            else:
                key = ''
                for l in i:
                    if l.esponent == 0: 
                        numbers.append(Number(l.coefficient)) 
                        break
                    key += l.symbol + '^' + str(l.esponent)

            if not isinstance(umap.get(key), list):
                umap[key] = [i]
            else: umap[key].append(i)

        number = sum(numbers)
        if number != 0: self.terms.append(Number(number))

        keys = list(umap.keys())
        keys.sort()

        for i in keys:
            if len(umap[i]) > 1:
                def summ(ls):
                    out = ls.pop(0)
                    for i in ls:
                        out = out + i
                    return out
                
                _i = summ(umap[i])
            else: _i = umap[i][0]
            self.terms.append(_i)
        
        self.terms += fractions

        self.terms.reverse()

        if len(self.terms) == 1 and isinstance(self.terms[0], (int, float, Number)):
            return Number(self.terms[0])
        
        if len(self.terms) == 0:
            self.terms.append(Number(0))
        
        return self

    def find_similar(self, unk):
        if isinstance(unk, (Unknow, Literal)):
            for i in self.terms:
                if isinstance(i, (Unknow, Literal)) and i.symbol == unk.symbol and i.esponent == unk.esponent:
                        return (i, i)
                if isinstance(i, Polinomial) and len(i.terms) == 1:
                    if i.terms[0].literal_part() == unk.symbol or i.terms[0].literal_part() == unk.symbol[::-1]:
                        return (i, i.terms[0].to_unknow())
        return None
    
    def __neg__(self):
        for i in range(len(self.terms)): self.terms[i] = -self.terms[i]
        return self
    
    def __eq__(self, value):
        if isinstance(value, Binomial) or value == Binomial:
            return True if len(self.terms) == 2 else False
        elif isinstance(value, Trinomial) or value == Trinomial:
            return True if len(self.terms) == 3 else False
        elif isinstance(value, Quadrinomial) or value == Quadrinomial:
            return True if len(self.terms) == 4 else False
        
        if isinstance(value, Polinomial):
            if self.terms == value.terms: return True
            else: return False
        elif len(self.terms) == 1:
            if self.terms[0] == value: return True
            else: return False 
        return False

    def __add__(self, value):

        self = Polinomial(terms=self.terms.copy())

        if isinstance(value, str): value = Polinomial.from_string(value)

        if isinstance(value, (Number, Fraction, LiteralFraction, int, float)):
            for i in self.terms:
                if isinstance(i, (Number)):
                    self.terms.remove(i)
                    self.terms.append(i + value)
                    return self
        elif isinstance(value, (Unknow, Literal)):
            similar = self.find_similar(value)
            if similar:
                self.terms.remove(similar[0])
                self.terms.append(similar[1] + value)
            else: self.terms.append(value)
        
        elif isinstance(value, Polinomial):
            for i in value.terms:
                similar = self.find_similar(i)
                if similar:
                    self.terms[self.terms.index(similar[0])] = similar[1] + value
                else: self.terms.append(i)

        elif isinstance(value, Radical):
            self.terms.append(value)

        return self
    
    def __radd__(self, value):
        return Polinomial(terms=[*self.terms, value])

    def __sub__(self, value):

        self = Polinomial(terms=self.terms.copy())

        if isinstance(value, str): value = Polinomial.from_string(value)

        if isinstance(value, (Number, Fraction, LiteralFraction, int, float)):
            for i in self.terms:
                if isinstance(i, (Number)):
                    self.terms.remove(i)
                    self.terms.append(i - value)
                    return self

        elif isinstance(value, (Unknow, Literal)):
            similar = self.find_similar(value)
            if similar:
                self.terms[self.terms.index(similar[0])] = similar[1] - value
            else: self.terms.append(-value)
        
        elif isinstance(value, Polinomial):
            for i in value.terms:
                similar = self.find_similar(i)
                if similar:
                    sub = similar[1] - i
                    self.terms[self.terms.index(similar[0])] = sub
                else: self.terms.append(-i)

        elif isinstance(value, Radical):
            self.terms.append(value)

        return self
    
    def __rsub__(self, value):
        return Polinomial(terms=[*self.terms, -value])
    
    def __mul__(self, value):

        self = Polinomial(terms=self.terms.copy())

        if isinstance(value, str): value = Polinomial.from_string(value)
        
        if isinstance(value, (Number, int, float, Fraction, LiteralFraction, Unknow, Literal, Radical)):
            for i in self.terms:
                self.terms[self.terms.index(i)] = i * value
            return self
            
        if isinstance(value, Polinomial):
            outterms = []
            for i in self.terms:
                for t in value.terms.copy():
                    outterms.append(i*t)
            return Polinomial(terms=outterms)
    
    def __truediv__(self, value):
        self = Polinomial(terms=self.terms.copy())

        if isinstance(value, str): value = Polinomial.from_string(value)
        
        if isinstance(value, (Number, int, float, Fraction, LiteralFraction, Unknow, Literal)):
            for i in self.terms:
                self.terms[self.terms.index(i)] = i / value
            return self

        if isinstance(value, Polinomial):
            qu, rest = divmod(self, value)
            if rest == 0:
                return qu
            else: return LiteralFraction(self, value)      

    def __divmod__(self, value):
        letter = value.terms[0]
        rest = Polinomial(terms=self.terms.copy())
        quotient = Polinomial([])
        for i in self:
            try:
                if isinstance(i, (Unknow, Literal)) and i.esponent >= letter.esponent:
                    term = rest.get_term_from_grade(i.esponent, ensure_success=True)
                    division = term/letter
                    mult = value * division
                    quotient = quotient + division

                    print('(', rest, ') - (', mult, ')', '=', end=' ')

                    rest: Polinomial = rest - mult

                    print(rest)

                    rest.semplify_and_format()

            except AttributeError as e:
                import traceback
                print(traceback.format_exc())
                return None
        
        return (quotient, rest)   
    
    def __pow__(self, value):
        return
    
    def __iter__(self):
        return iter(self.terms)

class LiteralFraction(object):

    numerator: Union[Polinomial, Unknow, Number] = None
    denominator: Union[Polinomial, Unknow, Number] = None
    literal: bool = False

    def __new__(cls, *args):
        self = super(LiteralFraction, cls).__new__(cls)

        if len(args) == 1 and isinstance(args[0], str): 
            fstr = args[0]
            fstr = fstr.split('/')

            for n, i in enumerate(fstr):
                if n == 0: self.numerator = Polinomial.from_string(i)
                elif n == 1: self.denominator = Polinomial.from_string(i)
            
            if isinstance(self.numerator, (Number, int, float)) and isinstance(self.denominator, Number): self.literal = False
            else: self.literal = True
        elif len(args) == 1 and isinstance(args[0], int): return Number(args[0])
        elif len(args) == 1 and isinstance(args[0], float): return Fraction(args[0])
        elif len(args) == 2:
            if isinstance(args[0], (Number, int)) and isinstance(args[1], (Number, int)): return Fraction(*args)
            else:
                self.numerator = Polinomial.from_string(args[0]) if isinstance(args[0], str) else args[0]
                self.denominator = Polinomial.from_string(args[1]) if isinstance(args[1], str) else args[1]

                if isinstance(self.numerator, Polinomial): self.numerator = self.numerator.semplify_and_format()
                if isinstance(self.denominator, Polinomial): self.denominator = self.denominator.semplify_and_format()

                if isinstance(self.numerator, (Unknow, Literal, Polinomial)) or isinstance(self.denominator, (Unknow, Literal, Polinomial)): self.literal = True
                else: return Fraction(self.numerator, self.denominator)

        return self
    
    def from_div(obj1: Union[Number, Unknow, Polinomial], obj2: Union[Number, Unknow, Polinomial]):
        pass

    def __neg__(self):
        self.numerator = -self.numerator
        return self

    def __str__(self) -> str:
        num = ''
        if isinstance(self.numerator, Polinomial): num = '(' + self.numerator.__str__() + ')'
        else: num = str(self.numerator)

        den = ''
        if isinstance(self.denominator, Polinomial): den = '(' + self.denominator.__str__() + ')'
        else: den = str(self.denominator)

        return '{}/{}'.format(num, den)

    def __eq__(self, value):
        if isinstance(value, LiteralFraction):
            if self.numerator == value.numerator and self.denominator == value.denominator: return True
            else: return False
        return False
    
    def __add__(self, value) -> Union[LiteralFraction, Fraction]:
        self = LiteralFraction(self.numerator, self.denominator)
        if isinstance(value, (LiteralFraction, Fraction)):
            fn = self.numerator * value.denominator
            sn = self.denominator * value.numerator
            commondenominator = self.denominator * value.denominator
            return LiteralFraction((fn + sn), commondenominator)
        else:
            self.numerator = self.numerator + (self.denominator * value)
        return self

    def __sub__(self, value) -> Union[LiteralFraction, Fraction]:
        self = LiteralFraction(self.numerator, self.denominator)
        if isinstance(value, (LiteralFraction, Fraction)):
            fn = self.numerator * value.denominator
            sn = self.denominator * value.numerator
            commondenominator = self.denominator * value.denominator
            return LiteralFraction((fn + sn), commondenominator)
        else:
            self.numerator = self.numerator + (self.denominator * value)
        return self
    
    def __mul__(self, value):
        if isinstance(value, (LiteralFraction, Fraction)):
            return LiteralFraction(self.numerator * value.numerator, self.denominator * value.denominator)
        else:
            return LiteralFraction(self.numerator * value, self.denominator)

    def __truediv__(self, value):
        self = LiteralFraction(self.numerator, self.denominator)
        if isinstance(value, (LiteralFraction, Fraction)):
            return LiteralFraction(self.numerator * value.denominator, self.denominator * value.numerator)
        else:
            self.numerator = self.numerator + (self.denominator * value)
        return self
    
    def __pow__(self, value):
        return LiteralFraction(self.numerator ** value, self.denominator ** value)

class Expression(object):
    '''
Basic Expression Class
======================

It's used for expressions with only sum, subtraction, division and multiplication
without any parentesis!

    '''

    def __init__(self, expr: str) -> None:
        self.expression = self.parse_expr(expr)

    def parse_expr(self, expr: str): #-> #List[Number, Unknow]:
        
        fexpr = expr.replace('+', ' +').replace('-',' -'). replace('=', ' = ').replace('  ', ' ').replace('+ ', '+').replace('- ','-')

        parts = fexpr.split(' = ')

        fp = Polinomial.from_string(parts[0])
        sp = Polinomial.from_string(parts[1])

        eq = fp-sp

        print(eq)