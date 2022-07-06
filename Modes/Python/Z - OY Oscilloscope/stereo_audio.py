import alsaaudio
import audioop
import time
import math


class StereoAudioCapture:

    def __init__(self):
        self.inp = None
        self.etc = None
        self.trig_this_time = 0
        self.trig_last_time = 0
        self.sin = [0] * 100

        self.audio_in = [0] * 100

    def init(self, etc_object) :
        self.etc = etc_object
        #setup alsa for sound in
        self.inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK)
        self.inp.setchannels(2)
        self.inp.setrate(11025)
        self.inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        self.inp.setperiodsize(300)
        self.trig_last_time = time.time()
        self.trig_this_time = time.time()

        for i in range(0,100) :
            self.sin[i] = int(math.sin(2 * 3.1459 * i / 100) * 32700)

    def recv(self) :
        # get audio
        l,data = self.inp.read()
        peak = 0
        while l:
            for i in range(0,100) :
                try :
                    avg = audioop.getsample(data, 2, i * 3)
                    avg += audioop.getsample(data, 2, (i * 3) + 1)
                    avg += audioop.getsample(data, 2, (i * 3) + 2)
                    avg = avg / 3
                    # scale it
                    avg = int(avg * self.etc.audio_scale)
                    if (avg > 20000) :
                        self.trig_this_time = time.time()
                        if (self.trig_this_time - self.trig_last_time) > .05:
                            if self.etc.audio_trig_enable: self.etc.audio_trig = True
                            self.trig_last_time = self.trig_this_time
                    if avg > peak :
                        self.etc.audio_peak = avg
                        peak = avg
                    # if the trigger button is held
                    if (self.etc.trig_button) :
                        self.audio_in[i] = self.sin[i]
                    else :
                        self.audio_in[i] = avg

                except :
                    pass
            l,data = self.inp.read()
