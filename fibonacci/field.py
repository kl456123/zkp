# -*- coding: utf-8 -*-

from random import randint

class FieldElement:
    k_modulus = 3*2**30+1
    generator_val = 5

    def __init__(self, val):
        self.val = val % FieldElement.k_modulus

    def __add__(self, other):
        try:
            other = FieldElement.typecast(other)
        except AssertionError:
            return NotImplemented
        return FieldElement((self.val+ other.val)%FieldElement.k_modulus)

    def __mul__(self, other):
        try:
            other = FieldElement.typecast(other)
        except AssertionError:
            return NotImplemented
        return FieldElement((self.val * other.val)%FieldElement.k_modulus)

    def __eq__(self, other):
        if isinstance(other, int):
            other = FieldElement(other)
        return isinstance(other, FieldElement) and other.val==self.val

    def __pow__(self, n):
        assert n>=0
        cur_pow = self
        res = FieldElement(1)
        while n>0:
            if n%2==1:
                res *=cur_pow
            n = n//2
            cur_pow*=cur_pow
        return res

    def __repr__(self):
        # Choose the shorter representation between the positive and negative values of the element.
        return repr(self.val)


    @staticmethod
    def one():
        return FieldElement(1)

    @staticmethod
    def zero():
        return FieldElement(0)

    @staticmethod
    def generator():
        return FieldElement(FieldElement.generator_val)

    @staticmethod
    def typecast(other):
        if isinstance(other, int):
            return FieldElement(other)
        # assert isinstance(other, FieldElement), f'Type Mismatch FieldElement and {type(other)}'
        assert isinstance(other, FieldElement), f'Type mismatch: FieldElement and {type(other)}.'
        return other

    def is_order(self, n):
        assert n>=1
        h = FieldElement(1)
        for _ in range(1, n):
            h*=self
            if h==FieldElement(1):
                return False

        return h*self==FieldElement(1)

