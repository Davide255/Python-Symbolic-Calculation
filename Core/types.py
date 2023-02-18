from typing import List, Union, Tuple
from fractions import Fraction
from math import factorial

SQRT_SYMBOL = '√'

class Binomial: pass
class Trinomial: pass
class Quadrinomial: pass

class Polinomial(object): ...
class Literal(object): ... 
class Unknow(object): ...
class Integer(object): ...
class LiteralFraction(object): ...

def apex(number: Union[int, Integer]):
    _apexs = {
        '-':u'\u207b',
        '0':u'\u2070',
        '1':u'\xb9',
        '2':u'\xb2',
        '3':u'\xb3',
        '4':u'\u2074',
        '5':u'\u2075',
        '6':u'\u2076',
        '7':u'\u2077',
        '8':u'\u2078',
        '9':u'\u2079'
    }
    string = ''
    for n in str(number): string += _apexs[n]
    return string

class Integer(object):

    number: int = None
    esponent: int = 1
    
    def __new__(cls, number: int, esponent: int = 1):
        self = super(Integer, cls).__new__(cls)
        if isinstance(number, Integer): return number
        if not isinstance(number, int): return number ** esponent
        self.number = number
        self.esponent = esponent
        return self

    def __int__(self) -> int:
        return self.number ** self.esponent
    
    def __str__(self) -> str:
        if self.esponent == 1:
            return self.number.__str__()
        else: return '{}{}'.format(self.number, apex(self.esponent) if self.esponent != 1 else '')
    
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
    
    def __lt__(self, value):
        return int(self).__lt__(value)
    
    def __le__(self, value):
        return int(self).__le__(value)
    
    def __gt__(self, value):
        return int(self).__gt__(value)
    
    def __ge__(self, value):
        return int(self).__ge__(value)
    
    def __mod__(self, value):
        return self.number % value
    
    def __neg__(self):
        return Integer(-self.number, self.esponent)
    
    def __abs__(self):
        return abs(self.number ** self.esponent)
    
    def __radd__(self, value):
        return value.__add__(self.number ** self.esponent)
    
    def __rsub__(self, value):
        return value.__add__(-(self.number ** self.esponent))
    
    def __rmul__(self, value):
        return value.__mul__(self.number ** self.esponent)
    
    def __rtruediv__(self, value):
        return Fraction(value, self.number ** self.esponent)

    def __add__(self, value):
        if isinstance(value, (Unknow, Literal)):
            return value.__add__(self.number)
        elif isinstance(value, Radical):
            return Polinomial(terms=[value, self])
        elif isinstance(value, Integer):
            return Integer((self.number**self.esponent) + (value.number**value.esponent))
        else: 
            self = Integer(self.number)
            return self.number.__add__(value)

    def __sub__(self, value):
        if isinstance(value, (Unknow, Literal)):
            return value.__sub__(self.number)
        elif isinstance(value, Radical):
            return Polinomial(terms=[-value, self])
        elif isinstance(value, Integer):
            return Integer((self.number**self.esponent) - (value.number**value.esponent))
        else: 
            self = Integer(self.number)
            return self.number.__sub__(value)

    def __mul__(self, value):
        if isinstance(value, (Unknow, Literal)):
            return value * self.number
        elif isinstance(value, Radical):
            return value * self
        elif isinstance(value, Integer):
            if value.number == self.number: return Integer(self.number, self.esponent + value.esponent)
            elif self.esponent == value.esponent: return Integer(self.number * value.number, self.esponent)
            else: return Integer((self.number**self.esponent) * (value.number**value.esponent))
        else:
            self = Integer(self.number)
            return self.number.__mul__(value)

    def __truediv__(self, value):
        if isinstance(value, (Unknow, Literal)):
            return value / self.number
        elif isinstance(value, Radical):
            return value / self
        elif isinstance(value, Integer):
            if value.number == self.number: return Integer(self.number, self.esponent - value.esponent)
            elif self.esponent == value.esponent and (self.number / value.number).is_integer(): return Integer(self.number / value.number, self.esponent)
            else:
                div = (self.number**self.esponent) /(value.number**value.esponent)
                if div.is_integer():
                    return Integer(div)
                else: return LiteralFraction((self.number**self.esponent), (value.number**value.esponent))
        else: 
            self = Integer(self.number)
            return self.number.__truediv__(value)

    def __pow__(self, value):
        if isinstance(value, (Unknow, Literal)):
            # literal esponent not implemented
            raise ValueError('cannot elevate number by unknow or literal')
        elif isinstance(value, Radical):
            raise ValueError('Cannot elevate number by radical!')
        elif isinstance(value, Integer):
            return Integer(self.number**(self.esponent + (value.number**value.esponent)))
        elif isinstance(value, float):
            return self.number ** value
        else: 
            self = Integer(self.number)
            return self.number.__pow__(value)

