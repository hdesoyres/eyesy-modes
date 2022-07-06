#!/usr/bin/env python
import argparse
import imp
import math
import random
import threading
import wave
import time

import alsaaudio
import pygame

import sound

POSITIVE_STEP = +0.05
NEGATIVE_STEP = -0.05
KNOBS_MAPPINGS = {
    pygame.K_a: ('knob1', POSITIVE_STEP),
    pygame.K_q: ('knob1', NEGATIVE_STEP),
    pygame.K_z: ('knob2', POSITIVE_STEP),
    pygame.K_s: ('knob2', NEGATIVE_STEP),
    pygame.K_e: ('knob3', POSITIVE_STEP),
    pygame.K_d: ('knob3', NEGATIVE_STEP),
    pygame.K_r: ('knob4', POSITIVE_STEP),
    pygame.K_f: ('knob4', NEGATIVE_STEP),
    pygame.K_t: ('knob5', POSITIVE_STEP),
    pygame.K_g: ('knob5', NEGATIVE_STEP),
}


class ETCEmulator:
    # frequency is the number of images per second
    def __init__(self, mode_name, wav_filename=None, frequency=40):
        self.etc = FakeEtc()
        self.main_module = imp.load_source('main', 'Modes/Python/%s/main.py' % mode_name)
        self.delay = 1000.0 / frequency / 1000.0 # delay in miliseconds
        self.next_triger_time = time.time()

        # Init sound system (like original ETC)
        sound.init(self.etc)
        self.sound_patcher = ETCSoundPatcher(wav_filename)

        # Init PyGame Window
        self.window = PyGameWindow(self.etc)

    def start(self):
        # Start sound
        self.sound_patcher.start()

        # Setup Mode
        self.main_module.setup(self.window.screen, self.etc)

        # Run Mode in loop
        should_stop = False
        while not should_stop:
            now = time.time()
            should_stop = self.window.check_events()
            # check for sound
            sound.recv()

            if now > self.next_triger_time:
                # Draw mode to screen
                self.window.screen.fill(self.etc.bg_color)
                self.main_module.draw(self.window.screen, self.etc)
                pygame.display.update()
                self.next_triger_time = now + self.delay

        # Stop Sound
        self.sound_patcher.stop()

        # Stop pygame
        pygame.quit()


class FakeEtc(object):
    """
    Partial copy/paste of the original Etc module
    """
    def __init__(self):
        self.xres = 1280
        self.yres = 720

        # Buttons
        self.trig_button = False  # True = Always trig => audio is SIN
        self.knob1 = 0.5
        self.knob2 = 0.5
        self.knob3 = 0.5
        self.knob4 = 0.5
        self.knob5 = 0.5

        # audio
        self.audio_in = [0] * 100
        self.audio_peak = 0
        self.audio_trig = False
        self.audio_scale = 1.0
        self.audio_trig_enable = True

        # BG
        self.bg_color = (0, 0, 0)

    def color_picker( self, val ):
        # convert knob to 0-1
        c = float(val)

        # all the way down random bw
        rando = random.randrange(0, 2)
        color = (rando * 255, rando * 255, rando * 255)

        # random greys
        if c > .02 :
            rando = random.randrange(0,255)
            color = (rando, rando, rando)
        # grey 1
        if c > .04 :
            color = (50, 50, 50)
        # grey 2
        if c > .06 :
            color = (100, 100 ,100)
        # grey 3
        if c > .08 :
            color = (150, 150 ,150)
        # grey 4
        if c > .10 :
            color = (150, 150 ,150)

        # grey 5
        if c > .12 :
            color = (200, 200 ,200)
        # white
        if c > .14 :
            color = (250, 250 ,250)
        #colors
        if c > .16 :

            #r = float(control) / 1024 * 255
            #g = float((control * 2) % 1024) / 1024 * 255
            #b = float((control * 4) % 1024) / 1024 * 255

            r = math.sin(c * 2 * math.pi) * .5 + .5
            g = math.sin(c * 4 * math.pi) * .5 + .5
            b = math.sin(c * 8 * math.pi) * .5 + .5
            color = (r * 255,g * 255,b * 255)
        # full ranoms
        if c > .96 :
            color = (random.randrange(0,255), random.randrange(0,255), random.randrange(0,255))
        # primary randoms
        if c > .98 :
            r = random.randrange(0, 2) * 255
            g = random.randrange(0, 2) * 255
            b = random.randrange(0, 2) * 255
            color = (r,g,b)

        color2 = (color[0], color[1], color[2])
        return color2

    def color_picker_bg(self, val):
        c = float(val)
        r = (1 - (math.cos(c * 3 * math.pi) * .5 + .5)) * c
        g = (1 - (math.cos(c * 7 * math.pi) * .5 + .5)) * c
        b = (1 - (math.cos(c * 11 * math.pi) * .5 + .5)) * c

        color = (r * 255,g * 255,b * 255)

        self.bg_color = color
        return color


