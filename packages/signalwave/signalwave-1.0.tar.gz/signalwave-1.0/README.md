# SignalWave

SignalWave is a Python library for creating and analyzing signal wave functions.

## Installation

```sh
pip install signalwave
```

## Usage

```python
from signalwave import SignalWave
import numpy as np

wave = SignalWave([1, 2], [1, 0.5], [0, 0], [0, 0])
t = np.linspace(0, 10, 1000)
waveform = wave.generate_waveform(t)
```

## Features

- Generate signal waveforms using multiple oscillators.
- Analyze wave characteristics.
- Perform Fourier analysis on generated signals.
- Create modulated signals.

## Examples

1. **Basic Usage**: Learn how to generate and visualize a signal wave. [`example_basic.py`](examples/example_basic.py)
2. **Fourier Analysis**: Apply Fourier Transform to analyze the frequency content of a signal wave. [`example_fourier.py`](examples/example_fourier.py)
3. **Modulation**: Create an amplitude-modulated signal using a low-frequency wave. [`example_modulation.py`](examples/example_modulation.py)

