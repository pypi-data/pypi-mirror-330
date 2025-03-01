"""
Utilities for signal wave analysis.
"""

import numpy as np

def analyze_waveform(waveform):
    """ Analyze the waveform and return basic statistics. """
    return {
        'mean': np.mean(waveform),
        'std_dev': np.std(waveform),
        'max': np.max(waveform),
        'min': np.min(waveform)
    }