class Radical(object):
    
    coefficient = 1
    base = None
    index = 2

    def __new__(cls, 
        value: Union[Unknow, Literal, LiteralFraction, int, float, Integer, Polinomial, 
                     List[Union[Unknow, Literal, LiteralFraction, int, float, Integer, Polinomial]]], 
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
                return Integer(0)
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
        
        if isinstance(self.base, (Integer, int, float, Fraction)) and (self.base ** (1/self.index)).is_integer():
            return Integer(int(self.base ** (1/self.index)))
        else: return self.semplify()

    def semplify(self):
        esp = 1
        num = -1
        nin = -1

        if isinstance(self.base, (Integer, int, float, Fraction)):
            if (self.base ** (1/self.index)).is_integer():
                return Integer(self.base ** (1/self.index))
            else:
                tfa = [self.base] if not isinstance(self.base, (Fraction)) \
                    else [self.base.numerator, self.base.denominator]
                
                for base in tfa:
                    factors = []
                    processed = []
                    nfactors = Integer.factorize(base)
                    for i in nfactors:
                        if not i in processed:
                            factors.append(Integer(int(i), nfactors.count(i)))
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
                            out.append(Integer(i.number, newesp))
                            if esp != 0:
                                rin.append(Integer(i.number, esp))
                        else: rin.append(i)

                    if len(out) > 0:                
                        num = 1 if num == -1 else num
                        for i in out:
                            num *= i.number

                    if len(rin) > 0:
                        nin = 1 if nin == -1 else nin
                        for i in rin:
                            nin *= i.number
                    else: nin = base.coefficient if not isinstance(base, (int, Integer)) else int(base)

                if num != -1:
                    return Radical([num, nin, self.index])
                else: return self

        elif isinstance(self.base, (Unknow, Literal)):
            if isinstance(self.base.coefficient, (int, Integer)):
                if (self.base.coefficient ** (1/self.index)).is_integer():
                    num = int(self.base.coefficient ** (1/self.index))
                else:
                    factors = []
                    processed = []
                    nfactors = Integer.factorize(self.base.coefficient)
                    for i in nfactors:
                        if not i in processed:
                            factors.append(Integer(int(i), nfactors.count(i)))
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
                            out.append(Integer(i.number, newesp))
                            if esp != 0:
                                rin.append(Integer(i.number, esp))
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
                    return Radical([Integer(abs(num)), Unknow([nin, self.base.symbol, self.base.esponent]), self.index])
            else: return self
        elif isinstance(self.base, Radical):
            return Radical([self.base.coefficient, self.base.base, self.index * self.base.index])
        
        elif isinstance(self.base, Polinomial):
            
            if self.base == Binomial and Radical in self.base:
                a = self.base[0]
                b = self.base[1]

                if isinstance(a, Radical):
                    r = a
                    a = b
                    b = r

                if not isinstance(b, Radical):
                    return self

                if True:
                    rrad = a**2 - (b.base * (b.coefficient ** 2))

                    if rrad > 0:
                        if b.coefficient < 0:
                            return Radical(LiteralFraction((a + Radical(rrad)),2)) - \
                            Radical(LiteralFraction((a - Radical(rrad)),2))
                        else: return Radical(LiteralFraction((a + Radical(rrad)),2)) + \
                            Radical(LiteralFraction((a - Radical(rrad)),2))
                    else: return self

        else: return self

    def __str__(self) -> str:
        if not isinstance(self.base, Polinomial):
            return '{}{}{}{}'.format(self.coefficient if self.coefficient != 1 else '', apex(self.index), SQRT_SYMBOL, self.base)
        else: 
            return '{}{}{}({})'.format(self.coefficient if self.coefficient != 1 else '', apex(self.index), SQRT_SYMBOL, self.base)

    def __abs__(self): return Radical(self.base, self.index, abs(self.coefficient))

    def __neg__(self):
        return Radical(self.base, self.index, -self.coefficient)
    
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
    
    def __radd__(self, value):
        return self + value

    def __sub__(self, value):
        if isinstance(value, Radical) and self.base == value.base and self.index == value.index:
            return Radical([self.coefficient - value.coefficient, self.base, self.index])
        return Polinomial(terms=[self, -value])
    
    def __rsub__(self, value):
        return -self + value

    def __mul__(self, value):
        if isinstance(value, (Integer, int, float, Fraction, LiteralFraction)):
            return Radical([self.coefficient * value, self.base, self.index])
        elif isinstance(value, (Unknow, Literal)):
            return value * self
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

    def __rmul__(self, value):
        return self * value

    def __truediv__(self, value):
        if isinstance(value, (Integer, int, float, Fraction, LiteralFraction)):
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

    def __rtruediv__(self, value):
        return LiteralFraction(value, self)

    def __pow__(self, value):
        if isinstance(value, (int, Integer)):
            return Radical([self.coefficient ** int(value), self.base ** int(value), self.index])

class Unknow(object):

    symbol = None
    coefficient = None
    esponent = 1

    def __new__(cls, _Unknow: Union[str, List[Union[int, str, int]]] = None, return_if_0 = False):

        self = super(Unknow, cls).__new__(cls)

        if isinstance(_Unknow, str):
            if isinstance(_Unknow, str) and _Unknow.replace('-', '').replace('+','').isdigit():
                return Integer(int(_Unknow))

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
            return Integer(0)
    
        return self
    
    def set_value(self, value: Union[int, float, Fraction]):
        setattr(self, self.symbol, value)
        return self

    def __neg__(self):
        return Unknow([-self.coefficient, self.symbol, self.esponent])
    
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

        if isinstance(value, (Unknow, Literal, Fraction, LiteralFraction, Radical)):
            return Polinomial.from_mul(self, value)
        else:
            try:
                return Unknow([self.coefficient * int(value), self.symbol, self.esponent])
            except Exception as e:
                pass

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
            return Unknow([Integer(self.coefficient, value), self.symbol, self.esponent * value])

    def __mod__(self, value):
        return self.coefficient % value

    def __str__(self) -> str:
        return '{}{}{}'.format(str(self.coefficient) if abs(self.coefficient) != 1 else ('-' if self.coefficient < 0 else ''), self.symbol, apex(self.esponent) if self.esponent != 1 else '')

class Literal(Unknow): pass

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
    
    def __neg__(self):
        return 0 - self

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

        if isinstance(value, (Unknow, Literal, Integer, int, float, Fraction, LiteralFraction)):
            new = [i * value for i in self]
            return Polinomial(terms=new)

        if isinstance(value, UnknownMultiplication):
            new = [i * l for l in value.literals for i in self]
            return Polinomial(terms=new)
    
    def __truediv__(self, value):
        
        if isinstance(value, str): value = Polinomial.from_string(value)

        if isinstance(value, (Unknow, Literal, Integer, int, float, Fraction, LiteralFraction)):

            for i in self:
                if value / i:
                    pass

            return LiteralFraction(self, value)

        if isinstance(value, UnknownMultiplication):
            return LiteralFraction(self, value)
    
    def __pow__(self, value):

        if isinstance(value, str): value = Polinomial.from_string(value)

        if isinstance(value, (Integer, int, float, Fraction)):
            return Polinomial(terms=[UnknownMultiplication(*[i ** value for i in self.literals])])

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
    
    def __abs__(self): return self

    def __getitem__(self, key): return self.terms.__getitem__(key)
    def __contains__(self, obj):
        if type(obj) == type:
            for i in self.terms:
                if isinstance(i, obj): return True
        else: return self.terms.__contains__(obj)
    
    def scompone(self, poly: Polinomial = None):

        if isinstance(poly, str): poly = Polinomial.from_string(poly)

        if not poly: poly = Polinomial(terms=self.terms.copy())
        
        if poly == Trinomial:
            pa = poly[0]
            pb = poly[1]
            pc = poly[2]

            # 2 grade trinomial
            if pa.esponent == 2 and \
                pb.symbol == pa.symbol and \
                pb.esponent == 1 and not isinstance(pc, (Unknow, Literal, LiteralFraction)):

                a = Integer(pa.coefficient)
                b = Integer(pb.coefficient)
                
                delta = b ** 2 - 4*a*pc
                if delta > 0:
                    _rad = Radical(delta)
                    solutions = [LiteralFraction((_rad -b),(2*a)),
                                 LiteralFraction((-b -_rad),(2*a))]
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

    def literals(self) -> List[str]:
        out = []
        for i in self.terms:
            if isinstance(i, (Unknow, Literal)) and i.symbol not in out: out.append(i.symbol)
        return out

    def from_sum(ob1, ob2) -> Union[Integer, Unknow, Polinomial]:
        # n+n, x+n, x+x

        if isinstance(ob1, str): ob1 = Polinomial.from_string(ob1)
        if isinstance(ob2, str): ob2  = Polinomial.from_string(ob2)

        if isinstance(ob1, Polinomial):
            return ob1 + ob2
        elif isinstance(ob2, Polinomial):
            return ob2 + ob1

        if isinstance(ob1, (Integer, int, float, LiteralFraction, Fraction)):
            if isinstance(ob2, (Integer, int, float, LiteralFraction, Fraction)):
                return Integer(ob1 + ob2)
            if isinstance(ob2, (Unknow, Literal)):
                return Polinomial(terms=[ob1, ob2])
            
        if isinstance(ob1, (Unknow, Literal)):
            if isinstance(ob2, (Integer, int, float, Fraction)):
                return Polinomial(terms=[ob1, ob2])
            if isinstance(ob2, (Unknow, Literal)):
                if (ob1.symbol == ob2.symbol or ob1.symbol == ob2.symbol[::-1]) and ob1.esponent == ob2.esponent:
                    return Unknow([ob1.coefficient + ob2.coefficient, ob1.symbol])
                else:
                    return Polinomial(terms=[ob1, ob2])

    def from_sub(ob1, ob2):
        # n-n, x-n, x-x

        if isinstance(ob1, str): ob1 = Polinomial.from_string(ob1)
        if isinstance(ob2, str): ob2  = Polinomial.from_string(ob2)

        if isinstance(ob1, Polinomial):
            return ob1 - ob2
        elif isinstance(ob2, Polinomial):
            return -ob2 + ob1

        if isinstance(ob1, (Integer, int, float, Fraction, LiteralFraction)):
            if isinstance(ob2, (Integer, int, float, Fraction, LiteralFraction)):
                return Integer(ob1 - ob2)
            elif isinstance(ob2, (Unknow, Literal)):
                return Polinomial(terms=[ob1, -ob2])
            
        elif isinstance(ob1, (Unknow, Literal)):
            if isinstance(ob2, (Integer, int, float, Fraction, LiteralFraction, Radical)):
                return Polinomial(terms=[ob1, -ob2])
            elif isinstance(ob2, (Unknow, Literal)):
                if (ob1.symbol == ob2.symbol or ob1.symbol == ob2.symbol[::-1]) and ob1.esponent == ob2.esponent:
                    return Unknow([ob1.coefficient - ob2.coefficient, ob1.symbol, ob1.esponent])
                else:
                    return Polinomial(terms=[ob1, -ob2])

    def from_mul(ob1, ob2):
        # n*n, x*n, x*x

        if isinstance(ob1, str): ob1 = Polinomial.from_string(ob1)
        if isinstance(ob2, str): ob2  = Polinomial.from_string(ob2)

        if isinstance(ob1, (Integer, int, float, Fraction, LiteralFraction, Radical)):
            if isinstance(ob2, (Integer, int, float, Fraction, LiteralFraction)):
                return Integer(ob1 * ob2)
            elif isinstance(ob2, (Unknow, Literal)):
                return Unknow(ob2 * ob1)
            elif isinstance(ob2, Radical):
                return ob1 * ob2
            
        elif isinstance(ob1, (Unknow, Literal)):
            if isinstance(ob2, (Integer, int, float, Fraction, LiteralFraction)):
                return Unknow([ob1.coefficient * int(ob2), ob1.symbol])
            elif isinstance(ob2, (Unknow, Literal)):
                if ob1.symbol == ob2.symbol:
                    return Unknow([ob1.coefficient * ob2.coefficient, ob1.symbol, ob1.esponent + ob2.esponent])
                else:
                    return Polinomial(terms=[UnknownMultiplication(ob1, ob2)])
            elif isinstance(ob2, Radical):
                return Unknow([ob1.coefficient * ob2, ob1.symbol, ob1.esponent])
                
        elif isinstance(ob1, Polinomial):
            return ob1 * ob2

    def from_div(ob1, ob2):
        # n/n, x/n, x/x

        if isinstance(ob1, str): ob1 = Polinomial.from_string(ob1)
        if isinstance(ob2, str): ob2  = Polinomial.from_string(ob2)

        if isinstance(ob1, (Integer, int, float, Fraction, LiteralFraction)):
            if isinstance(ob2, (Integer, int, float, Fraction, LiteralFraction)):
                return Integer(ob1 / ob2)
            if isinstance(ob2, (Unknow, Literal)):
                return Unknow(ob1 / ob2)
            
        if isinstance(ob1, (Unknow, Literal)):
            if isinstance(ob2, (Integer, int, float, Fraction, LiteralFraction)):
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
                terms.append(Integer(i))

        if len(terms) == 0: return None
        else: return Polinomial(terms=terms) if len(terms) > 1 else terms[0]
    
    def semplify_and_format(self):

        numbers = []
        literals = []
        fractions = []
        radicals = []
        
        mons = [self]

        while len(mons) != 0:
            for i in mons.pop().terms:
                if isinstance(i, (Integer, int, float, Fraction)):
                    numbers.append(int(i))
                elif isinstance(i, (Unknow, Literal, UnknownMultiplication)):
                    literals.append(i)
                elif isinstance(i, Radical):
                    radicals.append(i)
                elif isinstance(i, Polinomial):
                    mons.append(i)
                elif isinstance(i, LiteralFraction):
                    fractions.append(i)

        self.terms.clear()
        
        umap = {}
        
        for i in literals:
            if not isinstance(i, UnknownMultiplication): 
                if i.esponent == 0: 
                    numbers.append(Integer(i.coefficient))
                    break
                key = i.symbol+'^'+str(i.esponent)   
            else:
                key = ''
                for l in i:
                    if l.esponent == 0: 
                        numbers.append(Integer(l.coefficient)) 
                        break
                    key += l.symbol + '^' + str(l.esponent)

            if not isinstance(umap.get(key), list):
                umap[key] = [i]
            else: umap[key].append(i)

        number = sum(numbers)
        if number != 0: self.terms.append(Integer(number))

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
        
        self.terms.reverse()
        fout = 0
        for f in fractions:
            if fout: fout = fout + i
            else: fout = i
        self.terms.append(fout) if fout else None

        rout = 0
        for r in radicals:
            if rout: rout = rout + r
            else: rout = r
        self.terms.append(rout) if rout else None

        if len(self.terms) == 1 and isinstance(self.terms[0], (int, float, Integer)):
            return Integer(self.terms[0])
        
        if len(self.terms) == 0:
            self.terms.append(Integer(0))
        
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
        terms = self.terms.copy()
        for i in range(len(terms)): terms[i] = -terms[i]
        return Polinomial(terms=terms)
    
    def __eq__(self, value):
        if isinstance(value, Polinomial):
            if self.terms == value.terms: return True
            else: return False
        if isinstance(value, Binomial) or value == Binomial:
            return True if len(self.terms) == 2 else False
        elif isinstance(value, Trinomial) or value == Trinomial:
            return True if len(self.terms) == 3 else False
        elif isinstance(value, Quadrinomial) or value == Quadrinomial:
            return True if len(self.terms) == 4 else False
        elif len(self.terms) == 1:
            if self.terms[0] == value: return True
            else: return False 
        return False

    def __add__(self, value):

        self = Polinomial(terms=self.terms.copy())

        if isinstance(value, str): value = Polinomial.from_string(value)

        if isinstance(value, (Integer, Fraction, LiteralFraction, int, float)):
            for i in self.terms:
                if isinstance(i, (Integer)):
                    self.terms.remove(i)
                    self.terms.append(i + value)
                    return self
            self.terms.append(value)
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

        if isinstance(value, (Integer, Fraction, LiteralFraction, int, float)):
            for i in self.terms:
                if isinstance(i, (Integer)):
                    self.terms.remove(i)
                    self.terms.append(i - value)
                    return self
            self.terms.append(-value)
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
        
        if isinstance(value, (Integer, int, float, Fraction, LiteralFraction, Unknow, Literal, Radical)):
            for i in self.terms:
                self.terms[self.terms.index(i)] = i * value
            return self
            
        if isinstance(value, Polinomial):
            outterms = []
            for i in self.terms:
                for t in value.terms.copy():
                    outterms.append(i*t)
            return Polinomial(terms=outterms)
    
    def __rmul__(self, value):
        return self * value
    
    def __truediv__(self, value):
        self = Polinomial(terms=self.terms.copy())

        if isinstance(value, str): value = Polinomial.from_string(value)
        
        if isinstance(value, (Integer, int, float, Fraction, LiteralFraction, Unknow, Literal)):
            for i in self.terms:
                if i % value != 0:
                    return LiteralFraction(self, value)
                self.terms[self.terms.index(i)] = i / value
            return self

        if isinstance(value, Polinomial):
            qu, rest = divmod(self, value)
            if rest == 0:
                return qu
            else: return LiteralFraction(self, value)      

    def __rtruediv__(self, value):
        return LiteralFraction(value, self)

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
    
    @classmethod
    def _pascal_triangle(self, esponent):
        if 0 < esponent < 5:
            return [int(n) for n in str(11*esponent)]
        elif esponent > 0:
            return [factorial(esponent)//(factorial(j)*factorial(esponent-j)) for j in range(esponent+1)]
        else: return []

    def __pow__(self, value):

        if isinstance(value, Fraction):
            return Radical(self**value.numerator, value.denominator)

        if self == Binomial and isinstance(value, (int, Integer)):
            terms = []
            a = self.terms[0]
            b = self.terms[1]

            n = value
            if isinstance(a, (Unknow, Literal)) and isinstance(b, (Unknow, Literal)):
                for k in range(0, n+1):
                    coeff = factorial(n) // factorial(k) // factorial(n-k)
                    if k == 0:
                        terms.append(Unknow([coeff, a.symbol, n]))
                    elif k == n:
                        terms.append(Unknow([coeff, b.symbol, k]))
                    else:
                        terms.append(Unknow([coeff, a.symbol, n-k]) * Unknow([1, b.symbol, k]))
            elif isinstance(b, (Unknow, Literal)) and isinstance(a, Integer):
                for k in range(0, n+1):
                    coeff = factorial(n) // factorial(k) // factorial(n-k)
                    if k == n:
                        terms.append((a ** k))
                    else:
                        terms.append(Unknow([coeff, b.symbol, n-k]) * (a ** k))
            elif isinstance(a, (Unknow, Literal)) and isinstance(b, Integer):
                for k in range(0, n+1):
                    coeff = factorial(n) // factorial(k) // factorial(n-k)
                    if k == n:
                        terms.append((b ** k))
                    else:
                        terms.append(Unknow([coeff, a.symbol, n-k]) * (b ** k))
            else:
                for k in range(0, n+1):
                    coeff = factorial(n) // factorial(k) // factorial(n-k)
                    if k == 0:
                        terms.append(a ** n)
                    elif k == n:
                        terms.append(b ** n)
                    else:
                        terms.append(coeff * (a **(n-k)) * (b ** k))

            return Polinomial(terms=terms)
        
        elif len(self.terms) == 1 and isinstance(self.terms[0], UnknownMultiplication):
            return self.terms[0] ** value
        
        else: raise ValueError('Cannot elvate non-binomial to a power or literals powers!')
    
    def __iter__(self):
        return iter(self.terms)

class LiteralFraction(object):

    numerator: Union[Polinomial, Unknow, Integer] = None
    denominator: Union[Polinomial, Unknow, Integer] = None
    literal: bool = False

    def __new__(cls, *args):
        self = super(LiteralFraction, cls).__new__(cls)

        if len(args) == 1 and isinstance(args[0], str): 
            fstr = args[0]
            fstr = fstr.split('/')

            for n, i in enumerate(fstr):
                if n == 0: self.numerator = Polinomial.from_string(i)
                elif n == 1: self.denominator = Polinomial.from_string(i)
            
            if isinstance(self.numerator, (Integer, int, float)) and isinstance(self.denominator, Integer): self.literal = False
            else: self.literal = True
        elif len(args) == 1 and isinstance(args[0], int): return Integer(args[0])
        elif len(args) == 1 and isinstance(args[0], float): return Fraction(args[0])
        elif len(args) == 2:
            if isinstance(args[0], (Integer, int)) and isinstance(args[1], (Integer, int)): return Fraction(int(args[0]), int(args[1])) if not int(args[0]) % int(args[1]) == 0 else int(args[0] / args[1])
            else:
                self.numerator = Polinomial.from_string(args[0]) if isinstance(args[0], str) else args[0]
                self.denominator = Polinomial.from_string(args[1]) if isinstance(args[1], str) else args[1]

                if isinstance(self.numerator, Polinomial): self.numerator = self.numerator.semplify_and_format()
                if isinstance(self.denominator, Polinomial): self.denominator = self.denominator.semplify_and_format()

                if isinstance(self.numerator, (Unknow, Literal, Polinomial, Radical)) or \
                    isinstance(self.denominator, (Unknow, Literal, Polinomial, Radical)): self.literal = True
                else: return Fraction(int(self.numerator), int(self.denominator))

        return self

    def __neg__(self):
        return LiteralFraction(-self.numerator, self.denominator)

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

class Equation(object):
    '''
Basic Expression Class
======================

It's used for expressions with only sum, subtraction, division and multiplication
without any parentesis!

    '''

    def __init__(self, first, second) -> None:
        self.first: Polinomial = first -second
        if isinstance(self.first, Polinomial):
            self.first.semplify_and_format()
            self.second = 0
        else: 
            self.first = first
            self.second = second

        Equation.example = property(lambda self: 0, lambda self, value: value)

        if isinstance(self.first, Polinomial):
            for i in self.first.literals():
                exec('setattr(Equation, \'{}\', property(lambda self: self.__getliteral__(\'{}\'), lambda self, value: self.__setliteral__(\'{}\', value)))'.replace('{}', i))

    def __getliteral__(self, literal):
        try:
            for i in self.first:
                if isinstance(i, (Unknow, Literal)) and i.symbol == literal:
                    return i
        except TypeError:
            pass
        raise AttributeError("'Equation' object has no attribute '{}'".format(literal))

    def __setliteral__(self, literal, value):
        print(literal, value)
        return self

    def __str__(self) -> str:
        return '{} = {}'.format(str(self.first), str(self.second)).replace('  ', ' ')

    def parse_expr(self, expr: str): #-> #List[Integer, Unknow]:
        
        fexpr = expr.replace('+', ' +').replace('-',' -'). replace('=', ' = ').replace('  ', ' ').replace('+ ', '+').replace('- ','-')

        parts = fexpr.split(' = ')

        fp = Polinomial.from_string(parts[0])
        sp = Polinomial.from_string(parts[1])

        eq = fp-sp

    def solve(self, unknow = None):
        if isinstance(self.first, Polinomial) and Unknow in self.first:
            uk = []
            num = []
            for i in self.first:
                if isinstance(i, Unknow):
                    uk.append(i)
                else: num.append(-i)

            if unknow == None and len(uk) == 1: unknow = uk[0].symbol
            else: return (Polinomial(uk), Polinomial(num))

            for i in uk:
                if not i.symbol == unknow:
                    num.append(i)
                    uk.remove(i)

            return Polinomial(num)/uk[0].coefficient

class System(object):

    def __init__(self, *equations: Equation) -> None:
        self.equations = []

        for i in equations:
            lp, np = i.solve()
            self.equations.append((lp, np))

    def solve(self):
        lps = []
        nps = []
        for i in self.equations:
            lps.append(i[0])
            nps.append(i[1][0])
        nps.reverse()

        if len(lps) == 2:
            if lps[0].literals() == lps[1].literals():
                a = lps[0][0]
                b = (lps[0] - a).semplify_and_format()[0].coefficient

                for i in lps[1]:
                    if i.symbol == a.symbol:
                        c = i
                        d = (lps[1] - c).semplify_and_format()[0].coefficient
                        break
                
                a = a.coefficient
                c = c.coefficient

                D = (a*d) - (b*c)

                FD = (nps[1]*d) - (b*nps[0])
                SD = (a*nps[0]) - (c*nps[1])

                FV = (lps[0][0].symbol, LiteralFraction(FD,D))
                SV = (lps[0][1].symbol, LiteralFraction(SD,D))

                return FV, SV