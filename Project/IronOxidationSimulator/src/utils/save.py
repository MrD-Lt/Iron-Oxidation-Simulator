"""
save.py
----------------------
Author: Dongzi Ding
Created: 2023-06-25
Modified: 2023-08-14
"""

import os
import pandas as pd


def save(result, dirname, figures):
    """
    Saves the result data to CSV files and figures to PNG files.

    Parameters:
        - result (dict): Dictionary containing the analysis results.
        - dirname (str): Directory path where the results will be saved.
        - figures (dict): Dictionary containing figures for saving as PNG.

    Returns:
        None
    """
    for option in result:
        if option == "3D plane plot":
            data_to_save = {
                "pH": [],
                "logFe": [],
                "logR": [],
                "Params": [],
                "R Squared": []
            }
            for method in result[option]:
                data_to_save["pH"].append(result[option][method][0])
                data_to_save["logFe"].append(result[option][method][1])
                data_to_save["logR"].append(result[option][method][2])
                data_to_save["Params"].append(result[option][method][3])
                data_to_save["R Squared"].append(result[option][method][4])
        elif option == "rate const analysis":
            data_to_save = {
                "Rate constant": [],
                "Intercept": [],
                "R Squared": []
                }
            for method in result[option]:
                data_to_save["Rate constant"].append(result[option][method]['slope'])
                data_to_save["Intercept"].append(result[option][method]['intercept'])
                data_to_save["R Squared"].append(result[option][method]['r_squared'])
        elif option == "initial rate analysis":
            data_to_save = {
                "Slope": [],
                "Intercept": [],
                "R Squared": []
            }
            for method in result[option]:
                if 'slopes' in result[option][method]:
                    data_to_save["Slope"].extend(result[option][method]['slopes'])
                    data_to_save["Intercept"].extend(result[option][method]['intercepts'])
                    data_to_save["R Squared"].extend(result[option][method]['r_squared_values'])
                else:
                    data_to_save["Slope"].append(result[option][method]['slope'])
                    data_to_save["Intercept"].append(result[option][method]['intercept'])
                    data_to_save["R Squared"].append(result[option][method]['r_squared'])

        else:

            data_to_save = {"Slope": [],
                            "Intercept": [], "R Squared": []}
            for method in result[option]:
                data_to_save["Slope"].append(result[option][method][2])
                data_to_save["Intercept"].append(result[option][method][3])
                data_to_save["R Squared"].append(result[option][method][4])
        result_df = pd.DataFrame(data_to_save)
        result_path = os.path.join(dirname, f"{option}_result.csv")
        try:
            result_df.to_csv(result_path, index=False)
        except Exception as e:
            print(f"Error saving CSV for option {option}: {e}")
        result_df.to_csv(result_path, index=False)

    for option, pixmap in figures.items():
        figure_path = os.path.join(dirname, f"{option}_figure.png")
        pixmap.save(figure_path, "PNG")

