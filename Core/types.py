from typing import List, Union, Tuple
from fractions import Fraction

from math import factorial as _factorial
from functools import reduce as _reduce

SQRT_SYMBOL = '√'

class Binomial: pass
class Trinomial: pass
class Quadrinomial: pass

class Polinomial(object): ...
class Literal(object): ... 
class Unknow(object): ...
class Literal(Unknow): pass
class Integer(object): ...
class LiteralFraction(object): ...
class Equation(object): ...

def factors(obj1: Union[Polinomial, Unknow, Literal, Integer, int], *objs: Union[Polinomial, Unknow, Literal, Integer, int]):
    '''find all common factors between elements, if only one is passed, it returns all his factors'''
    def __factors(item: Union[Unknow, Literal, Integer]):
        def _number_factors(n):
            return list(set(_reduce(list.__add__,
                        ([i, abs(n)//i] for i in range(1, int(abs(n)**0.5) + 1) if abs(n) % i == 0))))
        def _literal_factors(l: Unknow):
            return [Unknow([1, l.symbol, i]) for i in range(1, l.esponent+1)]
        def _radical_factors(r: Radical):
            return [Radical(i, r.index) for i in factors(r.base)]
        if isinstance(item, (int, Integer)): return _number_factors(item)
        elif isinstance(item, (Unknow, Literal)):
            out = []
            nf = __factors(item.coefficient)
            for i in _literal_factors(item):
                for n in nf:
                    out.append(i*n)
            out += nf
            return out
        elif isinstance(item, Radical):
            out = []
            nf = __factors(item.coefficient)
            for i in _radical_factors(item):
                for n in nf:
                    out.append(i*n)
            return out
        elif isinstance(item, UnknownMultiplication):
            lf = {}
            for i in item.literals:
                lf[i.symbol] = _literal_factors(i/i.coefficient)
            out = []
            nf = _number_factors(item.coefficient)
            out = out + nf

            lp = None
            for i in lf.keys():
                if not lp: lp = lf[i]
                else:
                    _p = []
                    for f in lf[i]: _p += [k*f for k in lp]
                    lp += _p
                    lp += lf[i]
            for n in nf: 
                facts = [k*n for k in lp]
                for i in facts: out.append(i)
            return out
        elif isinstance(item, Polinomial):
            return factors(*[t for t in item])
        elif isinstance(item, LiteralFraction):
            out = __factors(item.numerator)
            out += [LiteralFraction(1, d, _avoid_semplification=True) for d in __factors(item.denominator)]
            return out

    if isinstance(obj1, Polinomial):
        return factors(*[t for t in obj1], *objs)
    else:
        if not objs: objs = []
        _count = len(objs) + 1
        _factors = []
        for i in (obj1, *objs): _factors += __factors(i)
        out = []
        for f in _factors:
            if _factors.count(f) >= _count and not f in out: 
                out.append(f)
        return out

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
        if isinstance(number, float): 
            if number.is_integer(): number = int(number)
            else: return number ** esponent
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
    
    def __eq__(self, value) -> bool:
        return int(self).__eq__(value)
    
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
        elif isinstance(value, (Radical, LiteralFraction)):
            return Polinomial(terms=[value, self])
        elif isinstance(value, Integer):
            return Integer((self.number**self.esponent) + (value.number**value.esponent))
        else:
            return self.number.__add__(value)

    def __sub__(self, value):
        if isinstance(value, (Unknow, Literal)):
            return value.__sub__(self.number)
        elif isinstance(value, (Radical, LiteralFraction)):
            return Polinomial(terms=[-value, self])
        elif isinstance(value, Integer):
            return Integer((self.number**self.esponent) - (value.number**value.esponent))
        else:
            return self.number.__sub__(value)

    def __mul__(self, value):
        if isinstance(value, (Unknow, Literal)):
            return value * self.number
        elif isinstance(value, (Radical, LiteralFraction)):
            return value * self
        elif isinstance(value, Integer):
            if value.number == self.number: return Integer(self.number, self.esponent + value.esponent)
            elif self.esponent == value.esponent: return Integer(self.number * value.number, self.esponent)
            else: return Integer((self.number**self.esponent) * (value.number**value.esponent))
        elif isinstance(value, Fraction):
            return value * int(self)
        else:
            return self.number.__mul__(value)

    def __truediv__(self, value):
        if isinstance(value, (Unknow, Literal)):
            return LiteralFraction(self, value)
        elif isinstance(value, Radical):
            return LiteralFraction(self, value)
        elif isinstance(value, Integer):
            if value.number == self.number: return Integer(self.number, self.esponent - value.esponent)
            elif self.esponent == value.esponent and (self.number / value.number).is_integer(): return Integer(self.number / value.number, self.esponent)
            else:
                div = (self.number**self.esponent) /(value.number**value.esponent)
                if div.is_integer():
                    return Integer(div)
                else: return LiteralFraction((self.number**self.esponent), (value.number**value.esponent))
        elif isinstance(value, Fraction):
            return (value**-1) * self 
        else:
            return self.number.__truediv__(value)

    def __floordiv__(self, value):
        rv = self.__truediv__(value)
        return round(rv) if isinstance(rv, float) else rv

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
        
        if isinstance(self.base, (Integer, int, float, Fraction)) and (self.base ** (1/self.index)).is_integer():
            return Integer(self.coefficient * self.base ** (1/self.index))
        else: return self.semplify() if not _avoid_semplification else self

    def semplify(self):
        esp = 1
        num = -1
        nin = -1

        if isinstance(self.base, (Integer, int, Fraction)):
            if (self.base ** (1/self.index)).is_integer():
                return Integer(self.coefficient * self.base ** (1/self.index))
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
                    else: nin = base.coefficient if not isinstance(base, (int, Integer)) else int(base)

                if num != -1:
                    return Radical([num, nin, self.index], _avoid_semplification=True)
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
            return '{}{}{}{}'.format(str(self.coefficient).replace('1',''), apex(self.index), SQRT_SYMBOL, self.base)
        else: 
            return '{}{}{}({})'.format(str(self.coefficient).replace('1',''), apex(self.index), SQRT_SYMBOL, self.base)

    def to_number(self):
        if isinstance(self.base, (Integer, int)): return int(self.base) ** (1/self.index)
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
                return ImaginaryUnit(self.coefficient * int(value), self.esponent) if self.symbol == 'i' else\
                    Unknow([self.coefficient * int(value), self.symbol, self.esponent])
            except Exception as e:
                import traceback
                print(traceback.format_exc())

    def __rmul__(self, value):
        return self.__mul__(value)

    def __truediv__(self, value):
        if isinstance(value, str): value = Polinomial.from_string(value)

        if isinstance(value, (Unknow, Literal)):
            return Polinomial.from_div(self, value)
        else:
            try: 
                self = Unknow([self.coefficient, self.symbol, self.esponent]) if not self.symbol == 'i' else \
                    ImaginaryUnit(self.coefficient, self.esponent)
                self.coefficient = self.coefficient / int(value)
                if self.coefficient.is_integer(): self.coefficient = int(self.coefficient)
                else: self.coefficient = Fraction.from_float(self.coefficient)
                return self
            except Exception:
                return LiteralFraction(self, value)         

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

        if len(self.literals) == 1: return self.literals[0]

        for i in self.literals:
            if isinstance(i, (int, Integer)):
                self.literals.remove(i)
            if self.coefficient: self.coefficient = self.coefficient * (i.coefficient if isinstance(i, (Unknow, Literal)) else i)
            else: self.coefficient = (i.coefficient if isinstance(i, (Unknow, Literal)) else i)

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
        return 0 - self

    def __str__(self) -> str:
        fstr = ''
        for i in self.literal_part():
            fstr += self[i].symbol + (apex(self[i].esponent) if self[i].esponent !=1 else '')
        return str(self.coefficient).replace('1','') + fstr
    
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
            _coeff = value.coefficient
            for i in self:
                if not isinstance(i, (int, Integer, Fraction)):
                    if i.symbol == value.symbol: _lit.append(i / value)
                    else: _lit.append(i)
                else: _coeff = _coeff / i
            if _coeff.is_integer(): _coeff = int(_coeff)
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
    
    def __new__(cls, terms: list = None) -> None:
        self = super(Polinomial, cls).__new__(cls)

        if isinstance(terms, Polinomial): return terms
        self.terms = terms if terms else []
        self.semplify_and_format()
        if len(self.terms) == 1: return self.terms[0]
        else: return self

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
        return fstr.replace('++', '+').replace('  ', ' ')[:-1]
    
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
                    return Unknow([ob1.coefficient + ob2.coefficient, ob1.symbol, ob1.esponent])
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
                    return UnknownMultiplication(ob1, ob2)
            elif isinstance(ob2, Radical):
                return Unknow([ob1.coefficient * ob2, ob1.symbol, ob1.esponent]) if not ob1.symbol == 'i' else \
                        ImaginaryUnit(ob1.coefficient * ob2, ob1.esponent)
                
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
                    return Unknow([LiteralFraction(ob1.coefficient, ob2.coefficient), ob1.symbol, ob1.esponent - ob2.esponent])
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

        self.terms.reverse()

        if len(self.terms) == 1 and isinstance(self.terms[0], (int, float, Integer)):
            return Integer(self.terms[0])
        
        if len(self.terms) == 0:
            self.terms.append(Integer(0))

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
            if self.mcd() % value == 0:
                outterms = []
                for i in self:
                    outterms.append(i / value)
                return Polinomial(outterms)
            for i in self.terms:
                try:
                    if i % value != 0:
                        return LiteralFraction(self, value)
                except TypeError: return LiteralFraction(self, value)
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
        
        elif len(self.terms) == 1 and isinstance(self.terms[0], UnknownMultiplication):
            return self.terms[0] ** value
        
        else: raise ValueError('Cannot elvate non-binomial to a power or literals powers!')
    
    def __iter__(self):
        return iter(self.terms)

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

                if isinstance(self.numerator, (Unknow, Literal, Polinomial, Radical, UnknownMultiplication)) or \
                    isinstance(self.denominator, (Unknow, Literal, Polinomial, Radical, UnknownMultiplication)): self.literal = True
                else: return Fraction(int(self.numerator), int(self.denominator))

        return self.semplify() if not _avoid_semplification else self

    def semplify(self):
        common = factors(self.numerator, self.denominator)
        
        if not common == [1]:
            highest = common[0]
            for i in common[1:]:
                if isinstance(i, (Unknow, Literal)) and isinstance(highest, (Unknow, Literal)):
                    if i.coefficient > highest.coefficient: highest = i
                elif isinstance(i, (Unknow, Literal)) and isinstance(highest, (Integer, int)):
                    if i.coefficient > highest: highest = i
                elif isinstance(i, (Integer, int)) and isinstance(highest, (Unknow, Literal)):
                    if i > highest.coefficient: highest = i
                else:
                    if i > highest: highest = i

            return LiteralFraction(self.numerator / highest, self.denominator / highest, _avoid_semplification=True) if highest != 1 else self
        else: return self

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
        elif isinstance(value, Polinomial):
            terms = []
            for i in value:
                terms.append(self * i)
            return Polinomial(terms)
        else:
            if self.denominator == value: return self.numerator
            else: return LiteralFraction(self.numerator * value, self.denominator)

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
        self.first: Polinomial = first -second
        if isinstance(self.first, Polinomial):
            self.second = 0
        else: 
            self.first = first
            self.second = second

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
        '''Under developement: transform string to equation'''

        raise NotImplemented('Under developement: transform string to equation')

        fexpr = expr.replace('+', ' +').replace('-',' -'). replace('=', ' = ').replace('  ', ' ').replace('+ ', '+').replace('- ','-')

        parts = fexpr.split(' = ')

        fp = Polinomial.from_string(parts[0])
        sp = Polinomial.from_string(parts[1])

        eq = fp-sp

    def _ordinate_equation(self, equation: Union[Polinomial, Equation, List[Unknow]] = None):
        if not equation: equation = self.first
        if isinstance(equation, Equation): equation = equation.first

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

        literals += others
        return literals

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
                    pc = num[0]

                    a = pa.coefficient
                    b = pb.coefficient

                    delta = b**2 - 4*a*pc
                    if delta > 0:
                        _rad = Radical(delta)
                        solutions = [LiteralFraction((_rad -b),(2*a)),
                                    LiteralFraction((-b -_rad),(2*a))]

                        f = Equation(Unknow('x')*solutions[0].denominator - solutions[0].numerator, 0).solve()
                        s = Equation(Unknow('x')*solutions[1].denominator - solutions[1].numerator, 0).solve()

                        return (f, s)
                    elif delta == 0:
                        rv = Equation(Radical(pa)+ Radical(pc), 0).solve()
                        return (rv, rv)
                    else:
                        raise NotImplementedError('Cannot get the square root of a negative number')
                elif len(uk) == 2 and uk[0].symbol == uk[1].symbol \
                    and (uk[0].esponent == 2 and uk[1].esponent == 1) and len(num) == 0:
                    rv = Polinomial(uk)/uk[0].symbol
                    print(rv)
                    return (0, Equation(rv).solve())
                elif len(uk) == 1:
                    rv = Radical(LiteralFraction(-sum(num), uk[0].coefficient))
                    return (rv, -rv)

            # 3 grade equation
            elif len(uk) == 3 and uk[0].symbol == uk[1].symbol == uk[2].symbol and\
                uk[0].esponent == 3 and uk[1].esponent == 2 and uk[2].esponent == 1:
                pa, pb, pc = uk
                pd = Polinomial(num)

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

                _mult = d1**2 - 4*d0**3
                if _mult < 0:
                    _rad = Radical(abs(_mult), _avoid_semplification=True)*I
                else: _rad = Radical(_mult, _avoid_semplification=True)
                C0 = Radical((d1 + _rad)/2, 3, _avoid_semplification=True)
                C1 = Radical((d1 - _rad)/2, 3, _avoid_semplification=True)

                F = (Radical(3)*I -1)/2

                results = []
                for k in range(3):
                    print(-LiteralFraction(1, 3*a))
                    print(b, C0, F**k)
                    print(b + C0*F**k + LiteralFraction(d0, C0*F**k, _avoid_semplification=True))
                    r1 = -LiteralFraction(1, 3*a) * (b + C0*F**k + LiteralFraction(d0, C0*F**k, _avoid_semplification=True))
                    if not r1 in results: results.append(r1)
                    r2 = -LiteralFraction(1, 3*a) * (b + C1*F**k + LiteralFraction(d0, C1*F**k, _avoid_semplification=True))
                    if not r2 in results: results.append(r2)

                return tuple(results)

            for i in uk:
                if not i.symbol == unknow:
                    num.append(i)
                    uk.remove(i)

            return LiteralFraction(Polinomial(num), uk[0].coefficient)
        
        else: return self.first

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

    def __new__(cls, coefficient=1, esponent=1):
        self = super(ImaginaryUnit, cls).__new__(cls)
        self.coefficient = coefficient
        self.symbol = 'i'
        self.esponent = esponent
        return self

    def __pow__(self, value):
        if isinstance(value, (int, Integer)) and (self.esponent * value) % 2 == 0:
            if (self.esponent * value) % 4 == 0: return self.coefficient**value
            else: return -self.coefficient**value
        else: 
            return ImaginaryUnit(self.coefficient ** value, self.esponent * value)
            
I = ImaginaryUnit()