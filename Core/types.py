from typing import List, Union, Tuple
from math import factorial as _factorial

from .utils import *

sign = lambda item: 1 if abs(item)/item > 0 else -1

class Radical(object):
    
    coefficient = 1
    base = None
    index = 2

    def __new__(cls, 
        value: Union[Unknow, Literal, LiteralFraction, int, float, Integer, Polinomial, 
                     List[Union[Unknow, Literal, LiteralFraction, int, float, Integer, Polinomial]]], 
        index: int = 2,
        coefficient: int = 1,
        _avoid_semplification=False) -> None:

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
        
        if isinstance(self.base, (Integer, int, float, Fraction)) and (abs(self.base) ** (1/self.index)).is_integer():
            if self.index % 2 == 0 and sign(self.base) < 0: 
                return ImaginaryUnit([Integer(self.coefficient * abs(self.base) ** (1/self.index))])
            return Integer(self.coefficient * sign(self.base) * self.base ** (1/self.index))
        elif isinstance(self.base, (Integer, int, float, Fraction)) and self.base < 0:
            self.base = abs(self.base)
            return ImaginaryUnit([self])
        else: return self.semplify() if not _avoid_semplification else self

    def semplify(self):
        esp = 1
        num = -1
        nin = -1

        if isinstance(self.base, (Integer, int, Fraction)):
            if self.index % 2 == 0 and self.base < 0:
                self.base = abs(self.base)
                return ImaginaryUnit(coefficient=self.semplify())
            elif (abs(self.base) ** (1/self.index)).is_integer():
                return Integer(sign(self.base) * self.coefficient * self.base ** (1/self.index))
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
                            num *= i

                    if len(rin) > 0:
                        nin = 1 if nin == -1 else nin
                        for i in rin:
                            nin *= i
                    else: nin = 1

                if num != -1:
                    return Radical([num * self.coefficient, nin, self.index], _avoid_semplification=True)
                else: return self
        elif isinstance(self.base, (Unknow, Literal)):
            if isinstance(self.base.coefficient, (int, Integer)):
                if self.index % 2 == 0 and self.base.coefficient < 0: 
                    self.base.coefficient = abs(self.base.coefficient)
                    return ImaginaryUnit([self.semplify()])
                if (abs(self.base.coefficient) ** (1/self.index)).is_integer():
                    num = (abs(self.base.coefficient) ** (1/self.index)) * sign(self.base.coefficient)
                    num = int(num)
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
                        return Radical([Unknow([abs(num), self.base.symbol, int(self.base.esponent / self.index)]), nin, self.index], _avoid_semplification=True)
                elif self.base.esponent > self.index:
                    esp = self.base.esponent
                    newesp = 0
                    while esp >= self.index:
                        esp -= self.index
                        newesp += 1
                    return Radical([Unknow([abs(num), self.base.symbol, newesp]), Unknow([nin, self.base.symbol, esp]), self.index], _avoid_semplification=True)
                else: 
                    return Radical([Integer(abs(num)), Unknow([nin, self.base.symbol, self.base.esponent]), self.index], _avoid_semplification=True)
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
            return '{}{}{}{}'.format(str(self.coefficient).replace('1','') if abs(self.coefficient) == 1 else str(self.coefficient), apex(self.index), ROOT_SYMBOL, self.base)
        else: 
            return '{}{}{}({})'.format(str(self.coefficient).replace('1','') if abs(self.coefficient) == 1 else str(self.coefficient), apex(self.index), ROOT_SYMBOL, self.base)

    def __repr__(self) -> str:
        return '<Radical: '+ str(self)+ '>'

    def to_number(self):
        if isinstance(self.base, (Integer, int)): return sign(self.base) * (abs(self.base) ** (1/self.index))
        else: return self

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
        if isinstance(value, (Integer, int, float, Fraction)):
            return Radical([self.coefficient * value, self.base, self.index], _avoid_semplification=True)
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
        if isinstance(value, (Integer, int, float, Fraction)):
            return Radical(
                [int(self.coefficient / value) if (self.coefficient / value).is_integer() 
                 else LiteralFraction(self.coefficient, value), 
                 self.base, self.index])
        elif isinstance(value, (Unknow, Literal, Polinomial)):
            return LiteralFraction(self, value)
        elif isinstance(value, Radical):
            if self.base == value.base and self.index == value.index:
                return self.coefficient / value.coefficient
            elif self.index == value.index:
                return Radical([self.coefficient / value.coefficient, self.base / value.base, self.index])
            elif self.base == value.base:
                return Radical([self.coefficient / value.coefficient, self.base, self.index - value.index])
            else: return LiteralFraction(self, value)

    def __rtruediv__(self, value):
        return LiteralFraction(value, self)

    def __pow__(self, value):
        if isinstance(value, (int, Integer)):
            return Radical([self.coefficient ** int(value), self.base ** int(value), self.index])
        
    def __gt__(self, value):
        if isinstance(value, (int, Integer)) and isinstance(self.base, (int, Integer)):
            return self.base ** (1/self.index) > value
        else: return False
    
    def __ge__(self, value):
        if isinstance(value, (int, Integer)) and isinstance(self.base, (int, Integer)):
            return self.base ** (1/self.index) >= value
        else: return False

    def __lt__(self, value):
        if isinstance(value, (int, Integer)) and isinstance(self.base, (int, Integer)):
            return self.base ** (1/self.index) < value
        else: return False

    def __le__(self, value):
        if isinstance(value, (int, Integer)) and isinstance(self.base, (int, Integer)):
            return self.base ** (1/self.index) <= value
        else: return False

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

        if self.coefficient == 0 and not return_if_0:
            return Integer(0)
        elif self.esponent == 0 and not return_if_0: return Integer(self.coefficient)

        if self.symbol == 'i': return ImaginaryUnit(self.coefficient, self.esponent)
    
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

    def __abs__(self): return Unknow([abs(self.coefficient), self.symbol, self.esponent])

    def __lt__(self, value):
        if isinstance(value, (int, Integer)):
            return False
        elif isinstance(value, (Unknow, Literal)):
            if self.symbol == value.symbol and self.esponent == value.esponent:
                return self.coefficient < value.coefficient
            else: return None
        else: return None
    
    def __gt__(self, value):
        if isinstance(value, (int, Integer)):
            return True
        elif isinstance(value, (Unknow, Literal)):
            if self.symbol == value.symbol and self.esponent == value.esponent:
                return self.coefficient > value.coefficient
            else: return None
        else: return None

    def __mod__(self, value):
        return self.coefficient % value
    
    def __rmod__(self, value):
        return value % self.coefficient

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
            return self.__new__(type(self), [self.coefficient * int(value), self.symbol, self.esponent])

    def __rmul__(self, value):
        return self.__mul__(value)

    def __truediv__(self, value):
        if isinstance(value, str): value = Polinomial.from_string(value)

        if isinstance(value, (Unknow, Literal)):
            return Polinomial.from_div(self, value)
        else:
            self = self.__new__(type(self), [self.coefficient, self.symbol, self.esponent])
            self.coefficient = self.coefficient / int(value)
            if isinstance(self.coefficient, float):
                if not self.coefficient.is_integer():
                    self.coefficient = Fraction.from_float(self.coefficient)
                else: self.coefficient = int(self.coefficient)
            return self
            
    def __rtruediv__(self, value):
        return LiteralFraction(value, self)

    def __pow__(self, value):
        if isinstance(value, str): value = Polinomial.from_string(value)

        if isinstance(value, (Unknow, Literal)):
            # Power with letter not implemented
            raise NotImplemented('Power with literals not implemented yet!')
            #return Unknow(self.coefficient ** value.coefficient,)
        elif isinstance(value, (int, Integer)):
            return Unknow([Integer(self.coefficient, value), self.symbol, self.esponent * value])

    def __mod__(self, value):
        if isinstance(value, (Unknow, Literal)):
            return self.coefficient % value.coefficient
        return self.coefficient % value

    def __str__(self) -> str:
        return '{}{}{}'.format(str(self.coefficient) if abs(self.coefficient) != 1 else ('-' if self.coefficient < 0 else ''), self.symbol, apex(self.esponent) if self.esponent != 1 else '')

    def __repr__(self) -> str:
        return '<Unknow: ' + str(self) + '>'

