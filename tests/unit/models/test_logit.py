import unittest

import numpy as np

from fit_psyche.models.logit import logit


class TestLogit(unittest.TestCase):
    def test_fit_func(self):
        # Arrange
        x = np.linspace(start=12, stop=16, num=6)

        # Act
        y = logit(x, mean=14, var=1)

        # Assert
        self.assertIsInstance(y, np.ndarray)
        self.assertEqual(len(x), len(y))
        for yp, yt in zip(y, [0.11920292, 0.23147522, 0.40131234, 0.59868766, 0.76852478, 0.88079708]):
            self.assertAlmostEqual(yp, yt)
