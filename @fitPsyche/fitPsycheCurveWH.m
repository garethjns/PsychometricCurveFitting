function [ffit, curve] = ...
    fitPsycheCurveWH(xAxis, yData, varargin)

% Start points and limits
useLims = 0;
if ~isempty(varargin)
    useLims = 1;
    UL = varargin{1}(1,:);
    SP = varargin{1}(2,:);
    LL = varargin{1}(3,:);
end

% Transpose if necessary
if size(xAxis,1)<size(xAxis,2)
    xAxis = xAxis';
end
if size(yData,1)<size(yData,2)
    yData = yData';
end

% Check range of data
if min(yData)<0 || max(yData)>1  
     % Normalise data to range 0 to 1
     yData = (yData-min(yData)) / (max(yData)-min(yData));
end
    
% Prepare fitting function
F = @(g,l,u,v,x) g+(1-g-l)*0.5*(1+erf((x-u)/sqrt(2*v^2)));

% Fit using fit function from fit toolbox
if useLims==1
    % SPs and limits specified, use while fitting
    ffit = ...
        fit(xAxis, yData, F, 'StartPoint', SP, 'Upper', UL, 'Lower', LL);
else
    % Lims not specified, don't use while fitting
    ffit = fit(xAxis, yData, F);
end

% Create a new xAxis with higher resolution
fineX = linspace(min(xAxis),max(xAxis),numel(xAxis)*50);
% Generate curve from fit
curve = feval(ffit, fineX);
curve = [fineX', curve];
