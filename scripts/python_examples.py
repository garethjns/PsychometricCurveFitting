import numpy as np

from fit_psyche.psychometric_curve import PsychometricCurve
import pprint

if __name__ == "__main__":
    x = np.linspace(start=12, stop=16, num=6)
    y = (x > x.mean()).astype(float)
    y[2] = y[2] + np.abs(np.random.rand())
    y[3] = y[3] - np.abs(np.random.rand())

    pc = PsychometricCurve(model='logit').fit(x, y)
    pc.plot(x, y)
    print(pc.score(x, y))
    pprint.pprint(pc.coefs_)

    pc = PsychometricCurve(model='wh').fit(x, y)
    pc.plot(x, y)
    print(pc.score(x, y))
    pprint.pprint(pc.coefs_)
