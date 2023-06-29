clc;
clear;
close all;

% Import data from Excel file
data = xlsread('Book3.xlsx');
y = data(:,1);
sdy_absolute  = data(:,2);
sdy_upper  = data(:,3);
sdy_lower  = data(:,4);
x = data(:,5);
sdx_absolute  = data(:,6);
sdx_upper  = data(:,7);
sdx_lower  = data(:,8);

% Weight (w) calculation
w = 1 ./ (sdy_absolute.^2+sdx_absolute.^2);

% Weighted mean (wm) calculation
wmx = sum(w .* x) / sum(w);
wmy = sum(w .* y) / sum(w);

% Weighted covariance and variance calculation
covwxy = sum(w .* (x - wmx) .* (y - wmy)) / sum(w);
varwx = sum(w .* (x - wmx).^2) / sum(w);
varwy = sum(w .* (y - wmy).^2) / sum(w);

% Slope and intercept calculation
slope = covwxy / varwx;
intercept = wmy - slope * wmx;

% Standard error calculation
residuals = y - intercept - slope * x;
MSE = sum(w .* residuals.^2) / sum(w);
se_slope = sqrt(MSE / varwx / (length(x) - 2));
se_intercept = se_slope * sqrt(sum(w .* x.^2) / sum(w));

% Calculate R-squared
R_squared = covwxy^2 / (varwx * varwy);

% Output results
disp(['Slope: ', num2str(slope)])
disp(['Intercept: ', num2str(intercept)])
disp(['Standard error of slope: ', num2str(se_slope)])
disp(['Standard error of intercept: ', num2str(se_intercept)])


% Plot the data and regression line
figure('Position', [0 0 500 400]);
errorbar(x, y, sdy_lower, sdy_upper, sdx_lower, sdx_upper, 'ko', 'LineWidth', 1);
hold on;
x_fit = min(x):0.001:max(x);
y_fit = slope * x_fit + intercept;
plot(x_fit, y_fit, 'r-', 'LineWidth', 1);
set(gca,'FontSize',12);
xlabel('log([Fe], μM)');
ylabel('log(R0, μMs^-1)');
legend('Data', 'Weighted linear regression line', 'location', 'northwest','FontSize',12);

yticks = get(gca, 'YTick');
set(gca, 'YTickLabel', sprintf('%.1f\n', yticks));
xticks = get(gca, 'XTick');
set(gca, 'XTickLabel', sprintf('%.1f\n', xticks));

% Display the Weighted linear regression equation and R-squared
xlimits = xlim;
ylimits = ylim;
x_coordinate = xlimits(1) + 0.1*(xlimits(2) - xlimits(1));
y_coordinate1 = ylimits(1) + 0.1*(ylimits(2) - ylimits(1));
y_coordinate2 = ylimits(1) + 0.05*(ylimits(2) - ylimits(1));
text(x_coordinate, y_coordinate1, ['log[R0] = (' sprintf('%.2f', slope) '±' sprintf('%.2f', se_slope) ')log[Fe] + (' sprintf('%.2f', intercept) '±' sprintf('%.2f', se_intercept) ')'],'FontSize',12);
text(x_coordinate, y_coordinate2, ['R^2 = ' sprintf('%.2f', R_squared)],'FontSize',12);

