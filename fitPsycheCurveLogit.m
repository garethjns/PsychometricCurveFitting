%http://matlaboratory.blogspot.co.uk/2015/04/introduction-to-psychometric-curves-and.html

function [coeffs, curve, threshold] = ...
    FitPsycheCurveLogit(xAxis, yData, weights, targets)

% Transpose if necessary
if size(xAxis,1)<size(xAxis,2)
    xAxis=xAxis';
end
if size(yData,1)<size(yData,2)
    yData=yData';
end
if size(weights,1)<size(weights,2)
    weights=weights';
end

% Check range of data
if min(yData)<0 || max(yData)>1  
     % Attempt to normalise data to range 0 to 1
    yData = yData/(mean([min(yData), max(yData)])*2);
end

% Perform fit
coeffs = glmfit(xAxis, [yData, weights], 'binomial','link','logit');

% Create a new xAxis with higher resolution
fineX = linspace(min(xAxis),max(xAxis),numel(xAxis)*50);
% Generate curve from fit
curve = glmval(coeffs, fineX, 'logit');
curve = [fineX', curve];

% If targets (y) supplied, find threshold (x)
if nargin==4
else
    targets = [0.25, 0.5, 0.75];
end
threshold = (log(targets./(1-targets))-coeffs(1))/coeffs(2);