class UnknownMultiplication(object):

    literals = None
    coefficient = None

    def __new__(cls, *literals, coefficient_mult=1) -> None:

        self = super(UnknownMultiplication, cls).__new__(cls)

        ref = {}
        _num = 1
        for l in literals:
            if not isinstance(l, (int, Fraction, Integer)):
                if ref.get(l.symbol): ref[l.symbol] = ref[l.symbol] * l
                else: ref[l.symbol] = l
            else: _num = _num * l
        self.literals = list(ref.values())

        if len(self.literals) == 1: return self.literals[0] * coefficient_mult

        for i in self.literals:
            if isinstance(i, (int, Integer)):
                self.literals.remove(i)
            if self.coefficient: 
                self.coefficient = self.coefficient * (i.coefficient if isinstance(i, (Unknow, Literal)) else i)
            else: self.coefficient = (i.coefficient if isinstance(i, (Unknow, Literal)) else i)
            self.literals[self.literals.index(i)] = Unknow([1, i.symbol, i.esponent])

        self.coefficient *= coefficient_mult
        self.coefficient = self.coefficient * _num

        return self

    def literal_part(self) -> List[str]:
        fstr = []
        for i in self.literals:
            fstr.append(i.symbol)
        fstr.sort()
        return fstr
    
    def __eq__(self, value):
        if isinstance(value, UnknownMultiplication):
            if self.coefficient == value.coefficient:
                for n, i in enumerate(self.literals):
                    if i.symbol != value.literals[n].symbol or\
                       i.esponent != value.literals[n].esponent: return False
                return True
        return False
    
    def __neg__(self):
        return UnknownMultiplication(*self.literals, coefficient_mult = -self.coefficient)

    def __str__(self) -> str:
        fstr = ''
        for i in self.literal_part():
            fstr += self[i].symbol + (apex(self[i].esponent) if self[i].esponent !=1 else '')
        return str(self.coefficient).replace('1','') + fstr
    
    def __repr__(self) -> str:
        return '<UnknownMultiplication: '+ str(self)+ '>'
    
    def to_list(self) -> List[Union[int, Unknow]]:
        return self.literals
    
    def __add__(self, value):
        return Polinomial.from_sum(self, value)
    
    def __radd__(self, value):
        return self.__add__(value)

    def __sub__(self, value):
        return Polinomial.from_sub(self, value)
    
    def __rsub__(self, value):
        return -self.__sub__(value)

    def __mul__(self, value):
        
        if isinstance(value, str): value = Polinomial.from_string(value)

        if isinstance(value, (Integer, int, float, Fraction)):
            return UnknownMultiplication(*self.literals, coefficient_mult=value)
        if isinstance(value, (Unknow, Literal)):
            return UnknownMultiplication(*self.literals, value)

        if isinstance(value, UnknownMultiplication):
            return UnknownMultiplication(*value.literals,*self.literals)
        
        if isinstance(value, LiteralFraction):
            return value * self
    
    def __truediv__(self, value):
        
        if isinstance(value, str): value = Polinomial.from_string(value)

        if isinstance(value, (Integer, int, Fraction)):
            return UnknownMultiplication(*self.literals, coefficient_mult=LiteralFraction(1, value))
        
        elif isinstance(value, (Unknow, Literal)):
            _lit = []
            _coeff = LiteralFraction(self.coefficient, value.coefficient)
            for i in self:
                if not isinstance(i, (int, Integer, Fraction)):
                    if i.symbol == value.symbol: 
                        _lit.append((i/i.coefficient) / (value/value.coefficient))
                    else: _lit.append(i/i.coefficient)
                else: _coeff = _coeff / i
            if isinstance(_coeff, int) or _coeff.is_integer(): _coeff = int(_coeff)
            else: _coeff = LiteralFraction(self.coefficient, value.coefficient)
            return UnknownMultiplication(*_lit, coefficient_mult=_coeff)

        if isinstance(value, UnknownMultiplication):
            _lit = []
            _coeff = self.coefficient
            valuel: dict = {}
            for i in value.literals:
                valuel[i.symbol] = i
            for i in self:
                if not isinstance(i, (int, Integer)):
                    if i.symbol in value.literal_part():
                        _lit.append(i / valuel.pop(i.symbol))
                    else: _lit.append(i)
            if len(valuel.values()) == 0:
                return UnknownMultiplication(*_lit)
            else: return LiteralFraction(UnknownMultiplication(*_lit, coefficient_mult=self.coefficient), UnknownMultiplication(*valuel.values(), coefficient_mult=value.coefficient))
    
    def __pow__(self, value):

        if isinstance(value, str): value = Polinomial.from_string(value)

        if isinstance(value, (Integer, int, float, Fraction)):
            return Polinomial(terms=[UnknownMultiplication(*[i ** value for i in self.literals])])

    def __iter__(self):
        return iter(self.literals)

    def __getitem__(self, key): 
        for i in self:
            if i.symbol == key: return i

