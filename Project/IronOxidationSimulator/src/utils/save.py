import pandas as pd
from matplotlib import pyplot as plt


def save(result, filename):
    dict_for_save = {
        "reaction_order_analysis":["Slope", "Intercept", "SE Slope", "SE Intercept", "R Squared"]
    }
    # 保存计算结果
    for option in result:
        result_df = pd.DataFrame(result[option], columns=dict_for_save[option])
        result_df.to_csv(option + '_result.csv', index=False)
        # 保存图像
        plt.savefig(option + '_visual.jpg')
