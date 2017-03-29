classdef fitPsyche
    % Psychometric curve fitting using logit glm (.fitPsycheCurveLogit) or
    % Wichmann and Hill 2001 (.fitPsycheCurveWH)
    %
    % fitPsyche object can be of type 'WH2001' or 'GLM'
    % - See examples
    % 
    % Fitting fuctions can also be accessed directly:
    % .fitPsycheCurveLogit
    % [coeffs, curve, threshold] = ...
    %       fitPsyche.fitPsycheCurveLogit(xAxis, yData, weights, targets)
    % Returns coeff values, and optional curve and thresholds for supplied
    % targets.
    %
    % .fitPsycheCurveWH
    % [ffit, curve] = ...
    %        fitPsycheCurveWH(xAxis, yData, varargin)
    % Where varargin contains optional values and limits for coefficients.
    % ie.
    %     UL = varargin{1}(1,:); % Upper limits for [g,l,u,v]
    %     SP = varargin{1}(2,:); % Start points for [g,l,u,v]
    %     LM = varargin{1}(3,:); % Lower limits for [g,l,u,v]
    % Where g = guess rate, l = lapse rate, u = mean, v = var.
    % For function y = g+(1-g-l)*0.5*(1+erf((x-u)/sqrt(2*v^2)));
    % Retuns fit object (which has its own plot method).
    %
    % 
    
    properties
        type = 'WH2001';
        model % Fit model (WH only)
        coeffs % Coeffs (GLM only)
        curve % High res fitted curve
        x % x axis
        y % Fit data
    end
    
    properties (Hidden = true, SetAccess = immutable)
        opts % Model specific inputs
    end
    
    methods
        function obj = fitPsyche(x, y, type, varargin)
            
            if ~exist('x','var') && ~exist('y','var')
               % Create dummy object
               return
            end
            
            obj.x = x;
            obj.y = y;
            obj.type = type;
            obj.opts = varargin;
            
            switch type
                case 'WH'
                    [obj.model, obj.curve] = ...
                        obj.fitPsycheCurveWH(x, y, varargin{:});
                    
                    obj. coeffs = 'See .model';
                case 'GLM'
                    
                    [obj.coeffs, obj.curve, threshold] = ...
                        obj.fitPsycheCurveLogit(x, y, varargin{:});
                    
                otherwise
                    return
            end
            
        end
        
        function h = plotPsyche(obj)
            h = scatter(obj.x, obj.y);
            hold on
            h = plot(obj.curve(:,1), obj.curve(:,2), 'color', h.CData);
        end
        
    end
    
    methods (Static)
        [ffit, curve] = ...
            fitPsycheCurveWH(xAxis, yData, varargin)
        
        [coeffs, curve, threshold] = ...
            fitPsycheCurveLogit(xAxis, yData, weights, targets)
    end
    
end

