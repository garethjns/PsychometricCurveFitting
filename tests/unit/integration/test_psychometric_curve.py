import unittest

import numpy as np
from sklearn.model_selection import RandomizedSearchCV

from fit_psyche.psychometric_curve import PsychometricCurve


class TestPsychometricCurve(unittest.TestCase):

    def setUp(self):
        self._sut = PsychometricCurve()
        self._grid = {'model': ['wh', 'logit'],
                      'guess_rate_lims': [(0.01, 0.05), (0.01, 0.03), (0.03, 0.04)],
                      'lapse_rate_lims': [(0.01, 0.05), (0.01, 0.03), (0.03, 0.04)]}
        x = np.linspace(start=12, stop=16, num=12)
        y = (x > x.mean()).astype(float)
        y[2] = y[2] + np.abs(np.random.rand() / 10)
        y[3] = y[3] - np.abs(np.random.rand() / 10)
        self._x = x
        self._y = y

    def test_with_sk_cv_search_single_job(self):
        # Act
        grid = RandomizedSearchCV(self._sut,
                                  n_jobs=1,
                                  param_distributions=self._grid)
        grid.fit(self._x, self._y)

        # Assert
        self.assertIsInstance(grid.best_estimator_.coefs_, dict)
        self.assertAlmostEqual(14, grid.best_estimator_.coefs_['mean'], -1)

    def test_with_sk_cv_search_multi_jobs(self):
        # Act
        grid = RandomizedSearchCV(self._sut,
                                  n_jobs=3,
                                  param_distributions=self._grid)
        grid.fit(self._x, self._y)

        # Assert
        self.assertIsInstance(grid.best_estimator_.coefs_, dict)
        self.assertAlmostEqual(14, grid.best_estimator_.coefs_['mean'], -1)
