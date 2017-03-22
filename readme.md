# Psychometric curve fitting

Two functions to fit psychometric curves:

fitPsycheCurveLogit - uses glmfit to fit a binomial distribution with a logit link function. 
fitPsychCurveWH - uses fit to fit a psychometric curve based on Wichmann and Hill 2001. This curve includes two additional parameters, "guess" and "lapse", which control somewhat for subject fallibility, improving the estimate of the discrimination threshold.

For now, see [FitPsycheCurveExamples.m](https://github.com/garethjns/PsychometricCurveFitting/blob/master/FitPyschCurveExamples.m) for usage examples

