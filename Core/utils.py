class Binomial: pass
class Trinomial: pass
class Quadrinomial: pass

class Polinomial(object): ...
class UnknownMultiplication(object): ...
class PolinomialMultiplication(object): ...
class Literal(object): ... 
class Unknow(object): ...
class Literal(Unknow): pass
class Radical(object): ...
class Integer(object): ...
class LiteralFraction(object): ...
class Equation(object): ...

# Literal Symbols
PI_SYMBOL = u'\u213c'
INFINITY_SYMBOL = u'\u221e'
DELTA_SYMBOL = u'\u2206'
# Operator Symbols
ROOT_SYMBOL = u'\u221a'
INTEGRAL_SYMBOL = u'\u222b'
CONGRUENT_SYMBOL = u'\u2245'
NOT_CONGRUENT_SYMBOL = u'\u2246'
# Geometric Symbols
TRIANGLE_SYMBOL = u'\u25b2'
SQUARE_SYMBOL = u'\u25a0'
# Arrows Symbols
ARROWS_SYMBOLS = {
    'left': u'\u2190',
    'top': u'\u2191', 
    'right': u'\u2192',
    'bottom': u'\u2193',
    'right-left': u'\u21c4',
    'left-right': u'\u21c6'
}

class Complex(object):
    name = 'Complex'
    symbol = 'C'

    subclasses = []

class Real(Complex):
    name = 'Real'
    symbol = 'R'

    subclasses = []

class Irrationals(Real):
    name = 'Irrational'
    symbol = 'I'

    subclasses = []

class Rationals(Real):
    name = 'Rational'
    symbol = 'Q'

    subclasses = []

class Integers(Rationals):
    name = 'Integer'
    symbol = 'Z'

    subclasses = []

class Naturals(Integers):
    name = 'Natural'
    symbol = 'N'

    subclasses = []

Complex.subclasses = [Real]
Real.subclasses = [Rationals, Irrationals]
Rationals.subclasses = [Integers]
Integers.subclasses = [Naturals]

class EquationSolution(object):
    result = 0
    reason = None
    existance_conditions = None

    def __new__(cls, results=0, reason = None, existance_condition = None):
        self = super(EquationSolution, cls).__new__(cls)
        self.result = results
        self.reason = reason
        self.existance_conditions = existance_condition
        return self

    def __eq__(self, __o: object) -> bool:
        if __o == type(self):
            return True
        elif isinstance(__o, type(self)):
            return True
        else: return False

    def __str__(self) -> str:
        return str(type(self).__name__).capitalize() + ': '+ str(self.result)

    def __repr__(self) -> str:
        return '<'+ str(self) +'>'

class POSSIBLE(EquationSolution):
    def __str__(self) -> str:
        return 'Solution: '+ str(self.result)

class IMPOSSIBLE(EquationSolution):
    pass

class UNDEFINED(EquationSolution):
    pass

class Condition(object):
    first = None
    _type: str = None
    second = None

    def __init__(self, first, _type, second) -> None:
        self.first = first
        self._type = _type
        self.second = second

    def __str__(self) -> str:
        return str(self.first) + ' ' + self._type + ' ' + str(self.second)

class ExistenceConditions(object):
    conditions = []

    def __init__(self, *conditions) -> None:
        self.conditions = list(conditions)

    def verify(self, result, unknown='x', *other_conditions):
        if isinstance(result, EquationSolution): return result
        elif isinstance(result, (list, tuple)):
            _out = []
            for r in result:
                _out.append(self.verify(r))
            return _out

        _tp = []
        for i in self.conditions + list(other_conditions):
            if i.first == unknown: _tp.append(i)
        
        possible = True
        for i in _tp:
            if i._type == '!=' and not result != i.second:
                possible = False
                break
            elif i._type == '<' and not result < i.second:
                possible = False
                break
            elif i._type == '>' and not result > i.second:
                possible = False
                break
            elif i._type == '<=' and not result <= i.second:
                possible = False
                break
            elif i._type == '>=' and not result >= i.second:
                possible = False
                break

        if not possible:
            log = '{} {} {}, Existance Condition: {}'.format(
                unknown, 'not {}'.format(i._type) if not i._type == '!=' else '=', result, str(i)
            )
            return IMPOSSIBLE(result, reason = log, existance_condition = self)
            
        return POSSIBLE(result, reason = str(i), existance_condition = self)

    def __iter__(self):
        return iter(self.conditions)

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
    
    def __repr__(self) -> str:
        return '<Integer: '+ str(self) +'>'

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
        if isinstance(value, Integer):
            if self.esponent == value.esponent and self.number == value.number: return True
            else: return False
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
        return abs(int(self))
    
    def __radd__(self, value):
        return value.__add__(int(self))
    
    def __rsub__(self, value):
        return value.__add__(-int(self))
    
    def __rmul__(self, value):
        return value.__mul__(int(self))
    
    def __rtruediv__(self, value):
        return Fraction(value, int(self))

    def __add__(self, value):
        if isinstance(value, (Unknow, Literal)):
            return value.__add__(self.number)
        elif isinstance(value, (Radical, LiteralFraction)):
            return Polinomial(terms=[value, self])
        elif isinstance(value, Integer):
            return Integer((self.number**self.esponent) + (value.number**value.esponent))
        elif isinstance(value, Fraction):
            return value.__add__(int(self))
        else:
            return self.number.__add__(value)

    def __sub__(self, value):
        if isinstance(value, (Unknow, Literal)):
            return value.__sub__(self.number)
        elif isinstance(value, (Radical, LiteralFraction)):
            return Polinomial(terms=[-value, self])
        elif isinstance(value, Integer):
            return Integer((self.number**self.esponent) - (value.number**value.esponent))
        elif isinstance(value, Fraction):
            return -value.__add__(-int(self))
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

