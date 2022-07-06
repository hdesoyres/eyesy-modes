import math
import random
import time

import numpy as np
import pygame


def _average(value_1, value_2, w=0.5):
    return w * value_1 + (1 - w) * value_2


class Operator(object):
    arity = 0

    def __init__(self, etc):
        self.etc = etc

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

    def __init__(self, etc, e1):
        super(Operator1, self).__init__(etc)
        self.e1 = e1


class Operator2(Operator):
    arity = 2

    def __init__(self, etc, e1, e2):
        super(Operator2, self).__init__(etc)
        self.e1 = e1
        self.e2 = e2


class Operator3(Operator):
    arity = 3

    def __init__(self, etc, e1, e2, e3):
        super(Operator3, self).__init__(etc)
        self.e1 = e1
        self.e2 = e2
        self.e3 = e3


class K1(Operator):
    def eval(self, x, y, z1, z2):
        value = self.etc.knob1 * 2.0 - 1.0
        # print('K1: ', value)
        return value

    def __str__(self):
        return 'K1(etc)'


class Trigger(Operator):
    def eval(self, x, y, z1, z2):
        value = 1.0 if self.etc.audio_trig else 0.0
        # print('Trigger', value)
        return value

    def __str__(self):
        return 'Trigger(etc)'


class K2(Operator):
    def eval(self, x, y, z1, z2):
        value = self.etc.knob2 * 2.0 - 1.0
        return value

    def __str__(self):
        return 'K2(etc)'


class K3(Operator):
    """
    Not used
    """
    def eval(self, x, y, z1, z2):
        return self.etc.knob3 * 2.0 - 1.0

    def __str__(self):
        return 'K3(etc)'


class X(Operator):
    def eval(self, x, y, z1, z2):
        return x

    def __str__(self):
        return 'X(etc)'


class Y(Operator):
    def eval(self, x, y, z1, z2):
        return y

    def __str__(self):
        return 'Y(etc)'


class Z1(Operator):
    def eval(self, x, y, z1, z2):
        return z1

    def __str__(self):
        return 'Z1(etc)'


class Z2(Operator):
    def eval(self, x, y, z1, z2):
        return z2

    def __str__(self):
        return 'Z2(etc)'


class Sum(Operator2):
    def eval(self, x, y, z1, z2):
        value_1 = self.e1.eval(x, y, z1, z2)
        value_2 = self.e2.eval(x, y, z1, z2)
        return _average(value_1, value_2)

    def __str__(self):
        return 'Sum(etc, %s, %s)' % (self.e1, self.e2)


class Product(Operator2):
    def eval(self, x, y, z1, z2):
        value_1 = self.e1.eval(x, y, z1, z2)
        value_2 = self.e2.eval(x, y, z1, z2)
        value = value_1 * value_2
        return value

    def __str__(self):
        return 'Product(etc, %s, %s)' % (self.e1, self.e2)


class Mod(Operator2):
    def eval(self, x, y, z1, z2):
        value_1 = self.e1.eval(x, y, z1, z2)
        value_2 = self.e2.eval(x, y, z1, z2)
        return np.fmod(value_1, value_2)

    def __str__(self):
        return 'Mod(etc, %s, %s)' % (self.e1, self.e2)


class Well(Operator1):
    def eval(self, x, y, z1, z2):
        value = self.e1.eval(x, y, z1, z2)
        return 1 - 2 / (1 + value*value) ** 8

    def __str__(self):
        return 'Well(etc, %s)' % self.e1


class Tent(Operator1):
    def eval(self, x, y, z1, z2):
        value = self.e1.eval(x, y, z1, z2)
        return 1 - 2 * np.abs(value)

    def __str__(self):
        return 'Tent(etc, %s)' % self.e1


class Sin(Operator1):
    def eval(self, x, y, z1, z2):
        phase = z1
        freq = z2
        value = self.e1.eval(x, y, z1, z2)
        return np.sin(phase + freq * value)

    def __str__(self):
        return 'Sin(etc, %s)' % self.e1


class Level(Operator3):
    """
    NOT USED : NOT WORKING !!
    """
    def eval(self, x, y, z1, z2):
        threshold = z1
        value_1 = self.e1.eval(x, y, z1, z2)
        value_2 = self.e1.eval(x, y, z1, z2)
        value_3 = self.e1.eval(x, y, z1, z2)
        return np.where(value_1 < threshold, value_2, value_3)

    def __str__(self):
        return 'Level(etc, %s, %s, %s)' % (self.e1, self.e2, self.e3)


class Mix(Operator3):
    def eval(self, x, y, z1, z2):
        value_1 = self.e1.eval(x, y, z1, z2)
        value_2 = self.e1.eval(x, y, z1, z2)
        value_3 = self.e1.eval(x, y, z1, z2)

        weight = 0.5 + value_3 / 2
        return _average(value_1, value_2, w=weight)

    def __str__(self):
        return 'Mix(etc, %s, %s, %s)' % (self.e1, self.e2, self.e3)


# TODO: add trigger
OPERATORS = [K2, X, Y, Z1, Z2, Sum, Product, Mod, Well, Tent, Sin, Mix, Trigger]  # K1, K3, Level
NULLARY_OPERATORS = [op for op in OPERATORS if op.arity == 0]
NOT_NULLARY_OPERATORS = [op for op in OPERATORS if op.arity > 0]


