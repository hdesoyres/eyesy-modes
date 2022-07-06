import os
import pygame
import math
import time
import random
from enum import Enum

class LFOType(Enum):
    SAW = 0
    SINE = 1
    TRIANGLE = 2
    BOOLEAN = 3



COLORS_DICT = {
    'DEEPSKY': pygame.Color(0,191,255),
    'SKY': pygame.Color(135,206,235),
    #'SEA': pygame.Color(102,205,170),
    'SEA': (32,178,170),
    'SEA_INIT': (32,178,170),
    'SHORE': pygame.Color(255,255,255,100),
    'SAND': pygame.Color(255,228,181),
    'SAND_SHADOW': pygame.Color(210,180,140),
    'DARK_SAND': pygame.Color(109,49,9),
    'SUN': pygame.Color(255,215,0),
    'SILVER': pygame.Color(192,192,192),
    'SUNRAY': pygame.Color(255,215,0,100),
    'CRAB': pygame.Color(255,140,0),
    'CRAB_ALT': pygame.Color(255,150,0),
    'CLOUD': pygame.Color(220,220,220),
    'BLACK': pygame.Color(0,0,0),
    'BROWN': pygame.Color(139,69,19),
    'STARFISH': pygame.Color(244,164,96),
    'WHITE': pygame.Color(255,255,255),
    'LIPSTICK': pygame.Color(220,20,60),
    'DIAMOND': pygame.Color(240,255,255),
    'CAP': pygame.Color(0,128,0),
    'CAP_ALT': pygame.Color(0,128,0),
    'CLAM': pygame.Color(233,150,122),
    'CLAM_OPEN': pygame.Color(220,130,102),
    'CLAM_TONGUE': pygame.Color(205,92,92),
    'DOLPHIN': pygame.Color(70,130,180),
    'DOLPHIN_DARK': pygame.Color(60,110,160),
    'GREY': pygame.Color(100,100,100),
}

class Accessories(Enum):
    GLASSES = 0
    SHADOW = 1
    HEADPHONES = 2
    MOUSTACHE = 3
    MOUTH = 4
    GOLDEN_CHAIN = 5
    CAP = 6
    LIPSTICK = 7
    PIERCING_L = 8
    PIERCING_R = 9
    GOURMETTE_L = 10
    GOURMETTE_R = 11
    BEARD_SMALL = 12


class LFO:
    def __init__(self, start, max, step, current = 0, direction = 1, type=LFOType.TRIANGLE, params={}):
        self.start = start
        self.max = max
        self.step = step
        self.current = current
        self.direction = direction
        self.type = type
        self.params = params
        self.trigger = False

    def update(self):
        self.trigger = False
        if (LFOType.SAW == self.type):
            if (self.current >= self.max and self.direction > 0) :
                self.current = self.start
                self.trigger = True
            if (self.current <= self.start and self.direction < 0) :
                self.current = self.max
                self.trigger = True

        elif (LFOType.TRIANGLE == self.type or LFOType.BOOLEAN == self.type):
            # when it gets to the top, flip direction
            if (self.current >= self.max) :
                self.direction = -1
                self.current = self.max  # in case it steps above max
                self.trigger = True

            # when it gets to the bottom, flip direction
            if (self.current <= self.start) :
                self.direction = 1
                self.current = self.start  # in case it steps below min
                self.trigger = True
            if (LFOType.BOOLEAN == self.type):
                self.value = round(self.current)

        self.current += self.step * self.direction

        return self.current

    def getAdvancement(self):
        adv = (self.current - self.start)/(self.max-self.start)
        if (self.direction > 0):
            return adv
        else:
            return 1 - adv


def setup(screen, etc):
    global travelingLoop, seaLoop, gwidth, gheight, smartRythmLFO, cloudsLoopArray, knobFLO, flipperRotate, flipperHoriz, boatLFO1, boatLFO2, randomCrabLFO

    gwidth=1280
    gheight=720
    travelingLoop = LFO(0, gwidth, 1, direction=1,type=LFOType.SAW)
    seaLoop = LFO(-10, 10, 0.3, direction=1,type=LFOType.TRIANGLE)
    cloudsLoopArray = [LFO(0, gwidth, 2, direction=1,type=LFOType.SAW, params={'height':40}), LFO(0, gwidth, 1, current=500, direction=1,type=LFOType.SAW, params={'height':80})]
    smartRythmLFO = LFO(-10, 10, 1, current=0, direction=1,type=LFOType.TRIANGLE)
    knobFLO = LFO(0, 1, 0.01, current=0, direction=1, type=LFOType.BOOLEAN)
    flipperRotate = LFO(-40, 40, 1, current=0, direction=-1, type=LFOType.SAW)
    flipperHoriz = LFO(-100, gwidth, 2, direction=1,type=LFOType.SAW)
    boatLFO1 = LFO(-100, gwidth, 1, direction=1,type=LFOType.SAW)
    boatLFO2 = LFO(-100, gwidth + 150, 1, current=gwidth, direction=-1,type=LFOType.SAW)
    randomCrabLFO = LFO(-100, gwidth + 150, 1, current=-100, direction=1,type=LFOType.SAW, params={'accessories':randomAccessories()})