from typing import Union, List
from fractions import Fraction
from functools import reduce as _reduce

def MCM(*items: Union[Polinomial, Unknow, Literal, Integer, int]):
    
    _all = []
    _ref = {}
    for i in items:
        if isinstance(i, (int, Integer)):
            _ref[str(i)] = Integer.factorize(i)
            _all += _ref[str(i)]
        elif isinstance(i, Polinomial):
            _ref[str(i)] = list(i.scompone())
            _all += _ref[str(i)]
        elif isinstance(i, PolinomialMultiplication):
            _ref[str(i)] = list(i)
            _all += _ref[str(i)]

    def _highest(item, ref: dict):
        rv = 0
        for i in ref.values():
            if i.count(item) > rv:
                rv = i.count(item)
        return item ** rv

    _processed = []
    out = PolinomialMultiplication(ensure_empty=True)
    for i in _all:
        if not i in _processed:
            out = out * _highest(i, _ref)
            _processed.append(i)

    return out

def MCD(*items: Union[Polinomial, Unknow, Literal, Integer, int]):
    
    _all = []
    _ref = {}
    for i in items:
        if isinstance(i, (int, Integer)):
            _ref[str(i)] = Integer.factorize(i)
            _all += _ref[str(i)]
        elif isinstance(i, Polinomial):
            _ref[str(i)] = list(i.scompone())
            _all += _ref[str(i)]

    def _lowest(item, ref: dict):
        rv = None
        for i in ref.values():
            _c = i.count(item)
            if not rv: rv = _c
            if _c > 0 and _c < rv:
                rv = i.count(item)
            elif _c == 0: 
                return 1
        return item ** rv

    _processed = []
    out = 1
    for i in _all:
        if not i in _processed:
            out = out * _lowest(i, _ref)
            _processed.append(i)

    return out

def factors(*objects: Union[Polinomial, Unknow, Literal, LiteralFraction, Fraction, Radical, Integer, int]):
    '''find all common factors between elements, if only one is passed, it returns all his factors'''
    
    class FactorList(list): pass
    
    def __factors(item: Union[Unknow, Literal, Integer]):
        def _number_factors(n):
            return list(set(_reduce(list.__add__,
                        ([i, abs(n)//i] for i in range(1, int(abs(n)**0.5) + 1) if abs(n) % i == 0))))
        def _literal_factors(l: Unknow):
            return [l.__new__(type(l), [1, l.symbol, i]) for i in range(1, l.esponent+1)]
        def _radical_factors(r: Radical):
            return [r.__new__(type(r), i, r.index) for i in factors(r.base)]
        
        if isinstance(item, (int, Integer)): return _number_factors(item)
        elif type(item).__name__ in ('Unknow', 'Literal'):
            out = []
            nf = __factors(item.coefficient)
            for i in _literal_factors(item):
                for n in nf:
                    out.append(i*n)
            out += nf
            return out
        elif type(item).__name__ == 'Radical':
            out = []
            nf = __factors(item.coefficient)
            for i in _radical_factors(item):
                for n in nf:
                    out.append(i*n)
            return out
        elif type(item).__name__ == 'UnknownMultiplication':
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
        elif type(item).__name__ == 'Polinomial':
            return factors(*[t for t in item])
        elif type(item).__name__ in ('LiteralFraction', 'Fraction'):
            out = __factors(item.numerator)
            out += [item.__new__(type(item), 1, d) for d in __factors(item.denominator)]
            return out
        elif isinstance(item, FactorList): return list(item)

    def __polinomial_factors(*items: Union[Polinomial, PolinomialMultiplication]):
        count = len(items)

        _factors = []
        ordered_list: List[Polinomial] = []
        _non_poly = []
        for i in items:
            if type(i).__name__ != 'PolinomialMultiplication':
                _non_poly.append(i)
            else: 
                ordered_list += i.polinomials
                _non_poly.append(i.coefficient)

        _factors += factors(*_non_poly)

        _same_base = {}
        while len(ordered_list) != 0:
            for i in ordered_list:
                ordered_list.remove(i)
                if type(i).__name__ == 'Polinomial':
                    _to_remove = []
                    for p in ordered_list:
                        if type(p).__name__ == 'Polinomial' and p.terms == i.terms:
                            key = str(p.__new__(type(p), *p.terms))
                            if not _same_base.get(key):
                                _same_base[key] = []
                            if p.esponent > i.esponent:
                                _same_base[key].append(i)
                            else: _same_base[key].append(p)
                            _to_remove.append(p)
                    for tr in _to_remove: ordered_list.remove(tr)
                elif ordered_list.count(i) >= count:
                    _factors.append(i)
            
        for i in _same_base.values():
            if len(i) == count-1:
                _lowest = i[0]
                for p in i[1:]:
                    if p.esponent < _lowest.esponent:
                        _lowest = p
                _factors.append(_lowest)

        return _factors

    objs = list(objects)

    for i in objects:
        if type(i).__name__ == 'Polinomial':
            objs[objs.index(i)] = FactorList(factors(*[t for t in i]))
        elif type(i).__name__ == 'PolinomialMultiplication':
            return __polinomial_factors(*objects)
        elif isinstance(i, (tuple, list)):
            objs.remove(i)
            for tf in i: objs.append(FactorList(__factors(tf)))
    
    _count = len(objs)
    _factors = []
    for i in objs: _factors += __factors(i)
    out = []
    for f in _factors:
        if _factors.count(f) >= _count and not f in out: 
            out.append(f)

    return out if out != [] else [1]

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
