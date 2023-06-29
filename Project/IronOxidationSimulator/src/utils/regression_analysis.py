# regression_analysis.py

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression


# 注意，这里需要Excel的数据符合预期的格式，还需要后面的调试来判断如何让用户正确输入。
# The code here needs the data in Excel to match the expected format,
# and also needs to be debugged later to determine how to get the user to enter it correctly.
def read_data(filename):
    """
    从Excel文件中读取数据
    Read data from an Excel file

    :param filename: 输入的Excel文件名 The input Excel filename
    :return: 包含x, y, 以及他们的误差的numpy数组
             Numpy arrays containing x, y and their errors
    """
    data = pd.read_excel(filename)
    y = data.iloc[:, 0].values
    sdy_absolute = data.iloc[:, 1].values
    sdy_upper = data.iloc[:, 2].values
    sdy_lower = data.iloc[:, 3].values
    x = data.iloc[:, 4].values
    sdx_absolute = data.iloc[:, 5].values
    sdx_upper = data.iloc[:, 6].values
    sdx_lower = data.iloc[:, 7].values
    return x, y, sdx_absolute, sdx_upper, sdx_lower, sdy_absolute, sdy_upper, sdy_lower

# 未处理问题：
# calculate_regression函数与sklearn的LinearRegression模型在功能上有些相似，它们都是用来做线性回归的。
# 然而，他们在处理误差和权重方面存在一些重要的区别。在calculate_regression函数中，我们使用了加权线性回归，而权重是根据每个数据点的绝对误差计算的。
# 这在数据点的误差不均等或误差信息可用的情况下是非常有用的。

# 相比之下，sklearn的LinearRegression模型执行的是普通的（非加权）线性回归，它假定所有数据点的误差都是均等的。
# 这使得LinearRegression在处理均匀误差的数据时非常高效，但在处理误差不均等的数据时可能不会提供最佳的模型。

def calculate_regression(x, y, sdx_absolute=None, sdy_absolute=None, use_sklearn=False):
    """
    根据输入的数据执行加权线性回归或普通线性回归，并返回斜率、截距和它们的标准误差
    Perform a weighted linear regression or ordinary linear regression based on the input data and return the slope, intercept and their standard errors

    :param x, y: 数据点的x, y坐标 Values of x, y coordinates of the data points
    :param sdx_absolute, sdy_absolute: x, y的绝对误差 Absolute errors of x, y
    :param use_sklearn: 是否使用sklearn的LinearRegression模型 Whether to use sklearn's LinearRegression model
    :return: 斜率，截距，斜率的标准误差，截距的标准误差，R平方值
             The slope, intercept, standard error of slope, standard error of intercept, R squared
    """
    if use_sklearn:
        # 使用sklearn的LinearRegression模型 Use sklearn's LinearRegression model
        model = LinearRegression()
        model.fit(x.reshape(-1, 1), y)
        slope = model.coef_[0]
        intercept = model.intercept_
        se_slope, se_intercept, r_squared = None, None, model.score(x.reshape(-1, 1), y)
    else:
        # 计算权重 Calculate weights
        w = 1 / (sdy_absolute ** 2 + sdx_absolute ** 2)

        # 计算加权均值 Calculate weighted means
        wmx = np.sum(w * x) / np.sum(w)
        wmy = np.sum(w * y) / np.sum(w)

        # 计算加权协方差和方差 Calculate weighted covariance and variance
        covwxy = np.sum(w * (x - wmx) * (y - wmy)) / np.sum(w)
        varwx = np.sum(w * (x - wmx) ** 2) / np.sum(w)
        varwy = np.sum(w * (y - wmy) ** 2) / np.sum(w)

        # 计算斜率和截距 Calculate slope and intercept
        slope = covwxy / varwx
        intercept = wmy - slope * wmx

        # 计算标准误差 Calculate standard errors
        residuals = y - intercept - slope * x
        mse = np.sum(w * residuals ** 2) / np.sum(w)
        se_slope = np.sqrt(mse / varwx / (len(x) - 2))
        se_intercept = se_slope * np.sqrt(np.sum(w * x ** 2) / np.sum(w))

        # 计算R平方值 Calculate R squared
        r_squared = covwxy ** 2 / (varwx * varwy)

    return slope, intercept, se_slope, se_intercept, r_squared


def plot_regression(x, y, sdx_lower, sdx_upper, sdy_lower, sdy_upper, slope, intercept, se_slope, se_intercept,
                    r_squared):
    """
    绘制数据点和回归线，并显示回归方程和R平方值
    Plot the data points and the regression line, and display the regression equation and R squared

    :param x, y: 数据点的x, y坐标 Values of x, y coordinates of the data points
    :param sdx_lower, sdx_upper, sdy_lower, sdy_upper: x, y的误差下界和上界 Lower and upper bounds of errors of x, y
    :param slope, intercept: 回归线的斜率和截距 Slope and intercept of the regression line
    :param se_slope, se_intercept: 斜率和截距的标准误差 Standard errors of slope and intercept
    :param r_squared: R平方值 R squared
    """
    # 绘制数据点和回归线 Plot data points and regression line
    plt.errorbar(x, y, yerr=[sdy_lower, sdy_upper], xerr=[sdx_lower, sdx_upper], fmt='ko')
    plt.plot([np.min(x), np.max(x)], [slope * np.min(x) + intercept, slope * np.max(x) + intercept], 'r-')
    plt.xlabel('log([Fe], μM)')
    plt.ylabel('log(R0, μMs^-1)')
    plt.legend(['Data', 'Weighted linear regression line'], loc='northwest')

    # 在图上显示加权线性回归方程和R平方值 Display the weighted linear regression equation and R squared on the plot
    xlim = plt.xlim()
    ylim = plt.ylim()
    text_x = xlim[0] + 0.1 * (xlim[1] - xlim[0])
    text_y = ylim[1] - 0.1 * (ylim[1] - ylim[0])
    plt.text(text_x, text_y, f"log[R0] = ({slope:.2f}±{se_slope:.2f})log[Fe] + ({intercept:.2f}±{se_intercept:.2f})")
    plt.text(text_x, text_y - 0.05 * (ylim[1] - ylim[0]), f"R² = {r_squared:.2f}")

    plt.show()

#