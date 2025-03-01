"""
Core functionalities for SignalWave.
"""

import numpy as np

class SignalWave:
    def __init__(self, frequencies, amplitudes, phases, damping):
        self.frequencies = np.array(frequencies)
        self.amplitudes = np.array(amplitudes)
        self.phases = np.array(phases)
        self.damping = np.array(damping)

    def generate_wave(self, t):
        """ Generate the signal wave at time t. """
        return np.sum(self.amplitudes * np.cos(self.frequencies * t + self.phases) * np.exp(-self.damping * t))

    def generate_waveform(self, t_array):
        """ Generate the waveform for an array of time values. """
        return np.array([self.generate_wave(t) for t in t_array])

    def get_parameters(self):
        """ Returns the parameters of the wave function. """
        return {
            'frequencies': self.frequencies,
            'amplitudes': self.amplitudes,
            'phases': self.phases,
            'damping': self.damping
        }
