import os
import pygame
import math
import time
from enum import Enum

class LFOType(Enum):
    SAW = 0
    SINE = 1
    TRIANGLE = 2

class LFO : #uses three arguments: start point, max, and how far each step is.
    def __init__(self, start, max, step, current = 0, direction = 1, type=LFOType.TRIANGLE):
        self.start = start
        self.max = max
        self.step = step
        self.current = current
        self.direction = direction
        self.type = type

    def update(self):
        if (LFOType.SAW == self.type):
            if (self.current >= self.max) :
                self.current = self.start
            if (self.current <= self.start) :
                self.current = self.max
        elif (LFOType.TRIANGLE == self.type):
            # when it gets to the top, flip direction
            if (self.current >= self.max) :
                self.direction = -1
                self.current = self.max  # in case it steps above max

            # when it gets to the bottom, flip direction
            if (self.current <= self.start) :
                self.direction = 1
                self.current = self.start  # in case it steps below min

        self.current += self.step * self.direction

        return self.current

def setup(screen, etc) :
    global xr, yr, x8, y5, hund, otwen, drei, acht, sqmover, sqmover2
    xr = etc.xres
    yr = etc.yres
    x8 = xr/8
    y5 = yr/5
    hund = (99*xr)/1280
    otwen = (120*xr)/1280
    drei = (3*xr)/1280
    acht = (8*xr)/1280
    sqmover = LFO(-120, 120, 10, direction=-1, type=LFOType.TRIANGLE)
    sqmover2 = LFO(-120, 120, 1, type=LFOType.TRIANGLE)
    if drei == 0 :
        drei =1
    pass

def draw(screen, etc) :
    global xr, yr, x8, y5, hund, otwen, drei, acht, sqmover, sqmover2
    etc.color_picker_bg(etc.knob5)
    for i in range(0, 7) :

        sqmover.step = etc.knob1
        sqmover.max = int(etc.knob2*120)
        sqmover.start = int(etc.knob2*-120)
        xoffset = -sqmover.update()
        yoffset = sqmover.update()*0.8

        sqmover2.step = 0.2
        sqmover2.max = int(etc.knob2*120)
        sqmover2.start = int(etc.knob2*-120)
        xoffset2 = sqmover2.update()
        yoffset2 = -sqmover2.update()*0.8

        for j in range(0, 10) :
            x = (j*(x8))-(x8)
            y = (i*(y5))-(y5)

            rad = abs(etc.audio_in[(j-i)]) / 600
            width = int(etc.knob3*hund)+1
            color = get_color(etc, i, j)

            if (i%2) == 1 :
                x = j*(x8)-(x8) + xoffset + xoffset2
            if (j%2) == 1 :
                y = i*(y5)-(y5) + yoffset - yoffset2

            rect = pygame.Rect(0,0,width,width)
            rect.center = (x,y)
            #rect.inflate_ip(rad,rad)

            pygame.draw.circle(screen, color, (int(x), int(y)), int(width+rad))


def get_color(etc, i, j):
    sel = int(etc.knob4*8)

    # if etc.audio_trig:
    #    sel = (sel + 1) % 7



    if sel >= 7 :
        color = (int(127 + 127 * math.sin((i*7) * .1 + time.time())),
                 int(127 + 127 * math.sin((i*7) * .05+ time.time())),
                 int(127 + 127 * math.sin((i*7) * .01 + time.time())))
    if 1 <= sel < 2 :
        color = (int(127 + 127 * math.sin((i*7) * .1 + time.time())),42,75)
    if 2 <= sel < 3 :
        color = (75,int(127 + 127 * math.sin((i*7) * .1 + time.time())),42)
    if 3 <= sel < 4 :
        color = (42,75,int(127 + 127 * math.sin((i*7) * .1 + time.time())))
    if 4 <= sel < 5 :
        color = (int(127 + 127 * math.sin((i*7) * .1 + time.time())),255,127)
    if 5 <= sel < 6 :
        color = (255,int(127 + 127 * math.sin((i*7) * .1 + time.time())),127)
    if 6 <= sel < 7 :
        color = (205,200,int(127 + 127 * math.sin((i*7) * .1 + time.time())))
    if 1 > sel :
        color = (int(127 + 127 * math.sin((i*7) * .1 + time.time())),
                 int(127 + 127 * math.sin((i*7) * .1 + time.time())),
                 int(127 + 127 * math.sin((i*7) * .1 + time.time())))


    if etc.audio_trig and (i % 2 == 0) and (j % 2 == 0):
        return (color[1], color[2], color[0])
    else:
        return color