def draw(screen, etc):
    global travelingLoop, seaLoop, gwidth, gheight, cloudsLoopArray, smartRythmLFO, knobFLO, flipperRotate, flipperHoriz, boatLFO1, boatLFO2, randomCrabLFO

    etc.color_picker_bg(etc.knob5)
    knobFLO.step = etc.knob1*0.2
    updateLFO(etc)

    drawBG(screen, etc)

def randomAccessories(max=12):
    accessories = []
    r = random.randint(0, max)
#    for i in range(r):
#        accessories.append(random.choice(list(Accessories)))

    return accessories

def updateLFO(etc):
    global travelingLoop, seaLoop, cloudsLoopArray, smartRythmLFO, knobFLO, flipperRotate, flipperHoriz, boatLFO1, boatLFO2, randomCrabLFO
    travelingLoop.update()

    for cloudLFO in cloudsLoopArray:
        cloudLFO.update()
        if cloudLFO.trigger:
            r = random.randint(0, 2)
            if r == 0 and len(cloudsLoopArray) > 1:
                cloudsLoopArray.remove(cloudLFO)
            if r == 1:
                cloudsLoopArray.append(LFO(0, gwidth, 0.8 + (random.random()*2), direction=(1 if random.random() > 0.5 else -1),type=LFOType.SAW, params={'height':int(20+random.random()*100)}))

    seaLoop.update()
    knobFLO.update()
    flipperRotate.update()
    flipperHoriz.update()
    boatLFO1.update()
    boatLFO2.update()
    randomCrabLFO.update()

    if randomCrabLFO.trigger:
        randomCrabLFO.params={'accessories':randomAccessories()}

    if etc.audio_trig:
        smartRythmLFO.step=(math.pow(1+getAudioInRatio(etc)*4,3)/(4*(1+smartRythmLFO.getAdvancement())))
        smartRythmLFO.update()


def getAudioInRatio(etc):
    return abs(etc.audio_in[0] / 48000.0)

