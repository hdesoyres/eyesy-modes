import time
from collections import namedtuple

import numpy as np
import pygame

import main, main_float, main_float_op


def run_local(main_module=main):
    pygame.init()
    window = (1280, 720)
    screen = pygame.display.set_mode(window)
    pygame.display.flip()

    etc = fake_etc()
    main_module.setup(screen, etc)

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        start_draw = time.time()
        main_module.draw(screen, etc)
        log_time("Draw", start_draw)

        pygame.display.update()

    pygame.quit()


def fake_etc():
    Etc = namedtuple('Etc', ['xres', 'yres', 'audio_in', 'audio_trig', 'knob1', 'knob2', 'knob3', 'knob4', 'knob5'])
    etc = Etc(
        xres=1280, yres=720,
        audio_trig=False,
        knob1=0.5, knob2=0.5, knob3=0.5, knob4=0.3, knob5=0.8,
        audio_in=((np.random.rand(5) -0.5) * 32767).astype('uint16')
    )
    return etc


def log_time(name, start):
    if int(time.time() * 1000) % 10 == 1:
        print('%s %s ms' % (name, int((time.time() - start) * 1000)))


if __name__ == '__main__':
    run_local(main_float_op)
