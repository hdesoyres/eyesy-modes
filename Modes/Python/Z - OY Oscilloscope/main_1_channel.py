import pygame


def setup(screen, etc):
    pass


def draw(screen, etc):
    # etc.audio_in # 100 audio values are stored as 16-bit
    # etc.xres

    line_color = etc.color_picker(etc.knob4)
    etc.color_picker_bg(etc.knob5)

    nb_samples = len(etc.audio_in)
    width = float(etc.xres / nb_samples)
    y_start = int(etc.yres / 2)

    for idx, sample in enumerate(etc.audio_in):
        height = y_start * float(sample / 32767.0)

        y_end = int(y_start + height)
        x_start = int(idx * width)
        x_end = x_start
        start_pos = (x_start, y_start)
        end_pos = (x_end, y_end)

        pygame.draw.line(screen, line_color, start_pos, end_pos, int(width))
