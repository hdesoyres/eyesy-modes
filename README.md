EYESY Emulator
==

# Dev Guidelines
## Installation
I recommend using a dedicated python 2.7 virtualenv
```
# Create a python 2.7 virtualenv in the ~/.venv/eyesy directory 
virtualenv --python python27 ~/.venv/eyesy

# Activate the virtualenv
source ~/.venv/eyesy/bin/activate

# Optional : upgrade pip
python -m pip install --upgrade pip
```

Then all you need is to install dependencies
```
pip install -r requirements.txt
```

## Usage
```
usage: emulator.py [-h] [-m MODE] [-w WAV]

Run an ETC emulator playing a mode and optionally a .wav file

optional arguments:
-h, --help            show this help message and exit
-m MODE, --mode MODE  Name of the mode (default: S - Riton I)
-w WAV, --wav WAV     Name of the mode (default: None)
```

## Simulating knobs/button inputs
The emulator knobs' values can update updated when the window is active using keyboards :
- a: Increase knob1
- q: Decrease knob1
- z: Increase knob2
- s: Decrease knob2
- e: Increase knob3
- d: Decrease knob3
- r: Increase knob4
- f: Decrease knob4
- t: Increase knob5
- g: Decrease knob5

Trigger button is emulated with the "ENTER"/"RETURN" key.
