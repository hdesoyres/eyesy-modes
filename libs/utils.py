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