def generate_random(etc, max_size=50):
    if max_size <= 0:
        # We used up available size, generate a leaf of the expression tree
        operator_class = random.choice(NULLARY_OPERATORS)
        return operator_class(etc)
    else:
        # randomly pick an operator whose arity > 0
        operator_class = random.choice(NOT_NULLARY_OPERATORS)

        max_input_size = int(max_size / operator_class.arity)
        operator_inputs = [
            generate_random(etc, max_input_size)
            for i in range(operator_class.arity)
        ]
        # print('operator_class: ', str(operator_class))
        # print('operator_inputs: ', operator_inputs)
        return operator_class(etc, *operator_inputs)


#### END OPERATOR


BYTES = 127

xs = None
ys = None
z1 = None
z2 = None
root_operator = None
last_op_index = 0


def safe_generate(etc):
    has_2d_ouput = False
    while not has_2d_ouput:
        root_operator = generate_random(etc, 3)
        has_2d_ouput = isinstance(root_operator.eval(xs, ys, z1, z2), np.ndarray)

    print(root_operator)
    return root_operator


def setup(screen, etc):
    global xs, ys, color_palette, z1, z2, root_operator

    # Create grid [-1, +1]
    x_range = np.arange(BYTES) / float(BYTES) * 2 - 1
    y_range = np.arange(BYTES) / float(BYTES) * 2 - 1
    grid = np.array(np.meshgrid(x_range, y_range)).T.reshape(-1, 2)
    xs = grid[:, 0]
    ys = grid[:, 1]
    z1 = 0.0
    z2 = 0.0

    # Generate operator
    root_operator = safe_generate(etc)

    # Remove annoying errors (generated by byte beat function)
    np.seterr(divide='ignore', invalid='ignore')


def _bound_z(z):
    return max(min(z, 1.0), -1.0)


def draw(screen, etc):
    global z1, z2, last_op_index, root_operator

    #
    current_op_index = int(etc.knob1 * 5)
    if current_op_index != last_op_index:
        root_operator = safe_generate(etc)
        last_op_index = current_op_index

    # Update z1 and z2
    z_speed = etc.knob3
    z1 = _bound_z(z1 + (random.random() - 0.5) * z_speed)
    z2 = _bound_z(z2 + (random.random() - 0.5) * z_speed)

    start_draw = time.time()
    image = generate_image(etc, z1, z2)

    start = time.time()
    image_surface = pygame.surfarray.make_surface(image)
    pygame.transform.scale(image_surface, screen.get_rect().size, screen)  # smoothscale is too slow
    # log_time('surface', start)

    # log_time('draw', start_draw)


def generate_image(etc, z1, z2):
    start = time.time()
    pixels = root_operator.eval(xs, ys, z1, z2)
    # print('pixels', pixels.shape)
    # print(pixels[:3])
    # log_time('root_operator', start)

    start = time.time()
    pixels = grayscale_to_rgb(etc, pixels)
    # log_time('grayscale_to_rgb', start)

    start = time.time()
    pixels = pixels.reshape((BYTES, BYTES, 3))
    # log_time('reshape', start)

    return pixels


def grayscale_to_rgb(etc, grayscaled):
    color_palette = generate_color_palette(etc.knob4, etc.knob5)
    zeros = np.zeros((grayscaled.shape[0], 3), dtype=np.uint8)
    grayscaled = ((grayscaled * 2 - 1) * 255).astype('uint8')
    colored = np.take(color_palette, grayscaled, axis=0, out=zeros)
    return colored


def grayscale_to_rgb_eye(etc, grayscaled):
    bg_color = etc.color_picker(etc.knob5)
    bg = np.tile(np.array(bg_color), (grayscaled.shape[0], 1)).astype('uint8')
    # print('bg', bg.shape)
    # print(bg[:3])

    fg_color = etc.color_picker(etc.knob4)
    fg = np.tile(np.array(fg_color), (grayscaled.shape[0], 1)).astype('uint8')
    # print('fg', fg.shape)
    # print(fg[:3])


    index = grayscaled > 0.5
    # print('INDEX:', index.shape)
    # print(index[:3])

    bg[index] = fg[index]
    # print('FINAL bg', bg.shape)
    # print(bg[:3])

    return bg


def generate_color_palette(from_color, to_color):
    """

    :param from_color: [0, 1]
    :param to_color: [0, 1]
    :return:
    """
    if from_color == to_color:
        from_color = 0.0
        to_color = 1.0

    step = (to_color - from_color) / 256.0
    scale = np.arange(from_color, to_color, step)
    red = 256 * (1 - (np.cos(scale * 3 * math.pi) * .5 + .5)) * scale
    green = 256 * (1 - (np.cos(scale * 7 * math.pi) * .5 + .5)) * scale
    blue = 256 * (1 - (np.cos(scale * 11 * math.pi) * .5 + .5)) * scale
    stacked = np.stack((red, green, blue), axis=-1).astype('uint8')
    return stacked


def log_time(name, start):
    if int(time.time()) % 10 == 1:
        print('%s %s ms' % (name, int((time.time() - start) * 1000)))
