import audioop
import time
from functools import partial

import alsaaudio
import numpy as np
import pygame
import pygame.gfxdraw

import sound

max_stereo_buffer_size = 15000


def get_avg_sample(data, i):
    avg = audioop.getsample(data, 2, i * 3)
    avg += audioop.getsample(data, 2, (i * 3) + 1)
    avg += audioop.getsample(data, 2, (i * 3) + 2)
    avg = avg / 3
    return avg


def stereo_recv(etc):
    start = time.time()

    # get audio
    l, data = sound.inp.read()  # 48Khz fails here!
    peak = 0
    while l:
        try:
            # Extract channels
            mono_data = audioop.tomono(data, 2, 1, 1)
            if sound.nb_channels >= 2:
                left_data = audioop.tomono(data, 2, 1, 0)
                right_data = audioop.tomono(data, 2, 0, 1)
            else:
                left_data = []
                right_data = []
        except Exception as exc:
            log_time('READING FAILED %s' % exc, time.time())
            time.sleep(0.010)
            return

        nb_stereo_samples = len(left_data) // sound.nb_channels
        for i in range(nb_stereo_samples):
            etc.audio_lin.append(audioop.getsample(left_data, 2, i))
            etc.audio_rin.append(audioop.getsample(right_data, 2, i))

        nb_mono_samples = len(mono_data) // sound.nb_channels // 3  # AVG sample takes 3 sample
        for i in range(nb_mono_samples):
            try:
                # "Original" code
                avg = get_avg_sample(mono_data, i)

                # scale it
                avg = int(avg * etc.audio_scale)
                if avg > 20000:
                    sound.trig_this_time = time.time()
                    if (sound.trig_this_time - sound.trig_last_time) > .05:
                        if etc.audio_trig_enable:
                            etc.audio_trig = True
                        sound.trig_last_time = sound.trig_this_time
                if avg > peak:
                    etc.audio_peak = avg
                    peak = avg
                # if the trigger button is held
                if etc.trig_button:
                    etc.audio_in[i] = sound.sin[i]
                else:
                    etc.audio_in[i] = avg
            except:
                pass
        l, data = sound.inp.read()

    if len(etc.audio_lin) > max_stereo_buffer_size:
        etc.audio_lin = etc.audio_lin[-max_stereo_buffer_size:]
    if len(etc.audio_rin) > max_stereo_buffer_size:
        etc.audio_rin = etc.audio_rin[-max_stereo_buffer_size:]
    log_time('stereo_recv', start)


def patch_sound_inp_recv(etc):
    # Set 2 new variable : left/right audio in
    etc.audio_lin = []
    etc.audio_rin = []

    # Close Mono PCM
    sound.inp = None

    # Open Stero PCM
    sound.inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK)
    sound.inp.setchannels(2)  # Original: 1
    sound.inp.setrate(44100)  # Original: 11025
    sound.inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
    sound.inp.setperiodsize(512)  # Original: 300
    sound.nb_channels = 2  # Original: 1

    # Patch sound.recv to handle stereo
    sound.recv = partial(stereo_recv, etc)


def setup(screen, etc):
    patch_sound_inp_recv(etc)


def draw(screen, etc):
    draw_start = time.time()
    etc.color_picker_bg(etc.knob5)

    gain = 2 * etc.knob1

    radius = max(1, int(etc.knob2 * 20))
    color = etc.color_picker(etc.knob4)

    nb_samples = len(etc.audio_rin)
    max_points = 10000 # min(750, nb_samples)  # 7500 is good, but pygame perf are really bad !

    # pygame drawer
    left_data = np.array(etc.audio_lin[-max_points:])
    right_data = np.array(etc.audio_rin[-max_points:])
    xs = (etc.xres * (0.5 + left_data * gain / 32767.0 / 2)).astype(np.int16)
    ys = (etc.yres * (0.5 + right_data * gain / 32767.0 / 2)).astype(np.int16)
    positions = np.c_[xs, ys]
    for idx, position in enumerate(positions):
        pygame.draw.circle(screen, color, position, radius)
        # screen.set_at((x, y), color)

    """ Blit took too long !!
    # NP Drawer
    left_data = np.array(etc.audio_lin[-max_points:])
    right_data = np.array(etc.audio_rin[-max_points:])
    pixels = np.zeros((etc.xres, etc.yres, 3), dtype=np.int16)
    xs = (etc.xres * (0.5 + left_data * gain / 32767.0 / 2)).astype(np.int16)
    ys = (etc.yres * (0.5 + right_data * gain / 32767.0 / 2)).astype(np.int16)
    pixels[xs, ys, :] = color
    start_blit = time.time()
    pygame.surfarray.blit_array(screen, pixels)
    log_time('blit_array', start_blit)
    """
    log_time('draw', draw_start)


def _get_value(gain, res, channel, idx):
    return int(res * (0.5 + gain * channel[idx] / 32767.0 / 2))


def log_time(name, start):
    if int(time.time() * 1000) % 10 == 1:
        print('%s %s ms' % (name, int((time.time() - start) * 1000)))