def drawBG(screen, etc):
    global travelingLoop, seaLoop, gwidth, gheight, cloudsLoopArray, smartRythmLFO, knobFLO, boatLFO1, boatLFO2, randomCrabLFO

    perpective = etc.knob1
    centerCoords = (gwidth - 100, 60)
    radius = 30

    COLORS_DICT['SEA'] = (int(COLORS_DICT['SEA_INIT'][0]+seaLoop.current), int(COLORS_DICT['SEA_INIT'][1]+seaLoop.current), int(COLORS_DICT['SEA_INIT'][2]+seaLoop.current))

    radius = radius + radius*abs(etc.audio_in[0]) / 10000
    jump = abs(etc.audio_in[0]) / 3000

    shoreY = gheight / 4 + gheight / 3 + seaLoop.current

    pygame.draw.rect(screen, COLORS_DICT['SKY'], [0, 0, gwidth, gheight / 3])
    drawSun(screen, etc, centerCoords, radius)
    pygame.draw.rect(screen, COLORS_DICT['SAND'], [0, shoreY, gwidth, gheight])
    pygame.draw.rect(screen, COLORS_DICT['SEA'], [0, gheight / 3, gwidth, gheight / 4 + seaLoop.current])

    for cloudLFO in cloudsLoopArray:
        drawCloud(screen, etc, (cloudLFO.current, cloudLFO.params['height'] +jump))

    #drawStarfish(screen, etc, (500, 200))

    drawSmallBoat(screen, etc, (boatLFO1.current, 200 + knobFLO.value*2), knobFLO, direction=1)
    drawSmallBoat(screen, etc, (boatLFO2.current, 220 + knobFLO.value*2), knobFLO)

    drawFlipper(screen, etc, (flipperHoriz.current, 250), flipperRotate.current)
    pygame.draw.rect(screen, COLORS_DICT['SEA'], [0, 290, gwidth, 100])

    drawCrab(screen, etc, (300 + seaLoop.current * 8, 375), [Accessories.GOLDEN_CHAIN, Accessories.HEADPHONES])
    drawCrab(screen, etc, (980 + seaLoop.current * 8, 372), [Accessories.GLASSES, Accessories.MOUSTACHE])
    pygame.draw.rect(screen, COLORS_DICT['SEA'], [0, 380, gwidth,  30])
    pygame.draw.rect(screen, COLORS_DICT['SHORE'], [0, shoreY, gwidth, (seaLoop.max + seaLoop.current) / 2])

    drawCrab(screen, etc, (640 + seaLoop.current * 8, 580), [Accessories.GLASSES, Accessories.SHADOW, Accessories.MOUTH, Accessories.GOLDEN_CHAIN, Accessories.MOUSTACHE])
    drawCrab(screen, etc, (440 + seaLoop.current * 8, 500), [Accessories.SHADOW, Accessories.MOUTH, Accessories.CAP])
    drawCrab(screen, etc, (840 + seaLoop.current * 8, 520), [Accessories.SHADOW, Accessories.MOUTH, Accessories.BEARD_SMALL, Accessories.GOURMETTE_L, Accessories.GOURMETTE_R, Accessories.PIERCING_L, Accessories.PIERCING_R])

    dawClam(screen, etc, (100, 550), smartRythmLFO.getAdvancement() > 0.5)
    dawClam(screen, etc, (1200, 550), smartRythmLFO.getAdvancement() > 0.5)
    dawClam(screen, etc, (200, 650), smartRythmLFO.getAdvancement() > 0.5)
    dawClam(screen, etc, (1100, 650), smartRythmLFO.getAdvancement() > 0.5)

    drawWorm(screen,etc, (150, 500), knobFLO)
    drawWorm(screen,etc, (1250, 500), knobFLO)
    drawWorm(screen,etc, (1150, 450), knobFLO)


def drawSun(screen, etc, centerCoords, radius):
    pygame.draw.circle(screen, COLORS_DICT['SUN'], centerCoords, radius)

def drawCloud(screen, etc, centerCoords):
    target_rect = pygame.Rect((0, 0, 100, 80))
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)

    pygame.draw.ellipse(shape_surf, COLORS_DICT['CLOUD'], (0, 5, 80, 40))
    pygame.draw.ellipse(shape_surf, COLORS_DICT['CLOUD'], (10, 3, 20, 20))
    pygame.draw.ellipse(shape_surf, COLORS_DICT['CLOUD'], (30, 0, 30, 30))
    pygame.draw.ellipse(shape_surf, COLORS_DICT['CLOUD'], (45, 3, 20, 15))
    pygame.draw.ellipse(shape_surf, COLORS_DICT['CLOUD'], (50, 23, 40, 20))

    screen.blit(shape_surf, centerCoords)
    return shape_surf

def drawStarfish(screen, etc, centerCoords):
    pygame.draw.polygon(screen, COLORS_DICT['STARFISH'], [
        (centerCoords[0], centerCoords[1]),
        (centerCoords[0]+10, centerCoords[1]+10),
        (centerCoords[0]+10, centerCoords[1]+5),
        (centerCoords[0], centerCoords[1]),
    ])

def drawSmallBoat(screen, etc, centerCoords, boolLfo, direction=0):
    target_rect = pygame.Rect((0, 0, 52, 52))
    surface = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    
    pygame.draw.polygon(surface, COLORS_DICT['BROWN'], [
        (0, 40),
        (50, 40),
        (41, 49),
        (8, 49)
    ])
    if (direction == 1):
        pygame.draw.line(surface, COLORS_DICT['BROWN'], (20, 0), (20, 40), 3)
        pygame.draw.polygon(surface, COLORS_DICT['WHITE'], [
            (23, 39),
            (23, 0),
            (34, 22),
            (39, 37),
        ])
        pygame.draw.arc(surface, COLORS_DICT['WHITE'], (-1, 0, 40, 80), 0.1, 1.3, 4)
    else:
        pygame.draw.line(surface, COLORS_DICT['BROWN'], (30, 0), (30, 40), 3)
        pygame.draw.polygon(surface, COLORS_DICT['WHITE'], [
            (27, 39),
            (27, 0),
            (16, 22),
            (13, 37),
        ])
        pygame.draw.arc(surface, COLORS_DICT['WHITE'], (13, 0, 40, 80), 1.87, 3, 4)

    if boolLfo.value == 0:
        pygame.draw.line(surface, COLORS_DICT['SHORE'], (2, 50), (48, 50), 2)
    else:
        pygame.draw.line(surface, COLORS_DICT['SHORE'], (3, 48), (47, 48), 2)

    screen.blit(surface, centerCoords)


