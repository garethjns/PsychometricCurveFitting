from dataclasses import dataclass, field
from typing import Tuple, Union, Dict, Callable, Optional

import matplotlib.pyplot as plt
import numpy as np
from scipy import optimize
from sklearn.base import BaseEstimator, RegressorMixin

from fit_psyche.models.logit import logit
from fit_psyche.models.wh2001 import wh2001


@dataclass
class PsychometricCurve(BaseEstimator, RegressorMixin):
    model: str = "logit"
    mean_lims: Tuple[float, float] = (0, 20)
    var_lims: Tuple[float, float] = (0.001, 20)
    guess_rate_lims: Tuple[float, float] = (0.01, 0.05)
    lapse_rate_lims: Tuple[float, float] = (0.01, 0.05)

    _fit_func: Optional[Callable] = field(default=None, init=False)
    coefs_: Optional[Union[None, Dict[str, float]]] = field(default=None, init=False)

    """
   Fit a Logit or Wichmann and Hill 2001 psychometric curve.

   Model parameters:
     - Both:
       - mean (bias): The mean point of the experimental variable where the decision flips (on average).
                      Describes decision bias.
       - var / discrimination threshold: The distribution variance. Lower means the decision flips quicker, so is
                                         "better". Both models are cumulative normal distributions. Greater
                                         variance = wider distribution = more change in x before decision flips.
     - wh only
       - Guess and lapse rates: Model subject fallibility. Essentially allow either end of the fit cumulative
                                distribution to anchor to points other than 0 and 1 at each end of the curve
                                (respectively). See Wichmann and Hill, 2001.

   For all parameters, starting points are set as a mean of the specified limits.

   :param model: Which model to use, 'logit' or 'wh'. Logit model has two parameters, mean and variance. WH
                 adds guess and lapse rate. Default 'logit'.
   :param mean_lims: Limit for the mean parameter. Should be set according to range of independent (x) variable.
                     For example, if the x variable is set between 10 and 20 units in the experiment, limits within
                     that range are reasonable. If it's outside something weird is going on!. Specified as
                     tuple(min, max). Default (0, 20).
   :param var_lims: Limit for the var parameter. Lower limit should be >0 and upper limit should be set according
                    to task difficulty. Specified as tuple(min, max). Default (0.001, 100).
   :param guess_rate_lims: Limit for the guess parameter. Sets anchor point for start of curve and represents
                           proportion of trails where subject acts randomly. Limits should be set according the
                           expectations about subject.
                           For example, it should be higher for humans than a machine learning model... Unless,
                           it's a machine learning model with stochastic elements like a NN with dropout or
                           reinforcement learning model that uses Epsilon greedy.
                           Suggestions:
                             - Human (0.01, 0.05) ie. 1-5%
                             - Deterministic ML model (0, 1e-6) - the 'logit' model may be more appropriate.
                             - Stochastic ML model: Around known epsilon greedy value, or some low value in other
                               cases.
                           Specified as tuple(min, max). Default (0.01, 0.05).
   :param lapse_rate_lims: Sets the anchor point for the upper end of the curve. See guess_rate_lims.
   """

    def __post_init__(self):
        if self.model not in ['logit', 'wh']:
            raise ValueError(f"Unknown model: {self.model}. Available models: 'logit', 'wh'")

    def fit(self, x: np.ndarray, y: np.ndarray) -> "PsychometricCurve":
        if self.model.lower() == "wh":
            self._fit_func = wh2001
            lims = [
                self.mean_lims,
                self.var_lims,
                self.guess_rate_lims,
                self.lapse_rate_lims,
            ]

            bounds = (
                [
                    self.mean_lims[0],
                    self.var_lims[0],
                    self.guess_rate_lims[0],
                    self.lapse_rate_lims[0],
                ],
                [
                    self.mean_lims[1],
                    self.var_lims[1],
                    self.guess_rate_lims[1],
                    self.lapse_rate_lims[1],
                ],
            )
        else:
            self._fit_func = logit
            lims = [self.mean_lims, self.var_lims]
            bounds = (
                [self.mean_lims[0], self.var_lims[0]],
                [self.mean_lims[1], self.var_lims[1]],
            )

        popt, pcov = optimize.curve_fit(
            f=self._fit_func,
            xdata=x,
            ydata=y,
            p0=[np.mean(lim) for lim in lims],
            bounds=bounds,
        )

        self.coefs_ = {"mean": popt[0], "var": popt[1]}
        if self.model.lower() == "wh":
            self.coefs_.update({"guess_rate": popt[2], "lapse_rate": popt[3]})

        return self

    def predict(self, x: np.array) -> np.ndarray:
        return self._fit_func(x, **self.coefs_)

    def plot(
            self,
            x: np.ndarray,
            y: np.ndarray = None,
            show: bool = True,
            y_label: str = "Prop.",
            x_label: str = "Independent variable",
    ) -> None:
        fig, ax = plt.subplots()

        ax.plot(x, self.predict(x), label="y_pred")

        if y is not None:
            ax.scatter(x, y, label="y")

        ax.legend()
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_title(f"Model: {self.model}")
        fig.tight_layout()

        if show:
            fig.show()

        return fig


if __name__ == "__main__":
    x_ = np.linspace(start=8, stop=16, num=16)
    y_ = (x_ > x_.mean()).astype(float)

    pc = PsychometricCurve(model="wh", guess_rate_lims=(0, 0.2)).fit(x_, y_)
    pc.plot(x_, y_)
