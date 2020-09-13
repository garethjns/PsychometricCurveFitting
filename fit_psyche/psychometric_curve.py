from typing import Tuple, Union, Dict, Callable

import matplotlib.pyplot as plt
import numpy as np
from scipy import optimize
from sklearn.base import BaseEstimator, RegressorMixin

from fit_psyche.models.wh2001 import wh2001
from fit_psyche.models.logit import logit


class PsychometricCurve(BaseEstimator, RegressorMixin):
    model: str
    coefs_: Union[None, Dict[str, float]]

    mean_lims: Tuple[float, float]
    var_lims: Tuple[float, float]
    guess_rate_lims: Tuple[float, float]
    lapse_rate_lims: Tuple[float, float]

    _fit_func: Callable

    def __init__(self, model: str = 'wh', mean_lims=(0, 20), var_lims=(0.1, 5),
                 guess_rate_lims=(0.01, 0.05), lapse_rate_lims=(0.01, 0.05)) -> None:

        self.coefs_ = None

        self.set_params(model=model,
                        mean_lims=mean_lims,
                        var_lims=var_lims,
                        guess_rate_lims=guess_rate_lims,
                        lapse_rate_lims=lapse_rate_lims)

    def set_params(self, *args, **kwargs) -> "PsychometricCurve":
        super().set_params(*args, **kwargs)
        if self.model.lower() == 'wh':
            self._fit_func = wh2001
        else:
            self._fit_func = logit

        return self

    def fit(self, x: np.array, y: np.array) -> "PsychometricCurve":
        if self.model.lower() == 'wh':
            lims = [self.mean_lims, self.var_lims, self.guess_rate_lims, self.lapse_rate_lims]
            bounds = ([self.mean_lims[0], self.var_lims[0], self.guess_rate_lims[0], self.lapse_rate_lims[0]],
                      [self.mean_lims[1], self.var_lims[1], self.guess_rate_lims[1], self.lapse_rate_lims[1]])
        else:
            lims = [self.mean_lims, self.var_lims]
            bounds = ([self.mean_lims[0], self.var_lims[0]], [self.mean_lims[1], self.var_lims[1]])

        popt, pcov = optimize.curve_fit(f=self._fit_func, xdata=x, ydata=y,
                                        p0=[np.mean(lim) for lim in lims], bounds=bounds)

        self.coefs_ = {'mean': popt[0], 'var': popt[1]}
        if self.model.lower() == 'wh':
            self.coefs_.update({'guess_rate': popt[2], 'lapse_rate': popt[3]})

        return self

    def predict(self, x: np.array) -> np.ndarray:
        return self._fit_func(x, **self.coefs_)

    def plot(self, x: np.array, y: np.ndarray = None, show: bool = True) -> None:
        fig, ax = plt.subplots()

        ax.plot(x, self.predict(x), label='y_pred')

        if y is not None:
            ax.scatter(x, y, label='y')

        ax.legend()
        ax.set_xlabel('N events')
        ax.set_ylabel('Prop fast')
        ax.set_title(f"Model: {self.model}")
        fig.tight_layout()

        if show:
            fig.show()

        return fig


if __name__ == "__main__":
    x = np.linspace(start=8, stop=16, num=16)
    y = (x > x.mean()).astype(float)

    pc = PsychometricCurve(model='wh').fit(x, y)
    pc.plot(x, y)