def drawWorm(screen, etc, centerCoords, boolLfo):
    heightDiff = 10 + etc.knob4 * 40
    pygame.draw.ellipse(screen, COLORS_DICT['BLACK'], (centerCoords[0] - 6, centerCoords[1] - 4, 13, 8))
    pygame.draw.line(screen, COLORS_DICT['BROWN'], (centerCoords[0], centerCoords[1]), (centerCoords[0], centerCoords[1] - heightDiff), 6)
    if boolLfo.value == 0:
        pygame.draw.line(screen, COLORS_DICT['BROWN'], (centerCoords[0] - 5, centerCoords[1] - heightDiff), (centerCoords[0], centerCoords[1] - heightDiff), 6)
    else:
        pygame.draw.line(screen, COLORS_DICT['BROWN'], (centerCoords[0] + 5, centerCoords[1] - heightDiff), (centerCoords[0], centerCoords[1] - heightDiff), 6)

def drawCrab(screen, etc, centerCoords, accessories=[]):
    if (Accessories.SHADOW in accessories):
        pygame.draw.ellipse(screen, COLORS_DICT['SAND_SHADOW'], (centerCoords[0] - 47, centerCoords[1], 100, 30))
    pygame.draw.ellipse(screen, COLORS_DICT['CRAB'], (centerCoords[0] - 40, centerCoords[1] - 20, 80, 40))

    targetGlassesCoord = (centerCoords[0] + int(smartRythmLFO.current), centerCoords[1] + 10 - 20 * etc.knob4)
    pygame.draw.line(screen, COLORS_DICT['CRAB_ALT'], (centerCoords[0] - 15, centerCoords[1]-10), (targetGlassesCoord[0] - 15, targetGlassesCoord[1] - 40), 7)
    pygame.draw.line(screen, COLORS_DICT['CRAB_ALT'], (centerCoords[0] + 15, centerCoords[1]-10), (targetGlassesCoord[0] + 15, targetGlassesCoord[1] - 40), 7)

    if (Accessories.PIERCING_L in accessories):
        pygame.draw.arc(screen, COLORS_DICT['SUN'], (centerCoords[0] - 30, centerCoords[1], 6, 6), 2.2, 0.5, 2)

    if (Accessories.GLASSES in accessories):
        drawGlasses(screen, etc, centerCoords, targetGlassesCoord)
    else:
        pygame.draw.line(screen, COLORS_DICT['BLACK'], (targetGlassesCoord[0] - 15, targetGlassesCoord[1] - 34), (targetGlassesCoord[0] - 15, targetGlassesCoord[1] - 40), 7)
        pygame.draw.line(screen, COLORS_DICT['BLACK'], (targetGlassesCoord[0] + 15, targetGlassesCoord[1] - 34), (targetGlassesCoord[0] + 15, targetGlassesCoord[1] - 40), 7)


    pygame.draw.arc(screen, COLORS_DICT['CRAB'], (centerCoords[0] - 55, centerCoords[1], 30, 20), 1, 3.6, 4)
    pygame.draw.arc(screen, COLORS_DICT['CRAB'], (centerCoords[0] - 50, centerCoords[1] + 6, 30, 20), 1, 3.6, 4)
    pygame.draw.arc(screen, COLORS_DICT['CRAB'], (centerCoords[0] - 45, centerCoords[1] + 12, 30, 20), 1, 3.6, 4)

    pygame.draw.arc(screen, COLORS_DICT['CRAB'], (centerCoords[0] + 25, centerCoords[1], 30, 20), -0.28, 2.4, 4)
    pygame.draw.arc(screen, COLORS_DICT['CRAB'], (centerCoords[0] + 20, centerCoords[1] + 6, 30, 20), -0.28, 2.4, 4)
    pygame.draw.arc(screen, COLORS_DICT['CRAB'], (centerCoords[0] + 15, centerCoords[1] + 12, 30, 20), -0.28, 2.4, 4)

    leftClawRect = pygame.Rect((centerCoords[0] - 60, centerCoords[1] - 40, 100, 100))
    leftClawSf = pygame.Surface(leftClawRect.size, pygame.SRCALPHA)
 
    angle = 70 - int(smartRythmLFO.current) * 4

    if (Accessories.HEADPHONES in accessories):
        pygame.draw.arc(screen, COLORS_DICT['BLACK'], (targetGlassesCoord[0] - 30, targetGlassesCoord[1] - 57, 62, 50), 0.3, 2.8, 6)
        pygame.draw.arc(screen, COLORS_DICT['BLACK'], (targetGlassesCoord[0] - 30, targetGlassesCoord[1] - 58, 62, 50), 0.3, 2.8, 7)
        pygame.draw.ellipse(screen, COLORS_DICT['BLACK'], (targetGlassesCoord[0] - 36, targetGlassesCoord[1] - 50, 19, 24))
        pygame.draw.ellipse(screen, COLORS_DICT['BLACK'], (targetGlassesCoord[0] + 19, targetGlassesCoord[1] - 50, 19, 24))

    if (Accessories.CAP in accessories):
        pygame.draw.arc(screen, COLORS_DICT['CAP'], (targetGlassesCoord[0] - 25, targetGlassesCoord[1] - 65, 50, 45), 0, math.pi, 7)
        pygame.draw.arc(screen, COLORS_DICT['CAP'], (targetGlassesCoord[0] - 23, targetGlassesCoord[1] - 65, 46, 41), 0, math.pi, 7)
        pygame.draw.line(screen, COLORS_DICT['CAP'], (targetGlassesCoord[0] - 25, targetGlassesCoord[1] - 43), (targetGlassesCoord[0] + 38, targetGlassesCoord[1] - 43), 4)
        pygame.draw.polygon(screen, COLORS_DICT['CAP'], [
            (targetGlassesCoord[0]-25, targetGlassesCoord[1] - 43),
            (targetGlassesCoord[0]-15, targetGlassesCoord[1] - 53),
            (targetGlassesCoord[0], targetGlassesCoord[1] - 65),
            (targetGlassesCoord[0] + 15, targetGlassesCoord[1] - 53),
            (targetGlassesCoord[0] + 25, targetGlassesCoord[1] - 43),
        ])

    if (Accessories.BEARD_SMALL in accessories):
        pygame.draw.polygon(screen, COLORS_DICT['BROWN'], [
            (centerCoords[0] - 4, centerCoords[1] + 5),
            (centerCoords[0], centerCoords[1] + 10),
            (centerCoords[0] + 4, centerCoords[1] + 5),
        ])

    if (Accessories.MOUTH in accessories and getAudioInRatio(etc) > 0.15 ):
        pygame.draw.ellipse(screen, COLORS_DICT['WHITE'], (centerCoords[0] - 10, centerCoords[1] - int(getAudioInRatio(etc) * 10), 20, int(getAudioInRatio(etc) * 20)))

    drawEllipseAngle(screen, COLORS_DICT['CRAB'], (centerCoords[0] - 60, centerCoords[1] - 20, 35, 17), 130, 4)
    if Accessories.GOURMETTE_L in accessories:
        pygame.draw.ellipse(screen, COLORS_DICT['SILVER'], (centerCoords[0] - 62, centerCoords[1] - 27, 25, 17), 4)
    drawEllipseAngle(screen, COLORS_DICT['CRAB'], (centerCoords[0] - 65 + int(smartRythmLFO.current), centerCoords[1] - 40, 35, 17), angle, 4)

    drawEllipseAngle(screen, COLORS_DICT['CRAB'], (centerCoords[0] + 30, centerCoords[1] - 20, 35, 17), 50, 4)
    if Accessories.GOURMETTE_R in accessories:
        pygame.draw.ellipse(screen, COLORS_DICT['SILVER'], (centerCoords[0] + 39, centerCoords[1] - 27, 25, 17), 4)
    drawEllipseAngle(screen, COLORS_DICT['CRAB'], (centerCoords[0] + 40 + int(smartRythmLFO.current), centerCoords[1] - 40, 35, 17), angle, 4)

    if Accessories.MOUSTACHE in accessories:
        pygame.draw.line(screen, COLORS_DICT['BROWN'], (centerCoords[0] - 2, centerCoords[1]-10), (centerCoords[0] - 10, centerCoords[1] - 5), 4)
        pygame.draw.line(screen, COLORS_DICT['BROWN'], (centerCoords[0] + 2, centerCoords[1]-10), (centerCoords[0] + 10, centerCoords[1] - 5), 4)

    if Accessories.GOLDEN_CHAIN in accessories:
        pygame.draw.arc(screen, COLORS_DICT['SUN'], (centerCoords[0] - 30, centerCoords[1] - 35, 60, 50), 2.8, 0.3, 4)
        pygame.draw.circle(screen, COLORS_DICT['SUN'], (int(centerCoords[0]), int(centerCoords[1] + 20)), 7)