class PyGameWindow:
    def __init__(self, etc):
        self.etc = etc
        pygame.init()
        window = (etc.xres, etc.yres)
        self.screen = pygame.display.set_mode(window)
        pygame.display.flip()

    def check_events(self):
        """
        Updates etc variables according to pygame events

        :return: True if the user asked to quit. False otherwise
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_KP_ENTER, pygame.K_RETURN):
                    self.etc.trig_button = not self.etc.trig_button
                elif event.key in KNOBS_MAPPINGS:
                    (knob_name, step) = KNOBS_MAPPINGS[event.key]
                    self.set_knob_value(knob_name, step)
        return False

    def set_knob_value(self, knob_name, step):
        new_value = getattr(self.etc, knob_name) + step
        new_value = min(max(new_value, 0.0), 1.0)
        setattr(self.etc, knob_name, new_value)
        self.print_knobs()

    def print_knobs(self):
        print('knob1: %.2f, knob2: %.2f, knob3: %.2f, knob4: %.2f, knob5: %.2f' % (
            self.etc.knob1,
            self.etc.knob2,
            self.etc.knob3,
            self.etc.knob4,
            self.etc.knob5,
        ))


class WavReader:
    """
    Helps reading a .wav file
    """
    def __init__(self, filepath):
        self.wav_file = wave.open(filepath, 'rb')
        self.period_size = 2000
        self.frame_rate = self.wav_file.getframerate()
        self.pcm_out = alsaaudio.PCM(
            alsaaudio.PCM_PLAYBACK,
            channels=self.wav_channels,
            rate=self.frame_rate,
            format=self.format,
            periodsize=self.period_size,
            mode=alsaaudio.PCM_NORMAL
        )
        self.read_last_time = False
        self.last_frame = None
        self.running = False
        self.thread = None

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._read_to_pcm_out)
        self.thread.start()

    def stop(self):
        self.running = False

    def read(self):
        """
        Will read 1/2 times to avoid read blocked in while loop
        :return:
        """
        if self.read_last_time:
            self.read_last_time = False
            return 0, ""
        elif self.last_frame:
            self.read_last_time = True
            return len(self.last_frame), self.last_frame
        else:
            self.read_last_time = False
            return 0, ""

    @property
    def format(self):
        # 8bit is unsigned in wav files
        if self.wav_file.getsampwidth() == 1:
            return alsaaudio.PCM_FORMAT_U8
        # Otherwise we assume signed data, little endian
        elif self.wav_file.getsampwidth() == 2:
            return alsaaudio.PCM_FORMAT_S16_LE
        elif self.wav_file.getsampwidth() == 3:
            return alsaaudio.PCM_FORMAT_S24_3LE
        elif self.wav_file.getsampwidth() == 4:
            return alsaaudio.PCM_FORMAT_S32_LE
        else:
            raise ValueError('Unsupported format')

    @property
    def wav_channels(self):
        return self.wav_file.getnchannels()

    def _read_to_pcm_out(self):
        self.last_frame = self.wav_file.readframes(self.period_size)
        while self.running:
            self.pcm_out.write(self.last_frame)
            self.last_frame = self.wav_file.readframes(self.period_size)


class ETCSoundPatcher:
    """
    Usefull utils which start playing a .wav file and sends the output to PCM_PLAYBACK (audio output).
    It's also "monkey patching" the sound module to simulate an audio capture made by the ETC.
    :return:
    """
    def __init__(self, wav_filename):
        self.reader = WavReader(wav_filename) if wav_filename else None

    def start(self):
        if self.reader:
            sound.inp = self.reader
            sound.nb_channels = self.reader.wav_channels
            self.reader.start()

    def stop(self):
        if self.reader:
            self.reader.stop()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run an ETC emulator playing a mode and optionally a .wav file ')
    parser.add_argument('-m', '--mode', type=str, required=False, default='S - Riton I', help='Name of the mode (default: S - Riton I)')
    parser.add_argument('-w', '--wav', type=str, required=False, default='input/Oxmo Puccino - Balance la sauce.wav', help='Name of the mode (default: None)')
    args = parser.parse_args()

    emulator = ETCEmulator(args.mode, args.wav)
    emulator.start()
