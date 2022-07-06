import random

import numpy as np


def _average(value_1, value_2, w=0.5):
    return w * value_1 + (1 - w) * value_2


class Operator:
    arity = 0

    def eval(self, x, y, z1, z2):
        """
        Evaluate this operator depending on the input
        :param x: Screen horizontal position [-1, +1]
        :param y: Screen vertical position [-1, +1]
        :param z1: Random value [-1, +1]
        :param z2: Random value [-1, +1]
        :return: a float in [-1, +1]
        """
        pass

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        pass


class Operator1(Operator):
    arity = 1

    def __init__(self, e1):
        self.e1 = e1


class Operator2(Operator):
    arity = 2

    def __init__(self, e1, e2):
        self.e1 = e1
        self.e2 = e2


class Operator3(Operator):
    arity = 3

    def __init__(self, e1, e2, e3):
        self.e1 = e1
        self.e2 = e2
        self.e3 = e3


class X(Operator):
    def eval(self, x, y, z1, z2):
        return x

    def __str__(self):
        return 'x'


class Y(Operator):
    def eval(self, x, y, z1, z2):
        return y

    def __str__(self):
        return 'y'


class Z1(Operator):
    def eval(self, x, y, z1, z2):
        return z1

    def __str__(self):
        return 'z1'


class Z2(Operator):
    def eval(self, x, y, z1, z2):
        return z2

    def __str__(self):
        return 'z2'


class Sum(Operator2):
    def eval(self, x, y, z1, z2):
        value_1 = self.e1.eval(x, y, z1, z2)
        value_2 = self.e2.eval(x, y, z1, z2)
        return _average(value_1, value_2)

    def __str__(self):
        return 'Sum(%s, %s)' % (self.e1, self.e2)


class Product(Operator2):
    def eval(self, x, y, z1, z2):
        value_1 = self.e1.eval(x, y, z1, z2)
        value_2 = self.e2.eval(x, y, z1, z2)
        return value_1 * value_2

    def __str__(self):
        return 'Product(%s, %s)' % (self.e1, self.e2)


class Mod(Operator2):
    def eval(self, x, y, z1, z2):
        value_1 = self.e1.eval(x, y, z1, z2)
        value_2 = self.e2.eval(x, y, z1, z2)
        return np.fmod(value_1, value_2)

    def __str__(self):
        return 'Product(%s, %s)' % (self.e1, self.e2)


class Well(Operator1):
    def eval(self, x, y, z1, z2):
        value = self.e1.eval(x, y, z1, z2)
        return 1 - 2 / (1 + value*value) ** 8

    def __str__(self):
        return 'Well(%s)' % self.e1


class Tent(Operator1):
    def eval(self, x, y, z1, z2):
        value = self.e1.eval(x, y, z1, z2)
        return 1 - 2 * np.abs(value)

    def __str__(self):
        return 'Tent(%s)' % self.e1


class Sin(Operator1):
    def eval(self, x, y, z1, z2):
        phase = z1
        freq = z2
        value = self.e1.eval(x, y, z1, z2)
        return np.sin(phase + freq * value)

    def __str__(self):
        return 'Sin(%s)' % self.e1


class Level(Operator3):
    def eval(self, x, y, z1, z2):
        threshold = z1
        value_1 = self.e1.eval(x, y, z1, z2)
        value_2 = self.e1.eval(x, y, z1, z2)
        value_3 = self.e1.eval(x, y, z1, z2)
        return np.where(value_1 < threshold, value_2, value_3)

    def __str__(self):
        return 'Level(%s, %s, %s)' % (self.e1, self.e2, self.e3)


class Mix(Operator3):
    def eval(self, x, y, z1, z2):
        value_1 = self.e1.eval(x, y, z1, z2)
        value_2 = self.e1.eval(x, y, z1, z2)
        value_3 = self.e1.eval(x, y, z1, z2)

        weight = 0.5 + value_3 / 2
        return _average(value_1, value_2, weight)

    def __str__(self):
        return 'Mix(%s, %s, %s)' % (self.e1, self.e2, self.e3)


OPERATORS = [X, Y, Z1, Z2, Sum, Product, Mod, Well, Tent, Sin, Level, Mix]
NULLARY_OPERATORS = [op for op in OPERATORS if op.arity == 0]
NOT_NULLARY_OPERATORS = [op for op in OPERATORS if op.arity > 0]


def generate_random(max_size=50):
    if max_size <= 0:
        # We used up available size, generate a leaf of the expression tree
        operator_class = random.choice(NULLARY_OPERATORS)
        return operator_class()
    else:
        # randomly pick an operator whose arity > 0
        operator_class = random.choice(NOT_NULLARY_OPERATORS)

        max_input_size = int(max_size / operator_class.arity)
        operator_inputs = [
            generate_random(max_input_size)
            for i in range(operator_class.arity)
        ]
        return operator_class(*operator_inputs)