class Polinomial(object):

    terms: List[Union[Polinomial, Tuple[Union[int, str]]]] = None
    esponent: int = 1
    
    def __new__(cls, *items, terms: list = [], esponent=1) -> None:
        self = super(Polinomial, cls).__new__(cls)
        self.esponent = esponent
        if esponent == 0: return Integer(1)
        if not isinstance(terms, (list, tuple)): return terms
        self.terms = list(terms) + list(items)
        if len(self.terms) == 1: return self.terms[0]
        else: return self.semplify_and_format()

    def __str__(self) -> str:
        fstr = ''
        for i in self.semplify_and_format():
            if isinstance(i, (list,tuple)):
                e = str(i[0]) + i[1].symbol + i[2].symbol
                e = '+'+e if not e.startswith('-') else e
                fstr += e
            else: fstr += '+'+str(i) if not str(i).startswith('-') else str(i)

            fstr += ' '
        fstr = fstr.replace('++', '+').replace('  ', ' ')[:-1]
    
        if self.esponent != 1:
            return '(' + fstr + ')' + apex(self.esponent)
        else: return fstr

    def __repr__(self) -> str:
        return '<Polinomial: '+str(self)+'>'

    def __abs__(self): return self

    def __getitem__(self, key): return self.terms.__getitem__(key)

    def __contains__(self, obj):
        if type(obj) == type:
            for i in self.terms:
                if isinstance(i, obj): return True
        else: return self.terms.__contains__(obj)
    
    def scompone(self, poly: Polinomial = None):

        if isinstance(poly, str): poly = Polinomial.from_string(poly)
        elif not poly: poly = Polinomial(terms=self.terms.copy(), esponent=self.esponent)
        elif not isinstance(poly, Polinomial): poly = Polinomial(poly)

        if poly.esponent != 1: poly = poly._caluclate_pow_()

        ord_poly = Equation(0)._ordinate_equation(poly)
        
        if poly == Trinomial:
            pa, pb, *pc = ord_poly
            pc = sum(pc)

            # 2 grade trinomial
            if pa.esponent == 2 and \
                pb.symbol == pa.symbol and \
                pb.esponent == 1 and not isinstance(pc, (Unknow, Literal, LiteralFraction)):

                a = pa.coefficient
                b = pb.coefficient
                
                delta = b ** 2 - 4*a*pc
                if delta > 0:
                    _rad = Radical(delta)
                    solutions = [LiteralFraction((-b + _rad),(2*a)),
                                 LiteralFraction((-b - _rad),(2*a))]
                    
                    if isinstance(solutions[1], (Fraction, LiteralFraction)):
                        f = (Unknow(pa.symbol)*solutions[0].denominator - solutions[0].numerator)
                    else: f = (Unknow(pa.symbol) - solutions[0])
                    if isinstance(solutions[1], (Fraction, LiteralFraction)):
                        s = (Unknow(pa.symbol)*solutions[1].denominator - solutions[1].numerator)
                    else: s = (Unknow(pa.symbol) - solutions[1])

                    _coeff = ((solutions[0].denominator if isinstance(solutions[0], (Fraction, LiteralFraction)) else 0) + 
                       solutions[1].denominator if isinstance(solutions[1], (Fraction, LiteralFraction)) else 0)
                    
                    if _coeff != 0:
                        _coeff = LiteralFraction(a, _coeff)
                    else: _coeff = 1
                    return PolinomialMultiplication(f, s, coefficient=_coeff)

                elif delta == 0:
                    rv = Radical(pa)+ Radical(pc)
                    return PolinomialMultiplication(rv,rv)
                else:
                    raise NotImplementedError('Cannot get the square root of a negative number')
            
        elif poly == Quadrinomial: # cube of binomial
            other = poly.terms.copy()
            tgrade = []

            for i in poly:
                if not isinstance(i, UnknownMultiplication) and i.esponent == 3:
                    other.remove(i)
                    tgrade.append(i)

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
                    return PolinomialMultiplication(rv, rv)
                
        elif poly == Binomial:
            f = poly[0]
            s = poly[1]

            a = Radical(f)

            # subtraction of squares
            if not isinstance(a, Radical) and (s.coefficient if isinstance(s, (Unknow, Literal)) else s.number) < 0:
                b = Radical(abs(s))
                if not isinstance(b, Radical):
                    return PolinomialMultiplication((a +b), (a -b))
            
            # subtraction of cubes
            a = Radical(f, 3)
            if not isinstance(a, Radical):
                b = Radical(abs(s), 3)
                if not isinstance(b, Radical):
                    if (s.coefficient if isinstance(s, (Unknow, Literal)) else s.number) < 0: # positive
                        return PolinomialMultiplication((a - b),((a**2) + a*b +(b**2))) 
                    else: # negative
                        return PolinomialMultiplication((a + b),((a**2) - a*b +(b**2)))
        
        commonfactors = factors(poly)
        d = 0
        for f in commonfactors:
            if f > d: d = f

        res = poly / d
        if d != 1 and isinstance(res, Polinomial):
            res = res.scompone()
        
        return PolinomialMultiplication(res, coefficient=d)

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
        elif isinstance(ob1, PolinomialMultiplication):
            return ob1.to_polinomial() + ob2
        elif isinstance(ob2, PolinomialMultiplication):
            return ob2.to_polinomial() + ob1
        
        if isinstance(ob2, UnknownMultiplication):
            r = ob1
            ob1 = ob2
            ob2 = r
            del r

        if isinstance(ob1, (Integer, int, float, LiteralFraction, Fraction)):
            if isinstance(ob2, (Integer, int, float, LiteralFraction, Fraction)):
                return Integer(ob1 + ob2)
            if isinstance(ob2, (Unknow, Literal)):
                return Polinomial(terms=[ob1, ob2])
            
        elif isinstance(ob1, (Unknow, Literal)):
            if isinstance(ob2, (Integer, int, float, Fraction)):
                return Polinomial(terms=[ob1, ob2])
            elif isinstance(ob2, (Unknow, Literal)):
                if (ob1.symbol == ob2.symbol or ob1.symbol == ob2.symbol[::-1]) and ob1.esponent == ob2.esponent:
                    return Unknow([ob1.coefficient + ob2.coefficient, ob1.symbol, ob1.esponent])
                else:
                    return Polinomial(terms=[ob1, ob2])
                
        elif isinstance(ob1, UnknownMultiplication):
            if isinstance(ob2, (int, Integer, float, Fraction, Unknow, Literal)):
                return Polinomial(UnknownMultiplication(*ob1.literals, coefficient_mult=ob1.coefficient), ob2)
            elif isinstance(ob2, UnknownMultiplication):
                ob2l = ob2.literal_part()
                for i in ob1.literal_part():
                    if not (i in ob2l and ob1[i].esponent == ob2[i].esponent): return Polinomial(ob1, ob2)
                return UnknownMultiplication(*ob1.literals, coefficient_mult=(ob1.coefficient*ob2.coefficient))

    def from_sub(ob1, ob2):
        return Polinomial.from_sum(ob1, -ob2)

    def from_mul(ob1, ob2):
        # n*n, x*n, x*x

        if isinstance(ob1, str): ob1 = Polinomial.from_string(ob1)
        if isinstance(ob2, str): ob2  = Polinomial.from_string(ob2)

        if isinstance(ob1, (Integer, int, float, Fraction, LiteralFraction, Radical)):
            if isinstance(ob2, (Integer, int, float, Fraction, LiteralFraction)):
                return Integer(ob1 * ob2)
            elif isinstance(ob2, (Unknow, Literal)):
                return ob2 * ob1
            elif isinstance(ob2, Radical):
                return ob1 * ob2
            
        elif isinstance(ob1, (Unknow, Literal)):
            if isinstance(ob2, (Integer, int, float, Fraction, LiteralFraction)):
                return ob1.__new__(type(ob1), [ob1.coefficient * ob2, ob1.symbol])
            elif isinstance(ob2, (Unknow, Literal)):
                if ob1.symbol == ob2.symbol:
                    return ob1.__new__(type(ob1), [ob1.coefficient * ob2.coefficient, ob1.symbol, ob1.esponent + ob2.esponent])
                else:
                    return UnknownMultiplication(ob1, ob2)
            elif isinstance(ob2, Radical):
                return ob1.__new__(type(ob1), [ob1.coefficient * ob2, ob1.symbol, ob1.esponent])
                
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
                    return ob1.__new__(type(ob1), [LiteralFraction(ob1.coefficient, ob2.coefficient), ob1.symbol, ob1.esponent - ob2.esponent])
                else:
                    return LiteralFraction(ob1.symbol, ob2.symbol) * LiteralFraction(ob1.coefficient, ob2.coefficient)

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
                elif isinstance(i, PolinomialMultiplication):
                    mons.append(i.to_polinomial())

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

        for i in keys:
            if len(umap[i]) > 1:
                def summ(ls):
                    out = ls.pop(0)
                    for i in ls:
                        out = out + i
                    return out
                
                _i = summ(umap[i])
            else: 
                _i = umap[i][0]
            self.terms.append(_i)
        
        fout = None
        for f in fractions:
            if fout: fout = fout + f
            else: fout = f
        self.terms.append(fout) if fout else None

        rout = None
        for r in radicals:
            if rout: rout = rout + r
            else: rout = r
        self.terms.append(rout) if (rout and (isinstance(rout, Radical) and rout.coefficient != 0)) else None

        if len(self.terms) == 1 and isinstance(self.terms[0], (int, float, Integer)):
            return Integer(self.terms[0], esponent=self.esponent)
        
        if len(self.terms) == 0:
            self.terms.append(Integer(0))

        self.terms = Equation(0)._ordinate_equation(self.terms)

        return self

    def mcd(self):
        highest = 0
        for i in factors(self):
            if isinstance(i, (Unknow, Literal)) and isinstance(highest, (Unknow, Literal)):
                if abs(i.coefficient) > highest.coefficient: highest = abs(i)
            elif isinstance(i, (Unknow, Literal)) and isinstance(highest, (Integer, int)):
                if abs(i.coefficient) > highest: highest = abs(i)
            elif isinstance(i, (Integer, int)) and isinstance(highest, (Unknow, Literal)):
                if abs(i) > highest.coefficient: highest = abs(i)
            else:
                if abs(i) > highest: highest = abs(i)
        return highest

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
            if self.esponent != value.esponent: return False 
            for i in self:
                if not i in value.terms: return False
            return True
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

        self = self._caluclate_pow_()

        if isinstance(value, str): value = Polinomial.from_string(value)

        if isinstance(value, (Integer, Fraction, LiteralFraction, int, float)):
            for i in self.terms:
                if isinstance(i, (Integer, int)):
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
                    self.terms[self.terms.index(similar[0])] = similar[1] + i
                else: self.terms.append(i)

        elif isinstance(value, Radical):
            self.terms.append(value)

        elif isinstance(value, PolinomialMultiplication):
            return self + value.to_polinomial()

        return self
    
    def __radd__(self, value):
        return Polinomial(terms=[*self.terms, value])

    def __sub__(self, value):

        self = self._caluclate_pow_()

        if isinstance(value, str): value = Polinomial.from_string(value)

        if isinstance(value, (Integer, Fraction, LiteralFraction, int, float)):
            for i in self.terms:
                if isinstance(i, (Integer, int)):
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

        self: Polinomial = Polinomial(terms=self.terms.copy(), esponent=self.esponent)
        if not isinstance(self, Polinomial): return self * value

        if isinstance(value, str): value = Polinomial.from_string(value)
        
        if isinstance(value, (Integer, int, float, Fraction, LiteralFraction, Unknow, Literal, Radical)):
            if value == 1: return self
            elif value == -1: return -self     
            if self.esponent != 1:
                return PolinomialMultiplication(self, coefficient=value, _keep_type=True)
            else:
                for i in self.terms:
                    self.terms[self.terms.index(i)] = i * value
                return self
            
        elif isinstance(value, Polinomial):
            if self.terms == value.terms:
                return Polinomial(*value.terms, esponent = self.esponent + value.esponent)
            else:
                terms = []
                for i in value:
                    terms += list(self * i)
                return Polinomial(*terms)
        
        elif isinstance(value, PolinomialMultiplication):
            return value * self
    
    def __rmul__(self, value):
        return self * value
    
    def __truediv__(self, value):
        self: Polinomial = Polinomial(terms=self.terms.copy(), esponent=self.esponent)

        if isinstance(value, str): value = Polinomial.from_string(value)
        
        if isinstance(value, (Integer, int, float, Fraction, LiteralFraction, Unknow, Literal)):
            if self.mcd() % value == 0:
                outterms = []
                for i in self:
                    outterms.append(i / value)
                return Polinomial(*outterms)
            for i in self.terms:
                try:
                    if i % value != 0:
                        return LiteralFraction(self, value)
                except TypeError: return LiteralFraction(self, value)
                self.terms[self.terms.index(i)] = i / value
            return self

        elif isinstance(value, Polinomial):
            if self.terms == value.terms:
                return Polinomial(*value.terms, esponent = self.esponent - value.esponent)
            
            qu, rest = divmod(self, value)
            if rest == 0:
                return qu
            else: return LiteralFraction(self, value)

        elif isinstance(value, PolinomialMultiplication):
            return LiteralFraction(self, value)

    def __rtruediv__(self, value):
        return LiteralFraction(value, self)

    def __divmod__(self, value):
        letter = Equation(0)._ordinate_equation(value)[0]
        rest = Polinomial(terms=self.terms.copy())
        quotient = Polinomial()
        _r = Equation(0)._ordinate_equation(rest)
        while _r[0].esponent >= letter.esponent:
            i = _r[0]
            if isinstance(i, (Unknow, Literal)) and i.esponent >= letter.esponent:
                division = i/letter
                mult = value * division
                quotient = quotient + division

                rest: Polinomial = rest - mult
                _r = Equation(0)._ordinate_equation(rest)
        
        return (quotient, rest)   

    def __pow__(self, value):
        if isinstance(value, Fraction):
            return Radical(self**value.numerator, value.denominator)

        elif isinstance(value, (int, Integer)):
            return Polinomial(*self.terms, esponent = self.esponent * value)

    def _caluclate_pow_(self):

        if self.esponent == 1: return self
        if self == Binomial:
            terms = []
            a = self.terms[0]
            b = self.terms[1]

            n = self.esponent
            if isinstance(a, (Unknow, Literal)) and isinstance(b, (Unknow, Literal)):
                for k in range(0, n+1):
                    coeff = _factorial(n) // _factorial(k) // _factorial(n-k)
                    if k == 0:
                        terms.append(Unknow([coeff, a.symbol, n]))
                    elif k == n:
                        terms.append(Unknow([coeff, b.symbol, k]))
                    else:
                        terms.append(Unknow([coeff, a.symbol, n-k]) * Unknow([1, b.symbol, k]))
            elif isinstance(b, (Unknow, Literal)) and isinstance(a, Integer):
                for k in range(0, n+1):
                    coeff = _factorial(n) // _factorial(k) // _factorial(n-k)
                    if k == n:
                        terms.append((a ** k))
                    else:
                        terms.append(Unknow([coeff, b.symbol, n-k]) * (a ** k))
            elif isinstance(a, (Unknow, Literal)) and isinstance(b, Integer):
                for k in range(0, n+1):
                    coeff = _factorial(n) // _factorial(k) // _factorial(n-k)
                    if k == n:
                        terms.append((b ** k))
                    else:
                        terms.append(Unknow([coeff * a.coefficient, a.symbol, n-k]) * (b ** k))
            else:
                for k in range(0, n+1):
                    coeff = _factorial(n) // _factorial(k) // _factorial(n-k)
                    if k == 0:
                        terms.append(a ** n)
                    elif k == n:
                        terms.append(b ** n)
                    else:
                        terms.append(coeff * (a **(n-k)) * (b ** k))

            return Polinomial(terms=terms)
        
        else: 
            out = self
            for i in range(self.esponent):
                out = out * self
            return Polinomial(*out)
    
    def __iter__(self):
        return iter(self.terms)

