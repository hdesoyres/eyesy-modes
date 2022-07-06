EYESY - Oscilloscope 3D
==
EYESY Mode which tries to simulate an Oscillospe XY.
This mode is intended to be used with Oscillospe Music.

# Display & Numbers
~Lines~ are not a good solutions
**Points** (with width)

- Screen is 1024x768 => 786432 pixels
- Max sampling rate : 48kHZ
- Desired framerate: 50Hz => Max processing time : 20ms
- 1000-1200 points should match sampling/frame rate (Visual Requirements : 10k-30k points)

# Know issues

## Performances
Many

## [Solved] No 2 audio input
TODO EXPLAIN monkey_patch

## Max sampling rate
Current: 11khZ
Need : 48kHZ (max card)

When augmenting :
alsaaudio.ALSAAudioError: Capture data too large. Try decreasing period size

### How to

**SSH**
```
ssh music@192.168.1.33
```

**List audio devices**
```
music@eyesy:~ $ arecord --list-devices
**** List of CAPTURE Hardware Devices ****
card 0: audioinjectorpi [audioinjector-pi-soundcard], device 0: AudioInjector audio wm8731-hifi-0 []
  Subdevices: 0/1
  Subdevice #0: subdevice #0
```
This says that the audio card is on card 0, device 0.

**Check max sample rate**
```
music@eyesy:~ $ arecord -f S16_LE -r 60000 -D hw:0,0 -d 5 -c 2 /tmp/test.wav
Recording WAVE '/tmp/test.wav' : Signed 16 bit Little Endian, Rate 60000 Hz, Stereo
Warning: rate is not accurate (requested = 60000Hz, got = 48000Hz)
         please, try the plug plugin 
```
This says max recording sample rate is 48khz.

## Point transparency
Will it be better ?

