function [coeffs, curve, threshold] = ...
    fitPsycheCurveLogit(xAxis, yData, varargin)

weights = ones(numel(xAxis),1);
targets = [0.25, 0.5, 0.75];
 
if numel(varargin)>=1
    % Assume weights
    weights = varargin{1};
end
if numel(varargin)==2
    % Assume weights and targets
    targets = varargin{2};
end

% Transpose if necessary
if size(xAxis,1)<size(xAxis,2)
    xAxis = xAxis';
end
if size(yData,1)<size(yData,2)
    yData = yData';
end

if size(weights,1)<size(weights,2)
    weights = weights';
end

% Check range of data
if min(yData)<0 || max(yData)>1  
     % Nrmalise data to range 0 to 1
    yData = (yData-min(yData)) / (max(yData)-min(yData));
end

% Perform fit
coeffs = glmfit(xAxis, [yData, weights], 'binomial','link','logit');

% Create a new xAxis with higher resolution
fineX = linspace(min(xAxis),max(xAxis),numel(xAxis)*50);
% Generate curve from fit
curve = glmval(coeffs, fineX, 'logit');
curve = [fineX', curve];

% If targets (y) supplied, find threshold (x)
threshold = (log(targets./(1-targets))-coeffs(1))/coeffs(2);