class PolinomialMultiplication(object):

    polinomials: List[Polinomial] = None
    coefficient: int = 1

    def __new__(cls, *polinomials: Tuple[Polinomial], coefficient: int = 1, ensure_empty=False) -> PolinomialMultiplication:
        self = super(PolinomialMultiplication, cls).__new__(cls)

        self.coefficient = coefficient
        _polinomials = []
        _processed = []
        for i in polinomials:
            if isinstance(i, Polinomial):
                if not i in _processed:
                    _polinomials.append(Polinomial(*i, esponent=i.esponent*polinomials.count(i)))
                    _processed.append(i)
            elif isinstance(i, PolinomialMultiplication):
                self.coefficient = self.coefficient * i.coefficient
                _polinomials += i.polinomials
            else: self.coefficient = self.coefficient * i

        _processed = []
        self.polinomials = []
        for p in _polinomials:
            if not p in _processed:
                esp = 0
                _processed.append(p)
                for i in _polinomials:
                    if p.terms == i.terms:
                        esp += i.esponent
                        _processed.append(i)
                self.polinomials.append(Polinomial(*p, esponent=esp))

        if len(self.polinomials) == 0 and not ensure_empty: return self.coefficient
        else: return self

    def __str__(self) -> str:
        fstr = ''
        if self.coefficient != 1:
            fstr += str(self.coefficient)
        for i in self.polinomials:
            _str = str(i)
            if '(' in _str:
                fstr += _str
            else: fstr += '('+_str+')'

        return fstr
    
    def __repr__(self) -> str:
        return '<PolinomialMultiplication: '+ str(self)+ '>'

    def to_polinomial(self) -> Polinomial:
        out = 1
        for i in self:
            out = out * i
        return out
    
    def __neg__(self):
        return PolinomialMultiplication(*self.polinomials, coefficient=-self.coefficient)

    def __add__(self, value):
        return Polinomial.from_sum(self.to_polinomial(), value)
    
    def __radd__(self, value):
        return Polinomial.from_sum(self.to_polinomial(), value)
    
    def __sub__(self, value):
        return Polinomial.from_sub(self.to_polinomial(), value)
    
    def __rsub__(self, value):
        return -Polinomial.from_sub(value, self.to_polinomial())
    
    def __mul__(self, value):
        if isinstance(value, PolinomialMultiplication):
            return PolinomialMultiplication(*self.polinomials, *value.polinomials, coefficient=self.coefficient*value.coefficient)
        else:
            return PolinomialMultiplication(*self.polinomials, value, coefficient=self.coefficient, ensure_empty=True)

    def __rmul__(self, value):
        return self * value
    
    def __truediv__(self, value):
        _p = list(self)
        if isinstance(value, Polinomial) and value in _p:
            pcopy = _p.copy()
            pcopy.remove(value)
            return PolinomialMultiplication(*pcopy)
        elif isinstance(value, PolinomialMultiplication):
            pcopy = _p.copy()
            for i in value:
                if i in _p:
                    pcopy.remove(i)
            return PolinomialMultiplication(*pcopy)
        elif isinstance(value, (int, Integer)):
            return PolinomialMultiplication(*self.polinomials, coefficient=LiteralFraction(self.coefficient, value))
        return LiteralFraction(self, value)
    
    def __rtruediv__(self, value):
        return LiteralFraction(value, self)
    
    def __iter__(self):
        return iter(self.polinomials + [self.coefficient])

