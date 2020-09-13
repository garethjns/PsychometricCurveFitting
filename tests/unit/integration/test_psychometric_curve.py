import unittest

import numpy as np
from sklearn.model_selection import RandomizedSearchCV

from fit_psyche.psychometric_curve import PsychometricCurve


class TestPsychometricCurve(unittest.TestCase):

    def test_with_sk_cv_search(self):
        # Arrange
        x = np.linspace(start=12, stop=16, num=6)
        y = (x > x.mean()).astype(float)
        y[2] = y[2] + np.abs(np.random.rand() / 10)
        y[3] = y[3] - np.abs(np.random.rand() / 10)

        # Act
        grid = RandomizedSearchCV(PsychometricCurve(),
                                  n_jobs=1,
                                  param_distributions={'guess_rate_lims': [(0.01, 0.05), (0.02, 0.04), (0.01, 0.04)],
                                                       'lapse_rate_lims': [(0.01, 0.05), (0.02, 0.04), (0.01, 0.04)]})
        grid.fit(x, y)

        # Assert
        self.assertIsInstance(grid.best_estimator_.coefs_, dict)
        self.assertAlmostEqual(14, grid.best_estimator_.coefs_['mean'], -1)
