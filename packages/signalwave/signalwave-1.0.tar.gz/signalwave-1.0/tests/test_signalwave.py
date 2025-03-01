"""
Unit tests for SignalWave library.
"""

import unittest
import numpy as np
from signalwave.core import SignalWave

class TestSignalWave(unittest.TestCase):
    def test_wave_generation(self):
        wave = SignalWave([1, 2], [1, 0.5], [0, np.pi/2], [0, 0])
        result = wave.generate_wave(0)
        self.assertAlmostEqual(result, 1.5, places=2)

if __name__ == '__main__':
    unittest.main()
