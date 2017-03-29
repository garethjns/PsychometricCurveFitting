# Psychometric curve fitting

Two functions to fit psychometric curves:

**fitPsycheCurveLogit** - uses glmfit to fit a binomial distribution with a logit link function.  
**fitPsychCurveWH** - uses fit to fit a psychometric curve based on [Wichmann and Hill 2001](http://wexler.free.fr/library/files/wichmann%20(2001)%20the%20psychometric%20function.%20i.%20fitting,%20sampling,%20and%20goodness%20of%20fit.pdf). This curve includes two additional parameters, "guess" and "lapse", which control somewhat for subject fallibility, improving the estimate of the discrimination threshold.

 
# Usage
Fitting functions can be acessed by creating a PsychFit object, or directly. See also [FitPsycheCurveExamples.m](https://github.com/garethjns/PsychometricCurveFitting/blob/master/FitPyschCurveExamples.m).

```MATLAB
% Make up some data
y1 = [0 0 25 25 50 50 75 75 100 100]/100;
y2 = [20 20 20 30 40 60 70 80 80 80];
y2 = (y2+rand(1,numel(y2))*5)/100;
% Create x axis
x = 0.1:0.1:1;
```

## PsychFit object
### GLM
```MATLAB
ffit1 = fitPsyche(x, y1, 'GLM');
ffit2 = fitPsyche(x, y2, 'GLM');

figure
plotPsyche(ffit1)
hold on
plotPsyche(ffit2)
legend({'y1', 'y2', 'y1 fit', 'y2 fit'}, 'Location', 'NorthWest')
title('GLM fit')
```
![Alt text](Images/GLMObj.png?raw=true "Title")

### WH2001
```MATLAB
ffit1 = fitPsyche(x, y1, 'WH');
ffit2 = fitPsyche(x, y2, 'WH');

figure
plotPsyche(ffit1)
hold on
plotPsyche(ffit2)
legend({'y1', 'y2', 'y1 fit', 'y2 fit'}, 'Location', 'NorthWest')
title('WH 2001 fit')

disp(ffit1.model)
disp(ffit2.model)
```
![Alt text](Images/WHObj.png?raw=true "Title")

### WH2001 with limited coefficients
```MATLAB
%% Set limits for WH fit

% g (guess rate), l (lapse), u (mean, bias), v (varience, discrimination
% thresh)
% UpperLimits:
UL = [0.05, 0.05, 1, 1]; % Limit upper bound of g and l to 5%
% StartPoints:
SP = [0, 0, 0.5, 0.5];
% LowerLimits:
LL = [0.05, 0.05, 0, 0];

ffit1 = fitPsyche(x, y2, 'WH', [UL;SP;LL]);
ffit2 = fitPsyche(x, y2, 'WH');
figure
plotPsyche(ffit1)
hold on
plotPsyche(ffit2)
legend({'y2', 'y2 limited fit', 'y2', 'y2 fit'}, 'Location', 'NorthWest')
title('WH 2001 fit')

disp(ffit1.model)
disp(ffit2.model)
```
![Alt text](Images/WHObjLim.png?raw=true "Title")

## Direct method access
### GLM
```MATLAB
%% Fit GLM - access methods directly

[coeffs1, curve1, ~] = ...
    fitPsyche.fitPsycheCurveLogit(x, y1);
[coeffs2, curve2, ~] = ...
    fitPsyche.fitPsycheCurveLogit(x, y2);

% Plot
figure
scatter(x', y1')
hold on
scatter(x', y2')
plot(curve1(:,1),curve1(:,2))
plot(curve2(:,1),curve2(:,2))
legend({'y1', 'y2', 'y1 fit', 'y2 fit'}, 'Location', 'NorthWest')
title('GLM fit')
```
![Alt text](Images/GLMFit.png?raw=true "Title")

### WH2001
```MATLAB
[ffit1, curve1] = ...
    fitPsyche.fitPsycheCurveWH(x, y1);
[ffit2, curve2] = ...
    fitPsyche.fitPsycheCurveWH(x, y2);

% Plot
figure
scatter(x', y1')
hold on
scatter(x', y2')
plot(ffit1)
plot(ffit2)
legend({'y1', 'y2', 'y1 fit', 'y2 fit'}, 'Location', 'NorthWest')
title('WH2001 fit')
```
![Alt text](Images/WHDirect.png?raw=true "Title")
