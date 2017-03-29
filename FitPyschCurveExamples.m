% Fitpsychcurve examples


%% Make up some data

% y1 = (1:10:100)/100;
y1 = [0 0 25 25 50 50 75 75 100 100]/100;
% y2 = [0 5/2 10/2 20/2 40/2 60+40/2 80+20/2 90+10/2 95+5/2 100]/100;
% y2 = [x=(0.5:10)/10;
% y2 = [0 5 10 20 40 60 80 90 95 100]/100;

% y2 = [5 5 10 20 40 60 80 90 95 95];
% y2 = y(2+rand(1,numel(y2))*5)/100;

y2 = [20 20 20 30 40 60 70 80 80 80];
y2 = (y2+rand(1,numel(y2))*5)/100;

% Create x axis
x = 0.1:0.1:1;


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


%% Fit WH2001 - access methods directly

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


%% Fit GLM - create object

ffit1 = fitPsyche(x, y1, 'GLM');
ffit2 = fitPsyche(x, y2, 'GLM');

figure
plotPsyche(ffit1)
hold on
plotPsyche(ffit2)
legend({'y1', 'y2', 'y1 fit', 'y2 fit'}, 'Location', 'NorthWest')
title('GLM fit')


%% Fit WH2001 - create object

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
