clc;
clear;
close all;

% 1. Import data for fitting 
% 1.1 experimental data
data = xlsread('3Dplot_fast_kinetic.xlsx');
pH = data(:, 2);
deltapH = data(:, 3);
logFe = data(:, 8); 
deltalogFe = data(:, 9); 
logR = data(:,10); 
deltalogR = data(:, 11); 

% Create a new figure
figure('Position', [1000, 500, 500, 400]); 

% Create a 3D scatter plot
plot3(pH, logFe, logR, 'ko', 'MarkerFaceColor', 'k', 'MarkerSize', 8)
hold on
% Plot error bars
%plot3([pH(:),pH(:)]', [logFe(:),logFe(:)]', [-deltalogR(:),deltalogR(:)]'+logR(:)', '-r', 'LineWidth', 2)
%plot3([pH(:),pH(:)]', [-deltalogFe(:),deltalogFe(:)]'+logFe(:)', [logR(:),logR(:)]', '-r', 'LineWidth', 2)
%plot3([-deltapH(:),deltapH]'+pH(:)', [logFe(:),logFe(:)]', [logR(:),logR(:)], '-r', 'LineWidth', 2)
view(3);

set(gca,'FontSize',15);
xlabel('pH')
ylabel('logFe_0')
zlabel('logR_0')
grid on

% Fit a plane thourgh the data using linear regression
X = [pH, logFe];
mdl = fitlm(X, logR);

% Get the R-squared value
R_squared = mdl.Rsquared.Ordinary;

% Evaluate the fitted plane over a grid
pH_range = linspace(min(pH), max(pH), 50);
logFe_range = linspace(min(logFe), max(logFe), 50);
[pH_grid, logFe_grid] = meshgrid(pH_range, logFe_range);
logR_fit = predict(mdl, [pH_grid(:), logFe_grid(:)]);
logR_fit = reshape(logR_fit, size(pH_grid));

% Plot the fitted plane

surf(pH_grid, logFe_grid, logR_fit, 'FaceAlpha', 0.5, 'EdgeColor', 'none');

% Customize grid and axes appearance (optional)
grid on
grid minor
ax = gca;
ax.XAxis.LineWidth = 1.5;
ax.YAxis.LineWidth = 1.5;
ax.ZAxis.LineWidth = 1.5;


% Get the coefficients and their standard errors
coefficients = mdl.Coefficients.Estimate;
standard_errors = mdl.Coefficients.SE;

% Extract coefficients
a = coefficients(2);
b = coefficients(3);
c = coefficients(1);

% Extract standard errors
se_a = standard_errors(2);
se_b = standard_errors(3);
se_c = standard_errors(1);

% Display the equation of the fitted plane
title('Equation of the fitted plane','FontSize',15, 'FontWeight','normal');
equation_str = sprintf('logR_0 = %.2fpH +%.2flogFe_0 +%.2f', a, b, c);
title(equation_str, 'FontSize', 15, 'FontWeight', 'normal');

n = length(pH);

% Display average R-squared and standard deviation on the figure
text(1.00, 0.95, ['R^2=' num2str(R_squared,2)], 'Units', 'normalized', 'HorizontalAlignment', 'right', 'VerticalAlignment', 'top','FontSize',15);
text(1.00, 0.88, ['(n=' num2str(n) ')'], 'Units', 'normalized', 'HorizontalAlignment', 'right', 'VerticalAlignment', 'top','FontSize',15);
hold off


saveas(gcf,'Planeplotfast_kinetic.png');
saveas(gcf,'Planeplotfast_kinetic.fig');

disp(['R-squared value: ', num2str(R_squared)]);
% Display standard errors
disp(['Standard error for coefficient a: ', num2str(se_a)]);
disp(['Standard error for coefficient b: ', num2str(se_b)]);
disp(['Standard error for coefficient c: ', num2str(se_c)]);