def drawGlasses(screen, etc, centerCoords, targetCoords):
    pygame.draw.rect(screen, COLORS_DICT['BLACK'], (targetCoords[0] - 23, targetCoords[1] - 40, 20, 15))
    pygame.draw.rect(screen, COLORS_DICT['BLACK'], (targetCoords[0] + 8, targetCoords[1] - 40, 20, 15))
    pygame.draw.line(screen, COLORS_DICT['BLACK'], (targetCoords[0] - 20, targetCoords[1] - 35), (targetCoords[0] + 20, targetCoords[1] - 35), 5)


def drawEllipseAngle(surface, color, rect, angle, width=0):
    target_rect = pygame.Rect(rect)
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.ellipse(shape_surf, color, (0, 0, target_rect.width, target_rect.height))
    rotated_surf = pygame.transform.rotate(shape_surf, angle)
    surface.blit(rotated_surf, rotated_surf.get_rect(center = target_rect.center))


def dawClam(screen, etc, centerCoords, isOpen):
    pygame.draw.ellipse(screen, COLORS_DICT['SAND_SHADOW'], (centerCoords[0] - 16, centerCoords[1] + 4, 40, 30))
    if isOpen:
        pygame.draw.ellipse(screen, COLORS_DICT['SAND_SHADOW'], (centerCoords[0] - 14, centerCoords[1] - 20, 40, 45))
        pygame.draw.ellipse(screen, COLORS_DICT['CLAM_OPEN'], (centerCoords[0] - 20, centerCoords[1] - 17, 40, 25))
        pygame.draw.ellipse(screen, COLORS_DICT['CLAM'], (centerCoords[0] - 20, centerCoords[1], 40, 35))
        pygame.draw.line(screen, COLORS_DICT['CLAM'], (centerCoords[0] - 20, centerCoords[1] + 2), (centerCoords[0] + 20, centerCoords[1] + 2), 5)
        pygame.draw.ellipse(screen, COLORS_DICT['DIAMOND'], (centerCoords[0] - 10, centerCoords[1] + 5, 9, 9))
        pygame.draw.ellipse(screen, COLORS_DICT['CLAM_TONGUE'], (centerCoords[0] - 15, centerCoords[1] + 5, 33, 22))
    else:
        pygame.draw.polygon(screen, COLORS_DICT['CLAM'], [
            (centerCoords[0] - 25, centerCoords[1]),
            (centerCoords[0] + 25, centerCoords[1]),
            (centerCoords[0] + 20, centerCoords[1] + 5),
            (centerCoords[0] - 20, centerCoords[1] + 5),
        ])
        pygame.draw.ellipse(screen, COLORS_DICT['CLAM'], (centerCoords[0] - 20, centerCoords[1], 40, 35))


def drawFlipper(screen, etc, centerCoords, angle):
    target_rect = pygame.Rect((0, 0, 140, 40))
    surface = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.ellipse(surface, COLORS_DICT['DOLPHIN'], (10, 20, 100, 60))
    pygame.draw.polygon(surface, COLORS_DICT['DOLPHIN'], [
        (50, 22),
        (55, 9),
        (70, 22)
    ])
    pygame.draw.arc(surface, COLORS_DICT['DOLPHIN'], (42, 9, 30, 50), 0, 1.8, 5)
    pygame.draw.ellipse(surface, COLORS_DICT['DOLPHIN'], (100, 35, 10, 7))
    pygame.draw.line(surface, COLORS_DICT['BLACK'], (95, 34), (97, 36), 2)
    pygame.draw.polygon(surface, COLORS_DICT['DOLPHIN_DARK'], [
        (70, 30), (55, 37), (50, 30)
    ])
    rotated_surf = pygame.transform.rotate(surface, angle)
    screen.blit(rotated_surf, centerCoords)

