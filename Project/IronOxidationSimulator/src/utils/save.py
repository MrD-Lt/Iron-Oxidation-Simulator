import os
import pandas as pd


def save(result, dirname, figures):
    dict_for_save = {
        "reaction_order_analysis": ["Method", "Slope", "Intercept", "SE Slope", "SE Intercept", "R Squared"]
    }
    # 保存计算结果
    for option in result:
        data_to_save = {"Method": [], "Slope": [], "Intercept": [], "SE Slope": [], "SE Intercept": [], "R Squared": []}
        for method in result[option]:
            data_to_save["Method"].append(method)
            data_to_save["Slope"].append(result[option][method][6])
            data_to_save["Intercept"].append(result[option][method][7])
            data_to_save["SE Slope"].append(result[option][method][8])
            data_to_save["SE Intercept"].append(result[option][method][9])
            data_to_save["R Squared"].append(result[option][method][10])
        result_df = pd.DataFrame(data_to_save)
        result_path = os.path.join(dirname, f"{option}_result.csv")
        result_df.to_csv(result_path, index=False)

    # 保存图像
    for option, figure in figures.items():  # 遍历 figures 字典
        figure_path = os.path.join(dirname, f"{option}_figure.png")
        figure.savefig(figure_path)

