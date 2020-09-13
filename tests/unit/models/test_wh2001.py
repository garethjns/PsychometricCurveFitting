import unittest

import numpy as np

from fit_psyche.models.wh2001 import wh2001


class TestWH2001(unittest.TestCase):
    def test_fit_func(self):
        # Arrange
        x = np.linspace(start=12, stop=16, num=6)

        # Act
        y = wh2001(x, guess_rate=0.01, lapse_rate=0.01, mean=14, var=1)

        # Assert
        self.assertIsInstance(y, np.ndarray)
        self.assertEqual(len(x), len(y))
        for yp, yt in zip(y, [0.03229513, 0.12276828, 0.34768669, 0.65231331, 0.87723172, 0.96770487]):
            self.assertAlmostEqual(yp, yt)
