# -*- coding: utf-8 -*-

import operator
from field import FieldElement
from list_utils import two_lists_tuple_operation, remove_trailing_elements

def trim_trailing_zeros(p):
    return remove_trailing_elements(p, FieldElement.zero())

class Polynomial():

    @classmethod
    def X(cls):
        return cls([FieldElement.zero(), FieldElement.one()])

    def __init__(self, coefficients, var='x'):
        self.poly = coefficients
        self.var = var

    def __eq__(self, other):
        try:
            other = polynomial.typecast(other)
        except AssertionError:
            return False
        return self.poly== other.poly

    def __add__(self, other):
        other = Polynomial.typecast(other)
        return Polynomial(two_lists_tuple_operation(
            self.poly, other.poly, operator.add, FieldElement.zero()))

    def __sub__(self, other):
        other = Polynomial.typecast(other)
        return Polynomial(two_lists_tuple_operation(
            self.poly, other.poly, operator.sub, FieldElement.zero()))

    def __mul__(self, other):
        other = Polynomial.typecast(other)
        poly1, poly2 = [[x.val for x in p.poly] for p in (self, other)]
        res = [0] * (self.degree() + other.degree() + 1)
        for i, c1 in enumerate(poly1):
            for j, c2 in enumerate(poly2):
                res[i+j] += c1*c2
        return Polynomial([FieldElement(x) for x in res])

    __rmul__ = __mul__  # To support <int> * <Polynomial>.

    @staticmethod
    def typecast(other):
        if isinstance(other, int):
            other = FieldElement(other)
        if isinstance(other, FieldElement):
            other = Polynomial([other])
        assert isinstance(other, Polynomial), f'Type mismatch: Polynomial and {type(other)}.'
        return other

    def degree(self):
        return len(trim_trailing_zeros(self.poly)) - 1


    def eval(self, point):
        point = FieldElement.typecast(point).val
        val = 0
        for coef in self.poly[::-1]:
            val = (val*point + coef.val)%FieldElement.k_modulus
        return FieldElement(val)

    def compose(self, other):
        other = Polynomial.typecast(other)
        res = Polynomial([])
        for coef in self.poly[::-1]:
            res = res* other + Polynomial([coef])
        return res

    def __call__(self, other):
        if isinstance(other, int):
            other = FieldElement(other)
        if isinstance(other, FieldElement):
            return self.eval(other)
        if isinstance(other, Polynomial):
            return self.compose(other)
        raise NotImplementedError

    def __pow__(self, other):
        """
        Calculates self**other using repeated squaring.
        """
        assert other >= 0
        res = Polynomial([FieldElement(1)])
        cur = self
        while True:
            if other % 2 != 0:
                res *= cur
            other >>= 1
            if other == 0:
                break
            cur = cur * cur
        return res

    def qdiv(self, other):
        pass

    @staticmethod
    def monomial(degree, coefficient):
        """
        Constructs the monomial coefficient * x**degree.
        """
        return Polynomial([FieldElement.zero()] * degree + [coefficient])

X = Polynomial.X()

def calculate_lagrange_polynomials(x_values):
    pass


def interpolate_poly_lagrange(y_values, lagrange_polynomials):
    pass

def interpolate_poly(x_values, y_values):
    assert len(x_values) == len(y_values)
    assert all(isinstance(val, FieldElement) for val in x_values),\
        'Not all x_values are FieldElement'
    assert all(isinstance(val, FieldElement) for val in y_values),\
        'Not all y_values are FieldElement'
