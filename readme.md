# Psychometric curve fitting

Two functions to fit psychometric curves:
* **fitPsycheCurveLogit** - uses **glmfit** to fit a binomial distribution with a logit link function. It's basically a cumulative gaussian. Returns mean (subject bias) and variance (discrimination threshold). See <http://matlaboratory.blogspot.co.uk/2015/04/introduction-to-psychometric-curves-and.html> for details and examples.
* **fitPsychCurveWH** - uses **fit** to fit a psychometric curve based on [Wichmann and Hill 2001](http://wexler.free.fr/library/files/wichmann%20(2001)%20the%20psychometric%20function.%20i.%20fitting,%20sampling,%20and%20goodness%20of%20fit.pdf). This curve includes two additional parameters, "guess" and "lapse", which control somewhat for subject fallibility, improving the estimate of the discrimination threshold. See <http://matlaboratory.blogspot.co.uk/2015/05/fitting-better-psychometric-curve.html> for details and examples.
