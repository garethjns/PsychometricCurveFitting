import unittest

import matplotlib.pyplot as plt
import numpy as np

from fit_psyche.psychometric_curve import PsychometricCurve


class TestPsychometricCurve(unittest.TestCase):
    def setUp(self):
        self._sut = PsychometricCurve()
        self._x = np.linspace(start=12, stop=16, num=6)
        self._y = (self._x > self._x.mean()).astype(float)

    def test_invalid_model_raises_error(self):
        # Act/Assert
        self.assertRaises(ValueError, lambda: PsychometricCurve(model='invalid'))

    def test_wh_fit_with_simple_data(self):
        # Arrange
        self._sut.set_params(model='wh')

        # Act
        self._sut.fit(self._x, self._y)

        # Assert
        self.assertIsNotNone(self._sut.coefs_['mean'])
        self.assertIsNotNone(self._sut.coefs_['var'])
        self.assertIsNotNone(self._sut.coefs_['guess_rate'])
        self.assertIsNotNone(self._sut.coefs_['lapse_rate'])
        self.assertGreater(self._sut.score(self._x, self._y), 0.98)

    def test_wh_fit_with_noisy_data(self):
        # Arrange
        self._sut.set_params(model='wh')
        self._y[2] = self._y[2] + np.abs(np.random.rand() / 8)
        self._y[3] = self._y[3] - np.abs(np.random.rand() / 8)

        # Act
        self._sut.fit(self._x, self._y)

        # Assert
        self.assertIsNotNone(self._sut.coefs_['mean'])
        self.assertIsNotNone(self._sut.coefs_['var'])
        self.assertIsNotNone(self._sut.coefs_['guess_rate'])
        self.assertIsNotNone(self._sut.coefs_['lapse_rate'])
        self.assertGreater(self._sut.score(self._x, self._y), 0.90)

    def test_logit_fit_with_simple_data(self):
        # Arrange
        self._sut.set_params(model='logit')

        # Act
        self._sut.fit(self._x, self._y)

        # Assert
        self.assertIsNotNone(self._sut.coefs_['mean'])
        self.assertIsNotNone(self._sut.coefs_['var'])
        self.assertGreater(self._sut.score(self._x, self._y), 0.98)

    def test_logit_fit_with_noisy_data(self):
        # Arrange
        self._sut.set_params(model='logit')
        self._y[2] = self._y[2] + np.abs(np.random.rand() / 10)
        self._y[3] = self._y[3] - np.abs(np.random.rand() / 10)

        # Act
        self._sut.fit(self._x, self._y)

        # Assert
        self.assertIsNotNone(self._sut.coefs_['mean'])
        self.assertIsNotNone(self._sut.coefs_['var'])
        self.assertGreater(self._sut.score(self._x, self._y), 0.90)

    def test_plot_with_y(self):
        # Arrange
        self._y[2] = self._y[2] + np.abs(np.random.rand())
        self._y[3] = self._y[3] - np.abs(np.random.rand())
        self._sut.fit(self._x, self._y)

        # Act
        fig = self._sut.plot(self._x, self._y, show=False)

        # Assert
        self.assertIsInstance(fig, plt.Figure)