class LiteralFraction(object):

    numerator: Union[Polinomial, Unknow, Integer] = None
    denominator: Union[Polinomial, Unknow, Integer] = None
    literal: bool = False

    def __new__(cls, *args, _avoid_semplification=False):
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
        elif len(args) == 1 and isinstance(args[0], LiteralFraction): return args[0]
        elif len(args) == 2:
            if isinstance(args[0], (Integer, int)) and isinstance(args[1], (Integer, int)): return Fraction(int(args[0]), int(args[1])) if not int(args[0]) % int(args[1]) == 0 else int(args[0] / args[1])
            else:
                self.numerator = Polinomial.from_string(args[0]) if isinstance(args[0], str) else args[0]
                self.denominator = Polinomial.from_string(args[1]) if isinstance(args[1], str) else args[1]

                if self.denominator == 1: return self.numerator
                elif self.denominator == -1: return -self.numerator

                _types = (Unknow, Literal, Polinomial, Radical, UnknownMultiplication, PolinomialMultiplication, LiteralFraction)
                if isinstance(self.numerator, _types) or \
                    isinstance(self.denominator, _types): self.literal = True
                else: return Fraction(int(self.numerator), int(self.denominator))

        if self.denominator == 0: raise ZeroDivisionError('Passed 0 as denominator!')

        return self.semplify() if not _avoid_semplification else self

    def semplify(self):
        if isinstance(self.numerator, Polinomial):
            numerator = self.numerator.scompone()
        else: numerator = self.numerator
        if isinstance(self.denominator, Polinomial):
            denominator = self.denominator.scompone()
        else: denominator = self.denominator

        common = factors(numerator, denominator)
        if not common == [1]:
            self = LiteralFraction(numerator, denominator, _avoid_semplification=True)
            highest = common[0]
            for i in common[1:]:
                if isinstance(i, (Unknow, Literal)) and isinstance(highest, (Unknow, Literal)):
                    if i.coefficient > highest.coefficient: highest = i
                elif isinstance(i, (Unknow, Literal)) and isinstance(highest, (Integer, int)):
                    if i.coefficient > highest: highest = i
                elif isinstance(i, (Integer, int)) and isinstance(highest, (Unknow, Literal)):
                    if i > highest.coefficient: highest = i
                elif isinstance(i, Polinomial):
                    if isinstance(highest, Polinomial) and i.esponent > highest.esponent: highest = i
                    else: highest = i
                else:
                    if i > highest: highest = i

            return LiteralFraction(self.numerator / highest, 
                                   self.denominator / highest, _avoid_semplification=True) \
                   if highest != 1 else self
        else: return self

    def __neg__(self):
        return LiteralFraction(-self.numerator, self.denominator, _avoid_semplification=True)

    def __str__(self) -> str:
        num = ''
        if isinstance(self.numerator, Polinomial): num = '(' + self.numerator.__str__() + ')'
        else: num = str(self.numerator)

        den = ''
        if isinstance(self.denominator, Polinomial): den = '(' + self.denominator.__str__() + ')'
        else: den = str(self.denominator)

        return '{}/{}'.format(num, den)

    def __repr__(self) -> str:
        return '<LiteralFraction: '+ str(self)+ '>'

    def __eq__(self, value):
        if isinstance(value, LiteralFraction):
            if self.numerator == value.numerator and self.denominator == value.denominator: return True
            else: return False
        return False
    
    def __add__(self, value) -> Union[LiteralFraction, Fraction]:
        if value == 0: return self
        self = LiteralFraction(self.numerator, self.denominator, _avoid_semplification=True)
        if isinstance(value, (LiteralFraction, Fraction)):
            denominator = MCM(self.denominator, value.denominator)
            fn = self.numerator * (denominator / self.denominator)
            sn = value.numerator * (denominator / value.denominator)

            return LiteralFraction((fn + sn), denominator)
        else:
            self.numerator = self.numerator + (self.denominator * value)
        return self
    
    def __radd__(self, value):
        return self.__add__(value)

    def __sub__(self, value) -> Union[LiteralFraction, Fraction]:
        return self.__add__(-value)
    
    def __rsub__(self, value):
        return -self.__sub__(value)
    
    def __mul__(self, value):
        if isinstance(value, (LiteralFraction, Fraction)):
            return LiteralFraction(self.numerator * value.numerator, self.denominator * value.denominator)
        elif isinstance(value, Polinomial):
            terms = []
            for i in value:
                terms.append(self * i)
            return Polinomial(terms)
        else:
            if self.denominator == value: return self.numerator
            else: return LiteralFraction(self.numerator * value, self.denominator)

    def __rmul__(self, value):
        return self * value

    def __truediv__(self, value):
        self = LiteralFraction(self.numerator, self.denominator)
        if isinstance(value, (LiteralFraction, Fraction)):
            return LiteralFraction(self.numerator * value.denominator, self.denominator * value.numerator)
        elif isinstance(value, Polinomial):
            terms = []
            for i in value:
                terms.append(self * i)
            return Polinomial(terms)
        else:
            self.numerator = self.numerator + (self.denominator * value)
        return self
    
    def __pow__(self, value):
        return LiteralFraction(self.numerator ** value, self.denominator ** value)

class Equation(object):
    '''
Basic Expression Class
======================
Evaluate an expression and find the value of the unknown

Current Supported:
 - 1 grade equation
 - 2 grade equation
'''

    def __init__(self, first, second = 0) -> None:
        self.first: Polinomial = first
        if second != 0: self.first = self.first -second
        self.original = (first, second)

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
        return '{} = {}'.format(str(self.first), str(0)).replace('  ', ' ')

    def parse_expr(self, expr: str): #-> #List[Integer, Unknow]:
        '''Under developement: transform string to equation'''

        raise NotImplemented('Under developement: transform string to equation')

        fexpr = expr.replace('+', ' +').replace('-',' -'). replace('=', ' = ').replace('  ', ' ').replace('+ ', '+').replace('- ','-')

        parts = fexpr.split(' = ')

        fp = Polinomial.from_string(parts[0])
        sp = Polinomial.from_string(parts[1])

        eq = fp-sp

    @classmethod
    def _ordinate_equation(self, equation: Union[Polinomial, Equation, List[Unknow]] = None):
        if not equation: equation = self.first
        if isinstance(equation, Equation): equation = equation.first

        if isinstance(equation, (int, Integer, Unknow, Literal)): return equation

        umap = {}
        for i in equation:
            if isinstance(i, (Unknow, Literal)):
                if not i.symbol in umap.keys(): umap[i.symbol] = [i]
                else: umap[i.symbol].append(i)
            else: 
                if not 'others' in umap.keys(): umap['others'] = [i]
                else: umap['others'].append(i)
        if 'others' in umap.keys(): others = umap.pop('others')
        else: others = []

        literals = []
        for ls in umap.values():
            bf: Unknow = None
            for l in ls:
                if bf:
                    if bf.esponent > l.esponent: literals.append(l)
                    else: literals.insert(literals.index(bf), l)
                else: literals.append(l)
                bf = l

        return literals + others

    def solve(self, unknow = None):
        if isinstance(self.first, Polinomial) and Unknow in self.first:
            uk = []
            num = []
            for i in self.first:
                if isinstance(i, Unknow):
                    uk.append(i)
                else: num.append(i) if i != 0 else None

            uk = self._ordinate_equation(uk)

            if unknow == None and len(uk) == 1: unknow = uk[0].symbol
            # 2 grade equation
            if uk[0].esponent == 2:
                # complete
                if len(uk) == 2 and uk[0].symbol == uk[1].symbol \
                    and (uk[0].esponent == 2 and uk[1].esponent == 1) and len(num) == 1:
                    pa = uk[0]
                    pb = uk[1]
                    pc = sum(num)

                    a = pa.coefficient
                    b = pb.coefficient

                    delta = b**2 - 4*a*pc
                    if delta > 0:
                        _rad = Radical(delta)
                        solutions = [LiteralFraction((_rad -b),(2*a)),
                                    LiteralFraction((-b -_rad),(2*a))]
                        return tuple(solutions)
                    
                    elif delta == 0:
                        rv = Equation(Radical(pa) + sign(b)*Radical(pc)).solve()
                        return (rv, rv)
                    else:
                        raise NotImplementedError('Cannot get the square root of a negative number')

                elif len(uk) == 2 and uk[0].symbol == uk[1].symbol \
                    and (uk[0].esponent == 2 and uk[1].esponent == 1) and len(num) == 0:
                    rv = Polinomial(uk)/uk[0].symbol
                    return (0, Equation(rv).solve())

                elif len(uk) == 1:
                    rv = Radical(LiteralFraction(-sum(num), uk[0].coefficient))
                    return (rv, -rv)

            # 3 grade equation
            elif len(uk) == 3 and uk[0].symbol == uk[1].symbol == uk[2].symbol and\
                uk[0].esponent == 3 and uk[1].esponent == 2 and uk[2].esponent == 1:
                pa, pb, pc = uk
                pd = Polinomial(*num)

                a = pa.coefficient
                b = pb.coefficient
                c = pc.coefficient

                d0 = b**2 - 3*a*c
                d1 = 2*b**3 - 9*a*b*c + 27*pd*a**2

                if d0 == d1 == 0:
                    rv: Polinomial = Polinomial(3*a*Unknow(pa.symbol) + b)
                    rv = rv / rv.mcd()
                    return (rv,rv,rv)
                else:
                    pass
                    #raise NotImplementedError('''This third degree equation cannot be solved yet because of the forumula that require complex numbers!''')
                
                _factors = []
                for i in factors(pd):
                    if a*i**3 + b*i**2 + c*i + pd == 0:
                        _factors.append(Polinomial(Unknow(pa.symbol), -i))

                _factors = []

                if len(_factors) == 3: return [Equation(e).solve() for e in _factors]
                elif len(_factors) == 2:
                    _f = 1
                    for f in _factors:
                        _f = _f*f

                    _factors.append(divmod(self.first, _f)[0])
                    return [Equation(e).solve() for e in _factors]

                elif len(_factors) == 1:
                    _factors += list((self/_factors[0]).scompone())
                    return [Equation(e).solve() for e in _factors]
                
                else:
                    raise NotImplementedError('''This third degree equation cannot be solved yet because of the forumula that require complex numbers!''')
                    '''General cubic formula implementation'''
                    _mult = d1**2 - 4*d0**3
                    _rad = Radical(_mult, _avoid_semplification=True)
                    C = Radical((d1 + _rad)/2, 3, _avoid_semplification=True)

                    F = (Radical(-3) -1)/2

                    results = []
                    for k in range(3):
                        print(b, C, F**k)
                        print(b + C*F**k + LiteralFraction(d0, C*F**k, _avoid_semplification=True))
                        r1 = -LiteralFraction(1, 3*a) * (b + C*F**k + LiteralFraction(d0, C*F**k, _avoid_semplification=True))
                        if not r1 in results: results.append(r1)

                    return tuple(results)

            for i in uk:
                if not i.symbol == unknow:
                    num.append(i)
                    uk.remove(i)
            return LiteralFraction(-Polinomial(*num), uk[0].coefficient)
        elif isinstance(self.first, LiteralFraction):
            if not unknow: unknow = 'x'
            ec = self.create_existence_conditions(self.first.denominator)
            result = Equation(self.first.numerator).solve(unknow)
            return ec.verify(result)
        elif isinstance(self.first, Unknow): return 0
        else: 
            from .utils import IMPOSSIBLE
            return IMPOSSIBLE('x \u2209 C',
                'you are saying that {} = 0 !'.format(str(self.first)))

    @classmethod
    def create_existence_conditions(self, obj):
        from Core.utils import Condition, ExistenceConditions
        if isinstance(obj, Polinomial):
            poly = obj.scompone()
        elif isinstance(obj, PolinomialMultiplication):
            poly = obj
        elif isinstance(obj, Unknow):
            return ExistenceConditions(Condition(Unknow(obj.symbol), '!=', 0))
        
        _condition = []
        for i in poly:
            if isinstance(i, Polinomial):
                _liter = i.literals()
                if len(_liter) == 1:
                    vx = Equation(i).solve()
                    if not isinstance(vx, list): _condition.append(Condition(_liter[0], '!=', vx))
                    else:
                        for r in vx:
                            _condition.append(Condition(_liter[0], '!=', r))
        
        return ExistenceConditions(*_condition)

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

class ImaginaryUnit(Unknow):

    coefficient = 1
    esponent = 1

    def __new__(cls, *args, coefficient=1, esponent=1):
        self = super(ImaginaryUnit, cls).__new__(cls)

        if len(args) > 0 and isinstance(args[0], list):
            coefficient = args[0][0]
            esponent = 1 if not len(args[0]) == 3 else args[0][2]
        self.symbol = 'i'
        if esponent % 2 == 0:
            self = self.__pow__(esponent)
            return self * coefficient
        else:
            self.coefficient = coefficient
            return self

    def __pow__(self, value):
        if isinstance(value, (int, Integer)) and (self.esponent * value) % 2 == 0:
            if (self.esponent * value) % 4 == 0: return self.coefficient**value
            else: return -self.coefficient**value
        else: 
            return ImaginaryUnit(self.coefficient ** value, self.esponent * value)
            
I = ImaginaryUnit()